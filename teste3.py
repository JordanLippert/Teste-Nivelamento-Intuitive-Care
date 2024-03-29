import os
import mysql.connector
import pandas as pd
import zipfile
import csv


#Diretorios onde estão os arquivos ZIP
diretorio = './arquivos_teste3'

#Extração de todos arquivos ZIP para o diretório atual
for item in os.listdir(diretorio):
    if item.endswith('.zip'):
        arquivo_zip = os.path.join(diretorio, item)   
        with zipfile.ZipFile(arquivo_zip, 'r') as zip_ref:
            zip_ref.extractall(diretorio)
            print(f'Arquivo {arquivo_zip} descompactado com sucesso')
    
#Conexão ao MySQL Server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="dados_csv"
)
cursor = conn.cursor()

arquivos_csv = [f for f in os.listdir(diretorio) if f.endswith('.csv')]

def inserir_banco_de_dados(nome_tabela, caminho_arquivo_csv, codificacoes=['utf-8', 'latin-1', 'iso-8859-1']):
    for codificacao in codificacoes:
        try:
            with open(caminho_arquivo_csv, 'r', newline='', encoding=codificacao) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')  #Especificando o delimitador

                #Ler o cabeçalho do CSV
                header = next(csv_reader)

                #Cria a tabela no banco de dados se ela não existir
                create_table_query = f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({', '.join([f'{col} VARCHAR(255)' for col in header])})"
                cursor.execute(create_table_query)
                print("Tabela " + nome_tabela + " criada")

                #Iniciar uma transação
                conn.start_transaction()

                #Inserir os dados em lotes
                rows_to_insert = []
                batch_size = 3000  #Tamanho do lote
                current_batch = 0
                
                #Le as linhas por lotes de 3000 linhas cada
                for linha_atual, linha in enumerate(csv_reader, start=1):
                    rows_to_insert.append(linha)
                    if linha_atual % batch_size == 0:
                        current_batch += 1
                        insert_query = f"INSERT INTO {nome_tabela} ({', '.join(header)}) VALUES ({', '.join(['%s'] * len(header))})"
                        cursor.executemany(insert_query, rows_to_insert)
                        print(f"Lote {current_batch} aplicado no banco de dados (arquivo {caminho_arquivo_csv})")
                        rows_to_insert = []

                print("Lotes de inserção de dados inseridos")   

                #Inserir quaisquer linhas restantes
                if rows_to_insert:
                    insert_query = f"INSERT INTO {nome_tabela} ({', '.join(header)}) VALUES ({', '.join(['%s'] * len(header))})"
                    cursor.executemany(insert_query, rows_to_insert)

                print("Linhas extras inseridas")

                #Commit da transação
                conn.commit()
                print(f"Dados da tabela {nome_tabela} inseridos com sucesso")
                return True

        except UnicodeDecodeError:
            print(f"Erro de codificacao ao ler {caminho_arquivo_csv}, tentando proxima codificacao...")
    
    print("Todas as tentativas de codificacao falharam. Verifique o arquivo e as codificacoes.")
    return False

arquivos_csv = [f for f in os.listdir(diretorio) if f.endswith('.csv')]

#Loop pelos arquivos CSV
for arquivo in arquivos_csv:
    #Nome da tabela será o nome do arquivo CSV sem a extensão
    nome_arquivo = os.path.splitext(arquivo)[0]
    if (nome_arquivo == 'Relatorio_cadop'):
        nome_tabela = 'relatorio_cadop'
    else:
        nome_tabela = 'dados_tabela'

    inserir_banco_de_dados(nome_tabela, os.path.join(diretorio, arquivo))

#Fechar conexão
conn.close()
