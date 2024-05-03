from Model_Conta_corrente import Conta_corrente
from db_connection import execute_query, db_connection, read_query, get_last_insert_id
from Model_Extrato import Extrato
import time

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
        raise Exception("Nenhuma conta encontrada")
    for conta in contas:
        # Para cada conta, desempacota os valores da tupla (conta) nas variáveis correspondentes:
        agencia, numero, saldo, tipo, titular, limite_saques_diario, limite_por_saque, limite_da_conta, limite_referencia, extrato_id = conta
        conta_corrente = Conta_corrente(tipo, titular, numero, saldo, agencia, extrato_id, limite_saques_diario, limite_por_saque,
                                        limite_da_conta, limite_referencia)
        print(conta_corrente.__str__(False))

def listar_contas_do_usuario(cpf):
    query = f"""SELECT * FROM tb_checking_accounts
            WHERE titular={cpf}"""

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
    query = f"SELECT * FROM tb_checking_accounts WHERE numero_conta={numero_conta};"
    result = read_query(db_connection, query)
    return result is None or len(result) == 0

def remover_conta(numero_conta):
    if verificar_existencia_conta(numero_conta):
        print("Conta não encontrada. Verifique o número da conta e tente novamente.")
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
        print("Conta não encontrada. Verifique o número da conta e tente novamente.")
        return
    query = f"SELECT * FROM tb_checking_accounts WHERE numero_conta={numero_conta}"
    query_return = read_query(db_connection, query)  # tupla em uma lista
    return query_return[0]  # tupla

def deposito(nro_conta_destino, valor):
    conta_pesquisada = pesquisar_conta_por_numero(nro_conta_destino)

    # transforma a tupla em objeto Conta_corrente pra acessar os atributos
    agencia, numero, saldo, tipo, titular, limite_saques_diario, limite_por_saque, limite_da_conta, limite_referencia, extrato_id = conta_pesquisada
    conta_destino = Conta_corrente(tipo, titular, numero, saldo, agencia, extrato_id, limite_saques_diario, limite_por_saque,
                                        limite_da_conta, limite_referencia)

    diferenca_limite = conta_destino.limite_referencia - conta_destino.limite_da_conta
    if (conta_destino.limite_referencia > conta_destino.limite_da_conta) and valor <= diferenca_limite:
        conta_destino.limite_da_conta += valor
        execute_query(db_connection, f"UPDATE tb_checking_accounts SET limite_da_conta = {conta_destino.limite_da_conta}")
    elif (conta_destino.limite_referencia > conta_destino.limite_da_conta) and valor > diferenca_limite:
        conta_destino.limite_da_conta = conta_destino.limite_referencia
        execute_query(db_connection, f"UPDATE tb_checking_accounts SET limite_da_conta = {conta_destino.limite_referencia}")

    update_saldo_query = f"""UPDATE tb_checking_accounts 
                SET saldo = {conta_destino._saldo + valor}
                WHERE numero_conta = {conta_destino.numero}
    """
    execute_query(db_connection, update_saldo_query)
    conta_destino._saldo += valor

    extrato_query = f"""SELECT * FROM tb_extrato
                                WHERE id={conta_destino.extrato}
    """
    extrato_tupla = read_query(db_connection, extrato_query)
    operacoes_anteriores = extrato_tupla[0][1]
    nova_operacao = f"Depósito | Valor: R${valor: .2f} | Data: {time.localtime().tm_year}/{time.localtime().tm_mon}/{time.localtime().tm_mday}"
    operacoes_atualizadas = f"{operacoes_anteriores}, {nova_operacao}"

    update_extrato_query = f"""UPDATE tb_extrato
                SET operacoes = '{operacoes_atualizadas}'
                WHERE id = {conta_destino.extrato}
    """
    execute_query(db_connection, update_extrato_query)

    print(f"Depósito de R${valor: .2f} realizado com sucesso!\nSaldo: R${conta_destino._saldo: .2f}")


deposito(14, 3000)