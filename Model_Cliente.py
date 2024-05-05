from Model_Conta_corrente import Conta_corrente

class Cliente:
    def __init__(self, nome, nasc, cpf, endereco, contas=None):
        self.nome = nome
        self.nasc = nasc
        self.cpf = cpf
        self.endereco = endereco
        self.contas = contas if contas is not None else []

    def __str__(self):
        contas_str = "\n".join([f"Conta {i+1}: Número da conta: {conta.numero}, Agência {conta.ag}" for i, conta in enumerate(self.contas)])
        return f"{self.__class__.__name__}: {', '.join([f'{chave}: {valor}' for chave, valor in self.__dict__.items() if chave != 'contas'])}\nContas:\n{contas_str}"