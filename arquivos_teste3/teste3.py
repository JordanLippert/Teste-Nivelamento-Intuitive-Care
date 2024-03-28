import os
import mysql.connector
import pandas as pd
import zipfile
import csv

#Diretorios onde estão os arquivos ZIP
diretorio = os.path.join(os.getcwd(), './arquivos_teste3')

#Extração de todos arquivos ZIP para o diretório atual
for item in os.listdir(diretorio):
    if item.endswith('.zip'):
        arquivo_zip = os.path.join(diretorio, item)   
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            zip_ref.extractall(diretorio)
            print(f'Arquivo {arquivo_zip} decompactado com sucesso')
    
#Conexão ao MySQL Server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="dados_csv"
)
cursor = conn.cursor()
#cursor.execute("CREATE DATABASE dados_csv")

arquivos_csv = [f for f in os.listdir(diretorio) if f.endswith('2023.csv')]

#Loop pelos arquivos CSV 
for arquivo in arquivos_csv:
    #Nome da tabela será o nome do arquivo CSV sem a extensão
    nome_tabela = os.path.splitext(arquivo)[0]

    with open(os.path.join(diretorio, arquivo), 'r', newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        
        #Ler o cabeçalho do CSV
        header = next(csv_reader)    

        #Cria a tabela no banco de dados se ela não existir
        create_table_query = f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({', '.join([f'{col} VARCHAR(255)' for col in header])})"
        cursor.execute(create_table_query)

        #Inserir os dados linha por linha no banco de dados
        for row in csv_reader:
            insert_query = f"INSERT INTO {nome_tabela} VALUES ({', '.join(['%s'] * len(row))})"
            cursor.execute(insert_query, row)

#Commit e fechar conexão
conn.commit()
conn.close()