#Bibliotecas
import os
import wget
import requests
from zipfile import ZipFile 
from bs4 import BeautifulSoup

#URL site
url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

#Diretório de destino
pasta_destino = "./temp"

#Mandando uma solicitação para a página
url_response = requests.get(url)

#Nome do arquivo ZIP que será criado
arquivo_zip = "anexos.zip"

#Verificando se a solicitação foi bem-sucedida
if url_response.status_code == 200:
    #Analisador do conteúdo HTML da página
    soap = BeautifulSoup(url_response.text, 'html.parser')

    #Vetor com o nome dos anexos que irá ser baixado
    anexos = []

    #Encontrando os links dos anexos desejados
    for anexo in ["Anexo I", "Anexo II."]:
        link_anexo = soap.find("a", text=anexo)
        if link_anexo:
            anexos.append(link_anexo['href'])
        else:
            print(f"Anexo '{anexo}' nao encontrado")

    #Baixando os anexos e compactando no final
    with ZipFile(os.path.join(pasta_destino, "Anexos.zip"),'w') as zip:
        for link_anexo in anexos:
            filename = os.path.join(pasta_destino, os.path.basename(link_anexo))
            wget.download(link_anexo, filename)
            print(f"Arquivo '{filename}' baixado com sucesso.")
            zip.write(os.path.basename(filename))
   
else: 
    print("Erro na solicitaçao para carregar a pagina", url_response.status_code)