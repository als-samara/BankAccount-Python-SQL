from abc import ABC, abstractmethod
from Model_Extrato import Extrato

class Conta(ABC):
    def __init__(self, tipo, titular, numero=None, saldo=0.00, ag='0001', extrato=Extrato()):
        self.ag = ag
        self.numero = numero
        self._saldo = saldo
        self.titular = titular
        self.tipo = tipo
        self.extrato = extrato

    def __str__(self, incluir_extrato_limite_referencia=True):
        if incluir_extrato_limite_referencia:
            return f"{self.__class__.__name__}: {', '.join([f'{chave}:{valor}' for chave, valor in self.__dict__.items()])}"
        else:
            return f"{self.__class__.__name__}: ag:{self.ag}, numero:{self.numero}, _saldo:{self._saldo}, titular:{self.titular}, tipo:{self.tipo}, limite_saques_diario:{self.limite_saques_diario}, limite_por_saque:{self.limite_por_saque}, limite_da_conta:{self.limite_da_conta}"

    @abstractmethod
    def sacar(self, valor):
        pass

    @abstractmethod
    def depositar(self, valor, conta_destino):
        pass

    #@abstractmethod
    def transferir(self):
        pass