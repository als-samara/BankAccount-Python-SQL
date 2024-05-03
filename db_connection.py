import mysql.connector
from mysql.connector import  Error
import pandas as pd

"""
try:
	db_connection = mysql.connector.connect(host='localhost', user='root', password='root', database='db_aramas_bank')
	print("Database connection made!")
except mysql.connector.Error as error:
	if error.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database doesn't exist")
	elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("User name or password is wrong")
	else:
		print(error)
else:
	db_connection.close()
"""

def create_server_connection(host_name, user_name, user_password, db_name):
    db_connection = None
    try:
        db_connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

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
        print(f"Error: '{err}'")
        return err

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def get_last_insert_id(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT LAST_INSERT_ID();")
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

create_client_table = """
CREATE TABLE tb_clients (
  cpf VARCHAR(40) PRIMARY KEY,
  full_name VARCHAR(40) NOT NULL,
  nasc DATE NOT NULL,
  endereco VARCHAR(255) NOT NULL
  );
 """

create_account_table = """
CREATE TABLE tb_checking_accounts (
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
CREATE TABLE tb_extrato (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    operacoes VARCHAR(1500),
    conta_numero BIGINT,
    FOREIGN KEY (conta_numero) REFERENCES tb_checking_accounts(numero_conta)
);
"""

db_connection = create_server_connection('localhost','root','root', 'db_aramas_bank')
#create_database(db_connection, "CREATE DATABASE IF NOT EXISTS db_aramas_bank")
#execute_query(db_connection, create_client_table)
#execute_query(db_connection, create_account_table)
alter_table_accounts = "ALTER TABLE tb_checking_accounts ADD COLUMN extrato_id BIGINT, ADD CONSTRAINT fk_extrato FOREIGN KEY (extrato_id) REFERENCES tb_extrato(id);"
execute_query(db_connection, alter_table_accounts)