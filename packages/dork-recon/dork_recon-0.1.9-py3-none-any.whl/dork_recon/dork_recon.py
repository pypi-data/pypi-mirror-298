import argparse
import requests
import bs4
import urllib.parse
import re
import json
from abc import ABC, abstractmethod
from typing import List, Optional
from requests_tor import RequestsTor
from rich.console import Console
from rich.panel import Panel

# Configuração do Rich
console = Console()

DEFAULT_CONFIG_FILE = 'dorks_default.json'

# Classe abstrata para estratégia de busca
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, dork: str, page: int) -> Optional[str]:
        pass

# Classe abstrata para estratégia de parsing
class ParserStrategy(ABC):
    @abstractmethod
    def parse(self, html: str) -> List[str]:
        pass

# Classe para buscas no Google usando Tor (opcional)
class GoogleSearchStrategy(SearchStrategy):
    def __init__(self, use_tor: bool = False):
        # Se `use_tor` for True, usa o RequestsTor para as requisições
        self.session = RequestsTor() if use_tor else requests.Session()

    def search(self, dork: str, page: int) -> Optional[str]:
        start = page * 10
        url = f'https://google.com/search?q={urllib.parse.quote(dork)}&start={start}'
        try:
            console.print(f"[cyan]Realizando busca com dork: {dork}, Página: {page + 1}[/cyan]")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Erro na requisição HTTP: {e}[/red]")
            return None

# Classe para parsing dos resultados do Google
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

# Classe principal para executar o reconhecimento de dorks
class DorkRecon:
    def __init__(self, search_strategy: SearchStrategy, parser_strategy: ParserStrategy):
        self.search_strategy = search_strategy
        self.parser_strategy = parser_strategy

    def run(self, dorks: List[str], pages: int = 3) -> dict:
        results = {}
        for dork in dorks:
            console.print(f"[yellow]Executando dork: {dork}[/yellow]")
            results[dork] = []
            for page in range(pages):
                html = self.search_strategy.search(dork, page)
                if html:
                    urls = self.parser_strategy.parse(html)
                    for url in urls:
                        results[dork].append(url)
                        console.print(f"[green]URL encontrado:[/green] {url}")
                else:
                    console.print(f"[yellow]Falha ao obter resultados para a página {page + 1}.[/yellow]")
        return results

# Carrega dorks a partir de um arquivo JSON
def load_dorks_from_file(config_file: str) -> dict:
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            dorks = json.load(file)
            console.print(f"[green]Arquivo de configuração '{config_file}' carregado com sucesso.[/green]")
            return dorks
    except FileNotFoundError:
        console.print(f"[red]Arquivo de configuração '{config_file}' não encontrado![/red]")
        return {}
    except json.JSONDecodeError as e:
        console.print(f"[red]Erro ao decodificar o arquivo JSON: {e}[/red]")
        return {}

# Gera dorks personalizados com base no alvo
def generate_dorks_for_target(target: str, dorks: List[str]) -> List[str]:
    return [f"site:{target} {dork}" for dork in dorks]

# Salva os resultados em um arquivo JSON
def save_results_to_json(results: dict, output_file: str = 'dork_results.json'):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, indent=4)
    console.print(f"[green]Resultados salvos em {output_file}[/green]")

# Mostra os resultados de uma categoria específica usando Rich
def display_results_by_category(category: str, results_file: str = 'dork_results.json'):
    try:
        with open(results_file, 'r', encoding='utf-8') as file:
            results = json.load(file)
            if category in results:
                urls = "\n".join(results[category])
                panel = Panel(f"[green]URLs para a categoria {category}[/green]\n\n{urls}", title=f"[bold red]Resultados da categoria {category}[/bold red]")
                console.print(panel)
            else:
                console.print(f"[red]Categoria '{category}' não encontrada nos resultados.[/red]")
    except FileNotFoundError:
        console.print(f"[red]Arquivo de resultados '{results_file}' não encontrado![/red]")

# Função principal
def main():
    parser = argparse.ArgumentParser(description='Dork Recon')
    parser.add_argument('-c', '--config', type=str, help='Arquivo de configuração JSON com dorks predefinidos. Se omitido, será usado o arquivo default.')
    parser.add_argument('-t', '--target', type=str, help='Domínio ou URL alvo para gerar os dorks.')
    parser.add_argument('--type', type=str, choices=['files', 'pages', 'attack_points', 'config_files'], help='Tipo de dorks para buscar: "files", "pages", "attack_points" ou "config_files".')
    parser.add_argument('--tor', action='store_true', help='Usar a rede Tor para realizar as buscas.')
    parser.add_argument('-s', '--search', type=str, help='Mostrar resultados para uma categoria específica do arquivo de resultados.')

    args = parser.parse_args()

    if args.search:
        display_results_by_category(args.search)
        return

    if not args.target:
        console.print("[bold red]Por favor, forneça um --target válido ou use -s para buscar uma categoria existente.[/bold red]")
        return

    config_file = args.config if args.config else DEFAULT_CONFIG_FILE

    dorks_config = load_dorks_from_file(config_file)

    # Se --type não for passado, busca todas as categorias
    if not args.type:
        dorks_to_test = {key: dorks_config[key] for key in dorks_config.keys()}
    else:
        dorks_to_test = {args.type: dorks_config.get(args.type, [])}

    results = {}
    search_strategy = GoogleSearchStrategy(use_tor=args.tor)
    parser_strategy = GoogleParserStrategy()
    dork_recon = DorkRecon(search_strategy, parser_strategy)

    for category, dorks in dorks_to_test.items():
        if not dorks:
            console.print(f"[red]Nenhum dork encontrado para a categoria '{category}'.[/red]")
            continue

        target_dorks = generate_dorks_for_target(args.target, dorks)
        console.print(f"[cyan]Iniciando busca para a categoria: {category}[/cyan]")
        results[category] = dork_recon.run(target_dorks)

    save_results_to_json(results)

if __name__ == '__main__':
    main()
