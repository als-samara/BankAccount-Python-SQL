from Model_Conta_corrente import Conta_corrente
from db_connection import execute_query, db_connection, read_query, get_last_insert_id
from Controller_Conta import verificar_existencia_conta

def exibir_extrato(numero_conta):
    query = f"SELECT * FROM tb_extrato WHERE conta_numero={numero_conta}"
    if verificar_existencia_conta(numero_conta):
        print("Conta não encontrada. Verifique o número da conta e tente novamente.")
        return
    result = read_query(db_connection, query)
    print(result[0][1])  # coluna de operações, é uma string, quando for mexer nos métodos bancários, ver como farei pra concatenar

#exibir_extrato(140)