#Bibliotecas
import os
import pdfplumber
import PyPDF2
import pandas as pd
from io import BytesIO
from zipfile import ZipFile
from tempfile import NamedTemporaryFile

def subtituir_palavras_pdf(pdf_bytes, palavras_antigas, palavras_novas):
    #Criação dum leitor e de um escritor
    leitor = PyPDF2.PdfReader(pdf_bytes)
    escritor = PyPDF2.PdfWriter
    
    #Laço de repetição para extrair o texto de todas as páginas
    for pag_num in range (len(leitor.pages)):
        pagina = leitor.pages[pag_num]
        texto = pagina.extract_text()

        #Mais um laço para fazer a substituíção das palavras e repassar para o escritor
        for palavra_antiga, palavra_nova in zip (palavras_antigas, palavras_novas):
            texto = texto.replace(palavra_antiga, palavra_nova)

        pagina_modificada = PyPDF2.pdf.PageObject.create_text_object(None, texto)
        escritor.add_page(pagina_modificada)

    #Após processar todas as páginas será retornado um PDF modificado
    pdf_modificado = BytesIO()
    escritor.write(pdf_modificado)
    pdf_modificado.seek(0)
    return pdf_modificado

#Diretório de destino
pasta_destino = "./temp"

#Extração do Anexo I do arquivo ZIP
with ZipFile(os.path.join(pasta_destino, 'Anexos.zip'), 'r') as zip:
    with zip.open('Anexo_I_Rol_2021RN_465.2021_RN599_RN600.pdf') as pdf_file:
        #Ler o conteúdo do PDF em Bytes
        pdf_bytes = BytesIO(pdf_file.read())
       
        #Substituindo as palavras no PDF 
        pdf_modificado = subtituir_palavras_pdf(pdf_bytes, ["OD", "AMB"], ["SEG. ODONTOLOGICA", "SEG. AMBULATORIAL"])

        #Salvando PDF modificado em um arquivo temporário
        with NamedTemporaryFile(delete=False) as temp_pdf:
            temp_pdf.write(pdf_modificado.getbuffer())
            temp_pdf.seek(0)
        
        #Convertendo PDF modificado para CSV
        with pdfplumber.open(temp_pdf.name) as pdf:
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
        
    
