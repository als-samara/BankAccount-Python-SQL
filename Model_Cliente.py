from Model_Conta_corrente import Conta_corrente

class Cliente:
    def __init__(self, nome, nasc, cpf, endereco, contas=None):
        self.nome = nome
        self.nasc = nasc
        self.cpf = cpf
        self.endereco = endereco
        self.contas = contas if contas is not None else []

    def __str__(self):
        #return f"{self.__class__.__name__}: {', '.join([f'{chave}: {valor}' for chave, valor in self.__dict__.items()])}"
        contas_str = "\n".join([f"Conta {i+1}: Número da conta: {conta.numero}, Agência {conta.ag}" for i, conta in enumerate(self.contas)])
        return f"{self.__class__.__name__}: {', '.join([f'{chave}: {valor}' for chave, valor in self.__dict__.items() if chave != 'contas'])}\nContas:\n{contas_str}"

"""cliente1 = Cliente('Samara', '20/08/1997', '46975938806', 'rua x, número 100')
c1 = Conta_corrente('0001', 1, 400, 'samara', 1)
c2 = Conta_corrente('0001', 2, 700, 'samara', 1)
cliente1.contas = [c1, c2]
print(cliente1)"""