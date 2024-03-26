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

os.remove('Anexo_I_Rol_2021RN_465.2021_RN599_RN600.pdf')
    
