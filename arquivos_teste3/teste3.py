import os
import pandas as pd
import MySQLdb
import zipfile

#Diretorios onde estão os arquivos ZIP
diretorio_zip1 = "./arquivos_teste3/arquivos2023"
diretorio_zip2 = "./arquivos_teste3/arquivos2022"

for item in os.listdir(diretorio_zip1):
    if item.endswith('.zip'):
        #Caminho completo do arquivo ZIP
        arquivo_zip = os.path.join(diretorio_zip1, item)

        #Cria um objeto ZipFile
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            #Extrai todos arquivos ZIP para o diretório atual
            zip_ref.extractall(diretorio_zip1)
            print(f'Arquivo {arquivo_zip} decompactado com sucesso')

#Conexão com o banco de dados MySQL
conexao = MySQLdb.connect(host="localhost", user="jordan", passwd="123", db="Dados 2023")
cursor = conexao.cursor()

for arquivo in os.listdir(diretorio_zip1):
    if arquivo.endswith('.csv'):
        #Caminho completo do arquivo csv
        arquivo_csv = os.path.join(diretorio_zip1, arquivo)

        #Carrega os dados do arquivo CSV em um dataframe pandas
        dados = pd.read_csv(arquivo_csv)

        #Nome da tabela do banco de dados
        nome_tabela = os.path.splitext(arquivo)[0]

        #Insere os dados do dataframe no banco de dados
        dados.to_sql(nome_tabela, conexao, if_exists='replace', index=False)
        print(f'Dados do arquivo {arquivo} inseridos na tabela {nome_tabela} com sucesso')

#Fecha a conexão com o banco de dados
conexao.close()