from Model_Conta_corrente import Conta_corrente
from db_connection import execute_query, db_connection, read_query, get_last_insert_id
from Controller_Cliente import validar_cpf

def cadastrar_conta(Conta_corrente):
    sql_query_extrato = f"""
        INSERT INTO tb_extrato (operacoes)
        VALUES ("EXTRATO BANCÁRIO")
        """
    execute_query(db_connection, sql_query_extrato)
    last_extrato_id = get_last_insert_id(db_connection)

    sql_query = f"""
    INSERT INTO tb_checking_accounts (agencia, saldo, tipo, titular, limite_saques_diario, 
    limite_por_saque, limite_da_conta, limite_referencia, extrato_id)
    VALUES ('{Conta_corrente.ag}', {Conta_corrente._saldo},
{Conta_corrente.tipo}, '{Conta_corrente.titular}', {Conta_corrente.limite_saques_diario},
{Conta_corrente.limite_por_saque}, {Conta_corrente.limite_da_conta}, {Conta_corrente.limite_referencia}, {last_extrato_id})
    """
    query_return = execute_query(db_connection, sql_query)

    conta_numero = get_last_insert_id(db_connection)
    sql_query_update_extrato = f"""
            UPDATE tb_extrato
            SET conta_numero = {conta_numero}
            WHERE id = {last_extrato_id}
            """
    execute_query(db_connection, sql_query_update_extrato)

    if query_return is None:
        print("Conta cadastrada com sucesso!")

def listar_contas():
    query = "SELECT * FROM tb_checking_accounts;"
    contas = read_query(db_connection, query)
    if not contas:
        print("Nenhuma conta encontrada")
    for conta in contas:
        # Para cada conta, desempacota os valores da tupla (conta) nas variáveis correspondentes:
        agencia, numero, saldo, tipo, titular, limite_saques_diario, limite_por_saque, limite_da_conta, limite_referencia, extrato_id = conta
        conta_corrente = Conta_corrente(tipo, titular, numero, saldo, agencia, extrato_id, limite_saques_diario, limite_por_saque,
                                        limite_da_conta, limite_referencia)
        print(conta_corrente.__str__(False))

def listar_contas_do_usuario(cpf):
    query = f"""SELECT * FROM tb_checking_accounts
            WHERE titular={cpf}"""

    if not validar_cpf(cpf):
        return print("Número de CPF inválido")

    contas_usuario = read_query(db_connection, query)

    if not contas_usuario:
        try:
            raise Exception("Nenhuma conta encontrada para o CPF informado")
        except Exception as e:
            print(e)
            return

    for conta in contas_usuario:
        # Para cada conta, desempacota os valores da tupla (conta) nas variáveis correspondentes:
        agencia, numero, saldo, tipo, titular, limite_saques_diario, limite_por_saque, limite_da_conta, limite_referencia, extrato_id = conta
        conta_corrente = Conta_corrente(tipo, titular, numero, saldo, agencia, extrato_id, limite_saques_diario, limite_por_saque,
                                        limite_da_conta, limite_referencia)
        print(conta_corrente.__str__(False))

def verificar_existencia_conta(numero_conta):
    try:
        query = f"SELECT * FROM tb_checking_accounts WHERE numero_conta={numero_conta};"
        result = read_query(db_connection, query)
        if not result:  # Verifica se result é vazio
            print("Conta não encontrada. Verifique o número da conta e tente novamente.")
            return True
        return result is None or len(result) == 0
    except:
        print("Conta não encontrada. Verifique o número da conta e tente novamente.")
        return True

def remover_conta(numero_conta):
    if verificar_existencia_conta(numero_conta):
        return
    query = f"DELETE FROM tb_checking_accounts WHERE numero_conta={numero_conta};"
    confirma = input(f"Tem certeza que deseja excluir a conta {numero_conta}? Não será possível desfazer essa operação - [S / N] ")
    if confirma.upper() == 'S':
        execute_query(db_connection, query)
        print("Conta excluída com sucesso!")
    else:
        print("Operação cancelada")

def pesquisar_conta_por_numero(numero_conta):
    if verificar_existencia_conta(numero_conta):
        return
    query = f"SELECT * FROM tb_checking_accounts WHERE numero_conta={numero_conta}"
    query_return = read_query(db_connection, query)  # tupla em uma lista
    return query_return[0]  # tupla

def map_to_conta_corrente(nro_conta):
    conta_pesquisada = pesquisar_conta_por_numero(nro_conta)
    if conta_pesquisada is not None:
        # desempacota a tupla e transforma em objeto Conta_corrente pra acessar os atributos e métodos
        agencia, numero, saldo, tipo, titular, limite_saques_diario, limite_por_saque, limite_da_conta, limite_referencia, extrato_id = conta_pesquisada
        conta = Conta_corrente(tipo, titular, numero, saldo, agencia, extrato_id, limite_saques_diario, limite_por_saque,
                                            limite_da_conta, limite_referencia)
        return conta
    else:
        return

def deposito(nro_conta_destino, valor):
    try:
        conta_destino = map_to_conta_corrente(nro_conta_destino)
        conta_destino.depositar(valor, conta_destino)
    except:
        return

def saque(nro_conta, valor):
    try:
        conta = map_to_conta_corrente(nro_conta)
        return conta.sacar(valor)
    except:
        return

def transferencia(nro_conta_origem, nro_conta_destino, valor):
    try:
        if not verificar_existencia_conta(nro_conta_origem) and not verificar_existencia_conta(nro_conta_destino):
            conta_origem = map_to_conta_corrente(nro_conta_origem)
            conta_destino = map_to_conta_corrente(nro_conta_destino)
            retorno_saque = saque(conta_origem.numero, valor)
            if retorno_saque == False:
                return print("Não é possível realizar essa transferência, consulte seus limites de saque ou da conta no app do banco")
            else:
                conta_destino.depositar(valor, conta_destino)
        else:
            print("Uma das contas não foi encontrada.")
    except Exception as e:
        print(f"Erro durante a transferência: {e}")

