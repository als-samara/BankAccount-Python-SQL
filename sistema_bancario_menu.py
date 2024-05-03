from Controller_Cliente import cadastrar_cliente, pesquisar_cliente_por_cpf
from Controller_Conta import cadastrar_conta, listar_contas, listar_contas_do_usuario, remover_conta
from Model_Conta_corrente import Conta_corrente
from Controller_Extrato import exibir_extrato

menu = """

*********** Escolha uma opção: ***********

               [1] Depósito
               [2] Saque
               [3] Extrato
               [4] Transferência
               [5] Cadastrar Cliente
               [6] Cadastrar Conta Corrente
               [7] Listar Todas as Contas
               [8] Listar Contas do Usuário
               [9] Deletar Conta
               [S] Sair

******************************************

=> """

while True:
    option = input(menu)

    if option == '1':
        pass
    #input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '2':
        pass
    #input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '3':
        numero_conta = int(input("Digite o número da conta: "))
        exibir_extrato(numero_conta)
        input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '4':
        pass
    #input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '5':
        try:
            nome = input("Digite o nome completo: ")
            nasc = input("Digite a data de nascimento no formato YYYY-MM-DD: ")
            cpf = input("Digite o CPF: ")
            endereco = input("Digite o endereco: ")
            cadastrar_cliente(nome, nasc, cpf, endereco)
            print("Cliente cadastrado com sucesso")
        except:
            print("Verifique as informações digitadas e tente novamente")
        finally:
            input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '6':
        tipo = 0
        while tipo != 1:
            tipo = int(input("""
            Vamos começar o cadastro da sua conta! 
            Para cadastrar uma conta corrente, digite 1. 
            A funcionalidade de cadastrar uma conta Poupança está em desenvolvimento e será lançada em breve! 
            """))
        cpf = input("Digite o CPF do titular da conta: ")
        pesquisa_titular = pesquisar_cliente_por_cpf(cpf)
        if len(pesquisa_titular) == 0:
            print("CPF não cadastrado. Por favor, cadastre o cliente primeiro.")
        else:
            titular = pesquisa_titular[0][0]
            conta = Conta_corrente(tipo, titular)
            cadastrar_conta(conta)
        input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '7':
        listar_contas()
        input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '8':
        cpf = input("Digite o CPF para pesquisar as contas: ")
        listar_contas_do_usuario(cpf)
        input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '9':
        numero_conta = input("Digite o número da conta a ser excluída: ")
        remover_conta(numero_conta)
        input("Pressione qualquer tecla para voltar ao Menu")

    elif option.upper() == 'S':
        break

    else:
        input("Opção inválida, pressione qualquer tecla para voltar ao Menu")