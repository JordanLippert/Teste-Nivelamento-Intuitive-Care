import mysql.connector
from flask import Flask, request, jsonify

#Criando uma instância da aplicação Flask usando o nome do módulo como referência
app = Flask(__name__)

#Conexão ao MySQL Server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="dados_csv"
)
cursor = conn.cursor()

#Rota para a pesquisa textual
@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        #Realiza a consulta SQL para buscar os registros relevantes na tabela
        cursor.execute("SELECT * FROM relatorio_cadop WHERE Razao_Social LIKE %s OR Nome_Fantasia LIKE %s", ('%' + query + '%', '%' + query + '%'))
        results = cursor.fetchall()
        return jsonify(results)
    else:
        return jsonify([])
    
if __name__ == '__main__':
    app.run(debug=True)