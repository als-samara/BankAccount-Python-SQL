from Controller_Cliente import cadastrar_cliente, pesquisar_cliente_por_cpf
from Controller_Conta import cadastrar_conta, listar_contas, listar_contas_do_usuario, remover_conta, deposito, saque, transferencia
from Model_Conta_corrente import Conta_corrente
from Controller_Extrato import exibir_extrato
import datetime

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
        try:
            numero = int(input("Digite o número da conta: "))
            valor = int(input("Digite o valor: "))
            deposito(numero, valor)
        except ValueError:
            print("Verifique as informações inseridas e tente novamente")
        input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '2':
        try:
            numero = int(input("Digite o número da conta: "))
            valor = int(input("Digite o valor: "))
            saque(numero, valor)
        except ValueError:
            print("Verifique as informações inseridas e tente novamente")
        input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '3':
        try:
            numero_conta = int(input("Digite o número da conta: "))
            exibir_extrato(numero_conta)
        except ValueError:
            print("Verifique as informações inseridas e tente novamente")
        input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '4':
        try:
            nro_origem = int(input("Digite o número da conta de origem: "))
            nro_destino = int(input("Digite o número da conta de destino: "))
            valor = int(input("Digite o valor: "))
            confirma = input(f"Deseja confirmar a transferência de {valor: .2f} da conta {nro_origem} para a conta {nro_destino}? [S / N] ")
            if confirma.upper() == 'S':
                transferencia(nro_origem, nro_destino, valor)
        except ValueError:
            print("Verifique as informações inseridas e tente novamente")
        input("Pressione qualquer tecla para voltar ao Menu")

    elif option == '5':
        try:
            nome = input("Digite o nome completo: ")
            nasc = input("Digite a data de nascimento: ")
            date_obj = datetime.datetime.strptime(nasc, "%d/%m/%Y").date()
            cpf = input("Digite o CPF: ")
            rua = input("Digite o nome da rua do cliente: ")
            numero = input("Digite o número da casa: ")
            bairro = input("Digite o bairro: ")
            cidade = input("Digite a cidade: ")
            estado = input("Digite a sigla do estado: ")
            endereco = f"Rua: {rua}, nro {numero} - {bairro} - {cidade}/{estado}"
            cadastrar_cliente(nome, date_obj, cpf, endereco)
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