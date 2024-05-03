import time

from Model_Conta import Conta
from Model_Extrato import Extrato

class Conta_corrente(Conta):

    def __init__(self, tipo, titular, numero=None, _saldo=0.00, ag='0001', extrato=Extrato(), limite_saques_diario=3, limite_por_saque=700.00, limite_da_conta=500.00, limite_referencia=500.00):
        super().__init__(tipo, titular, numero, _saldo, ag, extrato)
        self.limite_saques_diario = limite_saques_diario  # 3
        self.limite_por_saque = limite_por_saque  # valor máximo por saque
        self.limite_da_conta = limite_da_conta  # limite (saldo que pode ficar negativo) variável da conta, conforme saques e depósitos são feitos
        self.limite_referencia = limite_referencia  # igual o limite variável inicial, mas usado para salvar o limite máximo real que a conta tem

    def depositar(self, valor):
        diferenca_limite = self.limite_referencia - self.limite_da_conta
        if (self.limite_referencia > self.limite_da_conta) and (valor <= diferenca_limite):
            self.limite_da_conta += valor
        elif (self.limite_referencia > self.limite_da_conta) and (valor > diferenca_limite):
            self.limite_da_conta = self.limite_referencia
        self._saldo += valor
        hora_deposito = time.localtime()
        operacao = f"Depósito | Valor: R${valor: .2f} | Data: {hora_deposito.tm_year}/{hora_deposito.tm_mon}/{hora_deposito.tm_mday}"
        self.extrato.operacoes.append(operacao)
        return print(f"Depósito de R${valor: .2f} realizado com sucesso!\nSaldo: R${self._saldo: .2f}")

    def sacar(self, valor):
        if Conta_corrente.limite_saques_atingido(self.limite_saques_diario, self.extrato):
            return print("Você atingiu o limite de saques diários!")

        saldo_disponivel = self._disp_para_saque()

        if (valor <= saldo_disponivel) and (valor <= self.limite_por_saque):
            if valor > self._saldo and valor <= self.limite_da_conta and self._saldo > 0:  # checa se usou limite
                limite_usado = valor - self._saldo  # calcula quanto limite usou
                self.limite_da_conta -= limite_usado
            elif valor > self._saldo and valor <= self.limite_da_conta and self._saldo <= 0: # checa se usou só limite pois saldo ja era negativo
                self.limite_da_conta -= valor
            self._saldo -= valor
            hora_saque = time.localtime()
            operacao = f"Saque | Valor: R${valor: .2f} | Data: {hora_saque.tm_year}/{hora_saque.tm_mon}/{hora_saque.tm_mday}"
            self.extrato.operacoes.append(operacao)
            return print(f"Saque de R${valor: .2f} realizado com sucesso!\nSaldo: R${self._saldo: .2f}")
        else:
            if (valor > saldo_disponivel):
                return print("Você não possui saldo suficiente para realizar esta operação")
            else:
                return print("Valor fora do seu limite por saque. Consulte seu gerente ou app do banco para mais informações.")

    def transferir(self, valor, nmr_conta_origem, nmr_conta_destino):
        pass
        # criar métodos CRUD, método de gerar automaticamente o número da conta
        # criar método para listar as contas por número
        # procurar pelo numero da conta de origem e destino (args do método)
        # criar exceção caso não encontre as contas
        # usar o método sacar na conta de origem
        # usar o método depositar na conta de destino

    def retornar_conta_por_numero(self, numero):
        pass
        # buscar no banco de dados

    def _disp_para_saque(self):
        if self._saldo > 0:
            return self._saldo + self.limite_da_conta
        return self.limite_da_conta

    @staticmethod
    def limite_saques_atingido(limite_saques_diario, extrato):
        saques_hoje = sum(1 for operacao in extrato.operacoes if
                          f"Saque" in operacao and f"{time.localtime().tm_year}/{time.localtime().tm_mon}/{time.localtime().tm_mday}" in operacao)
        if saques_hoje >= limite_saques_diario:
            return True

    def exibir_extrato(self):
        print(f"\n{self.extrato.__str__()}\nSaldo atual: R${self._saldo: .2f}")

"""
c1 = Conta_corrente('0001', 1, 400, 'samara', 1)

# TESTES SAQUES
print(c1)
print(f"{c1.limite_da_conta} - limite")
print(c1._saldo)
c1.sacar(800)  # valor fora do limite
c1.sacar(200)
print(f"{c1.limite_da_conta} - limite")
print(c1._saldo)
c1.sacar(300)
print(f"{c1.limite_da_conta} - limite")
print(c1._saldo)
c1.sacar(400)
c1.sacar(100)  # já realizou 3 saques, não vai aceitar mais
print(f"{c1.limite_da_conta} - limite")
print(c1._saldo)
print(c1.extrato)
# SAQUE FUNCIONANDO CORRETAMENTE

# TESTES DEPÓSITOS
c1.depositar(500)
c1.depositar(200)
print(f"{c1.limite_da_conta} - limite")
print(c1.extrato)
c1.exibir_extrato()
# DEPÓSITO FUNCIONANDO CORRETAMENTE
"""