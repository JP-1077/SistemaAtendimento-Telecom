'''
=======================================================================================================================
OBJETIVO:
    Criar um banco de dados no Sistema de Gerenciamento de Dados SQLite chamado "telecom.db". Nesse banco armazenaremos
    informações referente ao Sistema de Registro de Atendimento. 

POR QUE SQLITE?
    O SQLite foi escolhido por ser uma biblioteca embutida no Python, e por conta disso ela se torna leve, fácil e ideal
    para aplicações que não exigem um servidor de banco de dados completo.

INFORMAÇÕES TB_VOZ_CLIENTE:
    A tabela 'TB_VOZ_CLIENTE' possui os seguintes campos:
        - id: Identificador único do atendimento
        - id_call: ID da chamada
        - data_hora: Data e Hora da Atendimento
        - cpf_cliente: CPF do Cliente
        - tipo_problema:Tipo do problema que o cliente está registrando
        - descricao: Descrição do Problema
=======================================================================================================================
'''
# Importa a biblioteca do SQLITE
import sqlite3

#  Realiza a conexão com o banco de dados
banco = sqlite3.connect("telecom.db")

# Cria um cursor para executar comandos SQL
cursor = banco.cursor()

# Criação da Tabela TB_VOZ_CLIENTE
cursor.execute("""
    
    CREATE TABLE IF NOT EXISTS TB_VOZ_CLIENTE (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    id_call VARCHAR(20) NOT NULL UNIQUE,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cpf_cliente VARCHAR(100) NOT NULL,
    tipo_problema TEXT NOT NULL CHECK(tipo_problema IN (
        'Massiva' 
        , 'Técnico não compareceu' 
        , 'Modem'
        , 'Sinal' 
        , 'Conta' 
        , 'Plano/Oferta/Desconto' 
        , 'Reparo'                       
    )),
    descricao TEXT NOT NULL
);
""")

# Salva as alteração no banco de dados (telecom.db)
banco.commit()

# Fecha a conexão com o banco de dados
banco.close()

# Print de mensagem pra validação se o banco e a tabela foi criados com sucessos
print("✅ Banco de dados e tabela criados com sucesso!")