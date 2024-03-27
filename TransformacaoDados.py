#Bibliotecas
import os
import pdfplumber
import pandas as pd
from zipfile import ZipFile
 
#Diretório de destino
pasta_destino = "./temp"

#Extração do Anexo I do arquivo ZIP
with ZipFile(os.path.join(pasta_destino, 'Anexos.zip'), 'r') as zip:
    #Extraindo Anexo I
    zip.extract('Anexo_I_Rol_2021RN_465.2021_RN599_RN600.pdf')
    #Convertendo PDF modificado para CSV
    with pdfplumber.open('Anexo_I_Rol_2021RN_465.2021_RN599_RN600.pdf') as pdf:
        df_lista = []
        for pag in pdf.pages:
            df = pag.extract_tables()
            df_lista.extend(df)
            if df_lista:
                df = pd.concat([pd.DataFrame(data) for data in df_lista])
                df.to_csv("Anexo_I.csv", index=False)
                print("Arquivo CSV gerado com sucesso!")
            else: 
                print("Erro: Os dados do arquivo nao sao um DataFrame")
    #Substituição das abreviações OD e AMB            
    df = pd.read_csv('Anexo_I.csv')
    df = df.replace('OD', 'SEG. ODONTOLOGICA')
    df = df.to_csv("Anexo_I_Editado1.csv", index=False)
    df = pd.read_csv('Anexo_I_Editado1.csv')
    df = df.replace('AMB', 'SEG. AMBULATORIAL')
    df = df.to_csv("Anexo_I_Editado2.csv",  header=1, index=True)

#Compactação do arquivo CSV modificado
with ZipFile(os.path.join(pasta_destino, "Teste_Jordan_Lippert_de_Oliveira.zip"),'w') as zip:
    zip.write("Anexo_I_Editado2.csv")

#Removendo os arquivos que não serão usados
os.remove('Anexo_I_Rol_2021RN_465.2021_RN599_RN600.pdf')
os.remove('Anexo_I.csv')
os.remove('Anexo_I_Editado1.csv')
os.remove('Anexo_I_Editado2.csv')