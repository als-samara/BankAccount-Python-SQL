from Model_Conta_corrente import Conta_corrente
from db_connection import execute_query, db_connection, read_query, get_last_insert_id
from Controller_Conta import verificar_existencia_conta
from Model_Extrato import Extrato
import time

def exibir_extrato(numero_conta):
    query = f"SELECT * FROM tb_extrato WHERE conta_numero={numero_conta}"

    if verificar_existencia_conta(numero_conta):
        return

    result = read_query(db_connection, query)
    if not result or (len(result) == 1 and result[0][1] == 'EXTRATO BANCÁRIO'):
        print("Não foram realizadas movimentações")
        return

    extrato = Extrato()
    for row in result:
        operacoes = row[1].split(", ")  # Divide a string em uma lista de operações
        for operacao in operacoes:
            extrato.operacoes.append(operacao)

    print(extrato)

#exibir_extrato(14)