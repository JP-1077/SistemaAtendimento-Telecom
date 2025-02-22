"""
=======================================================================================================================
OBJETIVO
    Este script tem o objetivo de criar uma API REST usando FLASK para registrar e listar os atendimentos para clientes 
    que estão com problemas referente alguns serviços de uma empresa de telecomunicações.

FUNCIONALIDADES
    - Registro de reclamações no banco de dados SQLite
    - Listagem de atendimentos já cadastrados
    - Acesso via FrontEnd

POR QUE FLASK?
    - O Flask foi escolhido por ser um framework web em python que se torna ideal para criar APIs REST simples e rápidas

ROTAS DISPONÍVEIS
    A API possui duas rotas principais:
        - '/registrar_reclamacao' : Utiliza o método POST para registrar um novo atendimento
        - '/listar_reclamacao': Utiliza o método GET para retornar e listar todas os atendimentos já cadastrados
=======================================================================================================================
"""

from flask import Flask, request, jsonify
import sqlite3
import datetime

# Inicializa a aplicação Flask
app = Flask(__name__)

# CORS é utilizado para que seja possível que haja requisições de diferentes lugares
from flask_cors import CORS
CORS(app)

# Função para conectar ao banco de dados
def conexao_banco():
    try:
        # Conecta ao banco de dados
        conn = sqlite3.connect("telecom.db")
        return conn
    except sqlite3.Error as e:
        return None

# Função para inserir um atendimento no banco de dados "telecom.db"
def inserir_atendimento(id_call, cpf_cliente, tipo_problema, descricao):
    conn = conexao_banco()
    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

# Cursor é utilizado para que possamos executar comandos SQL, a partir da conexão com o banco
    cursor = conn.cursor()

# Abaixo, está alguns paramêtros que determinei para que o INSERT no banco desse certo

    # Lista demonstra quais são os tipos de problemas válidos no campo "tipo_problema"
    problemas_validos = [
        'Massiva', 'Técnico não compareceu', 'Modem',
        'Sinal', 'Conta', 'Plano/Oferta/Desconto', 'Reparo'
    ]

    # Condicional que determina, se o tipo de problema for diferente dos listados, retorna uma 
    # mensagem de erro e fecha a conexão com o banco 
    if tipo_problema not in problemas_validos:
        conn.close()
        return jsonify({"erro": "Tipo de problema inválido. Escolha um dos permitidos."}), 400
    
    # Determina como deve ser o formato do datetime no campo de data dor formulário
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Tentar realizar um INSERT (Inserir) na tabela do banco TB_VOZ_CLIENTE, mas caso não dê certo
    # ele exiba uma mensagem que o ID já está registrado na base
    try:
        # O cursor vai executar esse INSERT, a partir com os valores preenchidos atráves do forms
        cursor.execute("""
            INSERT INTO TB_VOZ_CLIENTE (id_call, data_hora, cpf_cliente, tipo_problema, descricao)
            VALUES (?, ?, ?, ?, ?)
        """, (id_call, data_hora, cpf_cliente, tipo_problema, descricao))

        # Salva as alteração no banco de dados (telecom.db)
        conn.commit()

        # Mensagem final alertando que a o atendimento foi registrado com sucesso.
        resposta = jsonify({"mensagem": "Atendimento registrada com sucesso!"}), 201

        # Caso ele não consiga realizar a operação de INSERT ele demonstre essa mensagem na tela.
    except sqlite3.IntegrityError:
        resposta = jsonify({"erro": "ID da call já existe no sistema!"}), 400
    finally:
        # Feche a conexão com o banco de dados
        conn.close()

    return resposta

# Rota HTTP para registrar o atendimento
# ==================================================

# Define a rota e o método HTTP que vai ser utilizado
@app.route("/registrar_reclamacao", methods=["POST"])

# Função para registrar o atendimento realizado 
def registrar_atendimento():

    # Obtém os dados da requisição em formato JSON
    dados = request.json

    #  Extração dos dados necessários do forms
    id_call = dados.get("id_call")
    cpf_cliente = dados.get("cpf_cliente")
    tipo_problema = dados.get("tipo_problema")
    descricao = dados.get("descricao")

    # Condicional que determina se algum dos campos não tiver preenchido, 
    # ele retorna mensagem de erro.
    if not all([id_call, cpf_cliente, tipo_problema, descricao]):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    # Mas caso todos os campos tiverem preenchidos, ele insire o dados
    return inserir_atendimento(id_call, cpf_cliente, tipo_problema, descricao)

# Rota para listar todas as reclamações
# ==================================================

# Define a rota e o método HTTP que vai ser utilizado
@app.route("/listar_reclamacoes", methods=["GET"])

# Função para listar todos os atendimentos já realizados 
def listar_reclamacoes():

    # Inicie uma conexão com o banco de dados
    conn = conexao_banco()

    # Caso a conexão não der certo, vai retornar mensagem de falha
    if not conn:
        return jsonify({"erro": "Falha na conexão com o banco de dados"}), 500

    # Cursor para conseguir executar comandos SQL
    cursor = conn.cursor()

    # Execução de um SELECT pra capturar todos os registros de atendimento
    cursor.execute("SELECT * FROM TB_VOZ_CLIENTE")

    # Obtém os resultados da consulta SQL
    reclamacoes = cursor.fetchall()

    # Fecha a conexão com o banco
    conn.close()

    # Converte os resultados para um lista de dicionarios (JSON)
    atendimento_lista = [
        {
            "id": row[0],
            "id_call": row[1],
            "data_hora": row[2],
            "cpf_cliente": row[3],
            "tipo_problema": row[4],
            "descricao": row[5]
        }
        for row in reclamacoes
    ]

    # Retorna a lista dos atendimentos
    return jsonify(atendimento_lista), 200

# Executa a API Flask
if __name__ == "__main__":
    app.run(debug=True)
