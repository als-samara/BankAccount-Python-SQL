import time

from Model_Conta import Conta
from Model_Extrato import Extrato
from db_connection import db_connection, execute_query, read_query

class Conta_corrente(Conta):

    def __init__(self, tipo, titular, numero=None, _saldo=0.00, ag='0001', extrato=Extrato(), limite_saques_diario=3, limite_por_saque=700.00, limite_da_conta=500.00, limite_referencia=500.00):
        super().__init__(tipo, titular, numero, _saldo, ag, extrato)
        self.limite_saques_diario = limite_saques_diario  # 3
        self.limite_por_saque = limite_por_saque  # valor máximo por saque
        self.limite_da_conta = limite_da_conta  # limite (saldo que pode ficar negativo) variável da conta, conforme saques e depósitos são feitos
        self.limite_referencia = limite_referencia  # igual o limite variável inicial, mas usado para salvar o limite máximo real que a conta tem

    def depositar(self, valor, conta_destino):
        diferenca_limite = self.limite_referencia - self.limite_da_conta

        if (self.limite_referencia > self.limite_da_conta) and (valor <= diferenca_limite):
            self.limite_da_conta += valor
            execute_query(db_connection, f"UPDATE tb_checking_accounts SET limite_da_conta = {conta_destino.limite_da_conta} WHERE numero_conta = {conta_destino.numero}")
        elif (self.limite_referencia > self.limite_da_conta) and (valor > diferenca_limite):
            self.limite_da_conta = self.limite_referencia
            execute_query(db_connection, f"UPDATE tb_checking_accounts SET limite_da_conta = {conta_destino.limite_referencia} WHERE numero_conta = {conta_destino.numero}")
        #self._saldo += valor
        update_saldo_query = f"""UPDATE tb_checking_accounts 
                        SET saldo = {conta_destino._saldo + valor}
                        WHERE numero_conta = {conta_destino.numero}
            """
        execute_query(db_connection, update_saldo_query)

        print(f"Depósito de R${valor: .2f} realizado com sucesso!\nSaldo: R${conta_destino._saldo + valor: .2f}")


    def sacar(self, valor):
        extrato_id = self.retornar_extrato_id_por_numero_da_conta(self.numero)
        if Conta_corrente.limite_saques_atingido(self.limite_saques_diario, extrato_id):
            return print("Você atingiu o limite de saques diários!")

        saldo_disponivel = self._disp_para_saque()

        if (valor <= saldo_disponivel) and (valor <= self.limite_por_saque):
            if valor > self._saldo and valor <= self.limite_da_conta and self._saldo > 0:  # checa se usou limite, além do saldo
                limite_usado = valor - self._saldo  # calcula quanto limite usou
                execute_query(db_connection, f"""
                UPDATE tb_checking_accounts SET limite_da_conta = {self.limite_da_conta - limite_usado}
                WHERE numero_conta = {self.numero}
""")

            elif valor > self._saldo and valor <= self.limite_da_conta and self._saldo <= 0: # checa se usou só limite pois saldo ja era negativo ou 0
                execute_query(db_connection, f"""
                                UPDATE tb_checking_accounts SET limite_da_conta = {self.limite_da_conta - valor} 
                                WHERE numero_conta = {self.numero}
                """)

            self._saldo -= valor
            update_saldo_query = f"""UPDATE tb_checking_accounts 
                                    SET saldo = {self._saldo}
                                    WHERE numero_conta = {self.numero}
                        """
            execute_query(db_connection, update_saldo_query)
        else:
            if (valor > saldo_disponivel):
                return print("Você não possui saldo suficiente para realizar esta operação")
            else:
                return print("Valor fora do seu limite por saque. Consulte seu gerente ou app do banco para mais informações.")

        find_extrato_query = f"SELECT * FROM tb_extrato WHERE id={extrato_id}"
        extrato_tupla = read_query(db_connection, find_extrato_query)
        operacoes_anteriores = extrato_tupla[0][1]
        nova_operacao = f"Saque | Valor: R${valor: .2f} | Data: {time.localtime().tm_year}/{time.localtime().tm_mon}/{time.localtime().tm_mday} {time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}"
        operacoes_atualizadas = f"{operacoes_anteriores}, {nova_operacao}"
        update_extrato_query = f"""UPDATE tb_extrato
                            SET operacoes = '{operacoes_atualizadas}'
                            WHERE id = {extrato_id}
                """
        execute_query(db_connection, update_extrato_query)
        return print(f"Saque de R${valor: .2f} realizado com sucesso!\nSaldo: R${self._saldo: .2f}")

    def transferir(self, valor, nmr_conta_origem, nmr_conta_destino):
        pass
        # criar métodos CRUD, método de gerar automaticamente o número da conta
        # criar método para listar as contas por número
        # procurar pelo numero da conta de origem e destino (args do método)
        # criar exceção caso não encontre as contas
        # usar o método sacar na conta de origem
        # usar o método depositar na conta de destino

    @staticmethod
    def retornar_extrato_id_por_numero_da_conta(numero):
        query = f"SELECT * FROM tb_checking_accounts WHERE numero_conta={numero}"
        query_return = read_query(db_connection, query)  # tupla em uma lista
        return query_return[0][9]

    def _disp_para_saque(self):
        if self._saldo > 0:
            return self._saldo + self.limite_da_conta
        return self.limite_da_conta

    @staticmethod
    def limite_saques_atingido_antigo(limite_saques_diario, extrato):
        saques_hoje = sum(1 for operacao in extrato.operacoes if
                          f"Saque" in operacao and f"{time.localtime().tm_year}/{time.localtime().tm_mon}/{time.localtime().tm_mday}" in operacao)
        if saques_hoje >= limite_saques_diario:
            return True

    @staticmethod
    def limite_saques_atingido(limite_saques_diario, extrato_id):
        query = f"SELECT * FROM tb_extrato WHERE id={extrato_id}"
        result = read_query(db_connection, query)
        for row in result:
            operacoes = row[1].split(", ")  # Divide a string em uma lista de operações
        saques_hoje = sum(1 for operacao in operacoes if
                          f"Saque" in operacao and f"{time.localtime().tm_year}/{time.localtime().tm_mon}/{time.localtime().tm_mday}" in operacao)
        if saques_hoje >= limite_saques_diario:
            return True
        else:
            return False

    #def exibir_extrato(self):
        #print(f"\n{self.extrato.__str__()}\nSaldo atual: R${self._saldo: .2f}")

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