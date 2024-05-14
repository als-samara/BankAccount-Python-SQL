from db_connection import db_connection, read_query
from Controller_Conta import verificar_existencia_conta, pesquisar_conta_por_numero
from Model_Extrato import Extrato

def search_extrato_for_id(id_extrato):
    try:
        query = f"SELECT * FROM tb_extrato WHERE id={id_extrato};"
        result = read_query(db_connection, query)
        if not result:
            print("Extrato id não localizado no banco de dados")
            return
        else:
            return result[0][1] ## operacoes
    except:
        return print("Falha ao procurar extrato pelo Id")

def map_to_object_extrato(id_extrato):
    search_extrato = search_extrato_for_id(id_extrato)
    if not search_extrato:
        return
    extrato_obj = Extrato()
    lista_operacoes = search_extrato.split(", ")  # cria uma lista de operações com a string de operações
    for operacao in lista_operacoes:
        extrato_obj.operacoes.append(operacao)
    return extrato_obj

def exibir_extrato(numero_conta):
    if verificar_existencia_conta(numero_conta):
        return

    query = f"SELECT * FROM tb_extrato WHERE conta_numero={numero_conta}"
    result = read_query(db_connection, query)
    extrato = map_to_object_extrato(result[0][0])
    conta = pesquisar_conta_por_numero(numero_conta)
    saldo_final = conta[2]
    print(extrato, f"\n\nSaldo atual: R$ {saldo_final}")