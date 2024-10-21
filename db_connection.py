import os
import time
import mysql.connector
from mysql.connector import Error

def create_server_connection(host_name, user_name, user_password, db_name):
    db_connection = None
    time.sleep(15)
    try:
        db_connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        if db_connection.is_connected():
            print("Conectado ao MySQL")
            return db_connection
    except Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")

    return db_connection  # returns a connection object

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #print("Query successful")
    except Error as err:
        #print(f"Error: '{err}'")
        return err

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        return err

def get_last_insert_id(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT LAST_INSERT_ID();")
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

create_client_table = """
CREATE TABLE IF NOT EXISTS tb_clients (
  cpf VARCHAR(40) PRIMARY KEY,
  full_name VARCHAR(40) NOT NULL,
  nasc DATE NOT NULL,
  endereco VARCHAR(255) NOT NULL
  );
 """

create_account_table = """
CREATE TABLE IF NOT EXISTS tb_checking_accounts (
  agencia VARCHAR(10),
  numero_conta BIGINT AUTO_INCREMENT PRIMARY KEY,
  saldo DECIMAL(29, 2),
  tipo INT,
  titular VARCHAR(40),
  limite_saques_diario INT,
  limite_por_saque DECIMAL(10, 2),
  limite_da_conta DECIMAL(17,2),
  limite_referencia DECIMAL(17, 2),
  FOREIGN KEY (titular) REFERENCES tb_clients(cpf)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
"""

create_extrato_table = """
CREATE TABLE IF NOT EXISTS tb_extrato (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    operacoes TEXT
);
"""

db_connection = create_server_connection(os.getenv("DB_HOST", "mysql"),os.getenv("DB_USER", "root"),os.getenv("DB_PASSWORD", "root"),os.getenv("DB_NAME", "db_aramas_bank"))
create_database(db_connection, "CREATE DATABASE IF NOT EXISTS db_aramas_bank")
execute_query(db_connection, create_client_table)
execute_query(db_connection, create_account_table)
execute_query(db_connection, create_extrato_table)

def check_foreign_key_exists(connection, table_name, constraint_name):
    query = f"""
    SELECT CONSTRAINT_NAME 
    FROM information_schema.KEY_COLUMN_USAGE 
    WHERE TABLE_NAME = '{table_name}' 
    AND CONSTRAINT_NAME = '{constraint_name}';
    """
    result = read_query(connection, query)
    return len(result) > 0  # Retorna True se a chave estrangeira já existir

if not check_foreign_key_exists(db_connection, 'tb_checking_accounts', 'fk_extrato'):
    alter_table_accounts = "ALTER TABLE tb_checking_accounts ADD COLUMN extrato_id BIGINT, ADD CONSTRAINT fk_extrato FOREIGN KEY (extrato_id) REFERENCES tb_extrato(id);"
    execute_query(db_connection, alter_table_accounts)

if not check_foreign_key_exists(db_connection, 'tb_extrato', 'fk_conta_numero'):
    alter_table_extrato = "ALTER TABLE tb_extrato ADD COLUMN conta_numero BIGINT, ADD CONSTRAINT fk_conta_numero FOREIGN KEY (conta_numero) REFERENCES tb_checking_accounts(numero_conta);"
    execute_query(db_connection, alter_table_extrato)