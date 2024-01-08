import requests
from bs4 import BeautifulSoup
import re
import logging
import pyfiglet

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para exibir ASCII art
def exibe_ascii_art():
    ascii_art = pyfiglet.figlet_format("OSINT Blogger")
    print(ascii_art)
    print('Criado Por Kensdy')

def verifica_blogger(url):
    try:
        # Cabeçalhos do navegador para simular uma requisição de navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Faz o pedido para a página com os cabeçalhos do navegador
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lança um erro para códigos de status HTTP diferentes de 200

        # Analisa o HTML da página
        soup = BeautifulSoup(response.text, 'html.parser')

        # Procura pela tag meta com content='blogger' e name='generator'
        blogger_tag = soup.find('meta', {'content': 'blogger', 'name': 'generator'})

        # Verifica se a tag foi encontrada
        if blogger_tag:
            return True  # É um site do Blogger
        else:
            return False  # Não é um site do Blogger

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao fazer a requisição para {url}: {e}")
        return None  # Retorna None em caso de erro

def encontra_dono_blogger(url):
    try:
        # Verifica se o site é feito em Blogger
        if not verifica_blogger(url):
            print("O site não é feito em Blogger.")
            return

        # Obter o conteúdo HTML da página
        response = requests.get(url)
        html_content = response.content.decode('utf-8')

        # Procurar por todas as ocorrências de "blogger.com/profile/" seguido de números
        profile_links = set(re.findall(r'blogger\.com/profile/(\d+)', html_content))

        # Criar URLs completos para cada número encontrado
        complete_urls = [f"https://www.blogger.com/profile/{profile}" for profile in profile_links]

        # Mostrar os resultados
        print("Perfis encontrados:")
        for url in complete_urls:
            print(url)
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao fazer a requisição para {url}: {e}")

def identifica_blogs_publicos(url):
    try:
        # Verifica se o link é de um perfil no Blogger
        if 'blogger.com/profile/' not in url:
            print("O link fornecido não é de um perfil no Blogger.")
            return

        # Obter o conteúdo HTML da página
        response = requests.get(url)
        html_content = response.content

        # Verificar se o texto "Profile Not Available" está presente em qualquer lugar da página
        if '<title>Profile Not Available</title>' in html_content.decode() or '<h1>Profile Not Available</h1>' in html_content.decode():
            print("O Perfil de Blogger que você solicitou não pode ser exibido. Diversos usuários do Blogger ainda não optaram por compartilhar publicamente seus perfis.")
        else:
            # Parsear o HTML com BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Encontrar os elementos desejados
            sidebar_items = soup.find_all('li', class_='sidebar-item')

            # Iterar sobre os elementos e extrair informações
            for item in sidebar_items:
                link = item.find('a')['href']
                nome = item.find('a').text
                print(f"Nome: {nome}, Link: {link}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao fazer a requisição para {url}: {e}")

# Exibir ASCII art no início do script
exibe_ascii_art()

# Loop principal
while True:
    # Menu de escolha
    print("\nEscolha a ferramenta por meio de seus números:")
    print("1- Verificar se um site foi criado usando o Blogger")
    print("2- Identificar o perfil do proprietário de um blog no Blogger")
    print("3- Identificar blogs públicos associados a um perfil no Blogger")
    print("4- Parar o script")

    opcao = input("Digite o número da ferramenta desejada: ")

    if opcao == '1':
        url_do_site = input("Digite a URL do site: ")
        resultado = verifica_blogger(url_do_site)

        if resultado is not None:
            if resultado:
                print("O site é feito em Blogger.")
            else:
                print("O site não é feito em Blogger.")

    elif opcao == '2':
        url_do_blog = input("Digite a URL do blog: ")
        encontra_dono_blogger(url_do_blog)

    elif opcao == '3':
        url_do_perfil = input("Digite a URL do perfil no Blogger: ")
        identifica_blogs_publicos(url_do_perfil)

    elif opcao == '4':
        print("Script encerrado.")
        break

    else:
        print("Opção inválida.")
