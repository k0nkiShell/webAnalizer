import requests
from bs4 import BeautifulSoup, Comment
import argparse

# Colores ANSI para formato en la terminal
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
LIGHT_BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def analyze_url(url, search_comments=False):
    try:
        # Realizar la solicitud HTTP a la página
        response = requests.get(url)
        response.raise_for_status()

        # Parsear el contenido HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        if search_comments:
            # Buscar y mostrar todos los comentarios en el HTML
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            if comments:
                comments_text = '\n'.join(f"\t{GREEN}<!-- {comment.strip()} -->{RESET}" for comment in comments)
                print(f"{LIGHT_BLUE}{BOLD}{url}{RESET}\n{comments_text}")
            else:
                print(f"{LIGHT_BLUE}{BOLD}{url}{RESET}\n\t{RED}No se ha encontrado ningún comentario{RESET}")
        else:
            # Buscar elementos con estilo 'visibility: hidden'
            hidden_elements = soup.find_all(style=lambda value: value and 'visibility: hidden' in value)
            hidden_texts = [element.get_text(strip=True) for element in hidden_elements]

            if hidden_texts:
                result = '\n'.join(f"\t{YELLOW}{text}{RESET}" for text in hidden_texts)
                print(f"{LIGHT_BLUE}{BOLD}{url}{RESET}\n{result}")
            else:
                print(f"{LIGHT_BLUE}{BOLD}{url}{RESET}\n\t{RED}No se ha encontrado nada{RESET}")
    except requests.RequestException as e:
        print(f"{LIGHT_BLUE}{BOLD}{url}{RESET}\n\t{RED}Error al obtener la página: {e}{RESET}")

def main(file_path, search_comments):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
        
        # Analizar cada URL
        for url in urls:
            url = url.strip()
            if url:
                analyze_url(url, search_comments)
    except FileNotFoundError:
        print(f"{RED}El archivo no se encontró: {file_path}{RESET}")
    except Exception as e:
        print(f"{RED}Error al leer el archivo: {e}{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analiza URLs para elementos ocultos o comentarios.')
    parser.add_argument('file_path', type=str, help='Ruta del archivo que contiene las URLs a analizar.')
    parser.add_argument('--comment', action='store_true', help='Buscar y mostrar comentarios en el HTML.')

    args = parser.parse_args()
    
    main(args.file_path, args.comment)
