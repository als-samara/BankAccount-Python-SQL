import datetime

class Cliente:
    def __init__(self, nome, nasc, cpf, endereco, contas=None):
        self.nome = nome
        self.nasc = nasc
        self.cpf = cpf
        self.endereco = endereco
        self.contas = contas if contas is not None else []

    @staticmethod
    def checa_idade(data_nasc):
        data_atual = datetime.datetime.now()
        idade = data_atual.year - data_nasc.year
        if (data_atual.month, data_atual.day) < (data_nasc.month, data_nasc.day):
            idade -= 1
        return idade

    def __str__(self):
        contas_str = "\n".join([f"Conta {i+1}: Número da conta: {conta.numero}, Agência {conta.ag}" for i, conta in enumerate(self.contas)])
        return f"{self.__class__.__name__}: {', '.join([f'{chave}: {valor}' for chave, valor in self.__dict__.items() if chave != 'contas'])}\nContas:\n{contas_str}"

nasc = datetime.date(1997,5,5)
Cliente.checa_idade(nasc)