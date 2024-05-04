class Extrato:
    def __init__(self):
        self.operacoes = []

    def __str__(self):
        if len(self.operacoes) <= 1:
            return "Não foram realizadas movimentações"
        else:
            return '\n'.join(map(str, self.operacoes))