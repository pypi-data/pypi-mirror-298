import argparse
import requests
import bs4
import urllib.parse
import re
import json
from abc import ABC, abstractmethod
from typing import List, Optional
from requests.exceptions import RequestException
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
import logging
import os

console = Console()
logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler()])
logger = logging.getLogger("rich")

DEFAULT_CONFIG_FILE = 'dorks_default.json'

class SearchStrategy(ABC):
    @abstractmethod
    def search(self, dork: str, page: int) -> Optional[str]:
        pass

class GoogleSearchStrategy(SearchStrategy):
    def search(self, dork: str, page: int) -> Optional[str]:
        start = page * 10
        url = f'https://google.com/search?q={urllib.parse.quote(dork)}&start={start}'
        try:
            logger.info(f"[cyan]Realizando busca com dork: {dork}, Página: {page + 1}[/cyan]")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            logger.error(f"[red]Erro na requisição HTTP: {e}[/red]")
            return None

class ParserStrategy(ABC):
    @abstractmethod
    def parse(self, html: str) -> List[str]:
        pass

class GoogleParserStrategy(ParserStrategy):
    def parse(self, html: str) -> List[str]:
        soup = bs4.BeautifulSoup(html, "html.parser")
        link_tags = soup.find_all('a')
        params_to_remove = ['sa', 'ved', 'usg']
        cleaned_urls = [
            self.clean_url(link_tag.get('href', ''), params_to_remove)
            for link_tag in link_tags
            if link_tag.get('href', '').startswith('/url?q=')
        ]
        return [url for url in cleaned_urls if url]

    def clean_url(self, href: str, params_to_remove: List[str]) -> str:
        url = href[7:]  # Remove '/url?q='
        url = urllib.parse.unquote(url)  # Decodifica caracteres

        if not (url.startswith('https://www.google.com') or
                url.startswith('https://support.google.com') or
                url.startswith('https://github.com') or
                url.startswith('https://stackoverflow.com') or
                url.startswith('https://accounts.google.com')):
            cleaned_url = re.sub(r'&?(?:{})=.*?(?=&|$)'.format('|'.join(params_to_remove)), '', url)
            return cleaned_url
        return ''

class DorkRecon:
    def __init__(self, search_strategy: SearchStrategy, parser_strategy: ParserStrategy):
        self.search_strategy = search_strategy
        self.parser_strategy = parser_strategy

    def run(self, dorks: List[str], pages: int = 3) -> dict:
        results = {}
        for dork in dorks:
            logger.info(f"[yellow]Executando dork: {dork}[/yellow]")
            results[dork] = []
            for page in range(pages):
                html = self.search_strategy.search(dork, page)
                if html:
                    urls = self.parser_strategy.parse(html)
                    for url in urls:
                        results[dork].append(url)
                        logger.info(f"[green]URL encontrado:[/green] {url}")
                else:
                    logger.warning(f"[yellow]Falha ao obter resultados para a página {page + 1}.[/yellow]")
        return results

def load_dorks_from_file(config_file: str) -> dict:
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            dorks = json.load(file)
            logger.info(f"[green]Arquivo de configuração '{config_file}' carregado com sucesso.[/green]")
            return dorks
    except FileNotFoundError:
        logger.error(f"[red]Arquivo de configuração '{config_file}' não encontrado![/red]")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"[red]Erro ao decodificar o arquivo JSON: {e}[/red]")
        return {}

def generate_dorks_for_target(target: str, dorks: List[str]) -> List[str]:
    return [f"site:{target} {dork}" for dork in dorks]

def save_results_to_json(results: dict, output_file: str = 'dork_results.json'):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)
    logger.info(f"[green]Resultados salvos em {output_file}[/green]")

def display_results_by_category(category: str, results_file: str = 'dork_results.json'):
    try:
        with open(results_file, 'r', encoding='utf-8') as file:
            results = json.load(file)
            if category in results:
                urls = "\n".join(results[category])
                panel = Panel(f"[green]URLs para a categoria {category}[/green]\n\n{urls}", title=f"[bold red]Resultados da categoria {category}[/bold red]")
                console.print(panel)
            else:
                logger.error(f"[red]Categoria '{category}' não encontrada nos resultados.[/red]")
    except FileNotFoundError:
        logger.error(f"[red]Arquivo de resultados '{results_file}' não encontrado![/red]")

def main():
    parser = argparse.ArgumentParser(description='Dork Recon')
    parser.add_argument('-c', '--config', type=str, help='Arquivo de configuração JSON com dorks predefinidos. Se omitido, será usado o arquivo default.')
    parser.add_argument('-t', '--target', type=str, help='Domínio ou URL alvo para gerar os dorks.')
    parser.add_argument('--type', type=str, choices=['files', 'pages', 'attack_points', 'config_files'], help='Tipo de dorks para buscar: "files", "pages", "attack_points" ou "config_files".')
    parser.add_argument('-s', '--search', type=str, help='Mostrar resultados para uma categoria específica do arquivo de resultados.')

    args = parser.parse_args()

    if args.search:
        display_results_by_category(args.search)
        return

    if not args.target or not args.type:
        console.print("[bold red]Por favor, forneça um --target e --type válidos ou use -s para buscar uma categoria existente.[/bold red]")
        return

    config_file = args.config if args.config else DEFAULT_CONFIG_FILE

    dorks_config = load_dorks_from_file(config_file)
    dorks = dorks_config.get(args.type, [])

    if not dorks:
        logger.error(f"[red]Nenhum dork encontrado para o tipo '{args.type}'.[/red]")
        return

    target_dorks = generate_dorks_for_target(args.target, dorks)

    search_strategy = GoogleSearchStrategy()
    parser_strategy = GoogleParserStrategy()
    dork_recon = DorkRecon(search_strategy, parser_strategy)

    results = dork_recon.run(target_dorks)
    save_results_to_json(results)

if __name__ == '__main__':
    main()
