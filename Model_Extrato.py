class Extrato:
    def __init__(self):
        self.operacoes = []

    def __str__(self):
        if len(self.operacoes) <= 0:
            return "Não foram realizadas movimentações"
        else:
            return '\n'.join(map(str, self.operacoes))

extrato = Extrato()
#print(extrato)
#extrato.operacoes.append('aaa')
#print(f"\n{extrato}")