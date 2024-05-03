from Model_Cliente import Cliente
from db_connection import execute_query, db_connection, read_query

def validar_cpf(cpf):
    return len(cpf) == 11
def cadastrar_cliente(nome, nasc, cpf, endereco):
    if not validar_cpf(cpf):
        print("CPF inválido. O CPF deve ter 11 dígitos.")
        return

    cliente = Cliente(nome, nasc, cpf, endereco)
    query_return = execute_query(db_connection, f"""
    INSERT INTO tb_clients VALUES 
    ('{cliente.cpf}','{cliente.nome}','{cliente.nasc}','{cliente.endereco}')
    """)

    if query_return is not None:
        if "Duplicate entry" in str(query_return):
            print("CPF já cadastrado. Verifique as informações digitadas e tente novamente.")
        elif "Incorrect date value" in str(query_return):
            print("Por favor, digite a data no formato solicitado (Ano-Mês-Dia)")
        else:
            print(query_return)
#cadastrar_cliente('Samara', '1997-08-20', '12345678900', 'rua x, número 100')

def pesquisar_cliente_por_cpf(cpf):
    query = f"SELECT * FROM tb_clients WHERE cpf={cpf};"
    query_return = read_query(db_connection, query)
    #print(query_return)
    return query_return

#pesquisar_cliente_por_cpf('46975938806')