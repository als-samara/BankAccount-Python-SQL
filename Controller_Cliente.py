from Model_Cliente import Cliente
from db_connection import execute_query, db_connection, read_query

def validar_cpf(cpf):
    return len(cpf) == 11
def cadastrar_cliente(nome, nasc, cpf, endereco):
    if not validar_cpf(cpf):
        print("CPF inválido. O CPF deve ter 11 dígitos.")
        return

    cliente = Cliente(nome, nasc, cpf, endereco)
    if cliente.checa_idade(nasc) >= 18:
        query_return = execute_query(db_connection, f"""
        INSERT INTO tb_clients VALUES 
        ('{cliente.cpf}','{cliente.nome}','{cliente.nasc}','{cliente.endereco}')
        """)
    else:
        return print("Não é possível criar uma Conta Corrente para menores de idade")

    if query_return is not None:
        if "Duplicate entry" in str(query_return):
            print("CPF já cadastrado. Verifique as informações digitadas e tente novamente.")
            return
        elif "Incorrect date value" in str(query_return):
            print("Verifique o formato dos objetos de data")
            return
        else:
            print(query_return)
            return
    print("Cliente cadastrado com sucesso")

def pesquisar_cliente_por_cpf(cpf):
    query = f"SELECT * FROM tb_clients WHERE cpf={cpf};"
    query_return = read_query(db_connection, query)
    return query_return