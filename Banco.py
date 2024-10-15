from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor <= self._saldo:
            self._saldo -= valor
            self._historico.adicionar_transacao(f"Saque de {valor}")
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(f"Depósito de {valor}")
            return True
        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0

    def sacar(self, valor):
        if self._saques_realizados < self._limite_saques and (self._saldo + self._limite) >= valor:
            self._saldo -= valor
            self._saques_realizados += 1
            self._historico.adicionar_transacao(f"Saque de {valor}")
            return True
        return False

    def __str__(self):
        return f"ContaCorrente {self.numero} - Saldo: {self.saldo} - Limite: {self._limite}"


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append((transacao, datetime.now()))


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.sacar(self._valor)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        conta.depositar(self._valor)


# Menu functions
def exibir_menu():
    print("\n--- Menu Principal ---")
    print("1. Criar Cliente")
    print("2. Criar Conta")
    print("3. Realizar Depósito")
    print("4. Realizar Saque")
    print("5. Exibir Saldo")
    print("6. Exibir Histórico de Transações")
    print("0. Sair")


def criar_cliente():
    nome = input("Nome: ")
    data_nascimento = input("Data de Nascimento (DD/MM/AAAA): ")
    cpf = input("CPF: ")
    endereco = input("Endereço: ")
    return PessoaFisica(nome, data_nascimento, cpf, endereco)


def criar_conta(cliente):
    numero = input("Número da Conta: ")
    return ContaCorrente.nova_conta(cliente, numero, limite=500, limite_saques=3)


def realizar_deposito(conta):
    valor = float(input("Valor do Depósito: R$ "))
    deposito = Deposito(valor)
    deposito.registrar(conta)
    print(f"Depósito de R${valor} realizado com sucesso!")


def realizar_saque(conta):
    valor = float(input("Valor do Saque: R$ "))
    saque = Saque(valor)
    if saque.registrar(conta):
        print(f"Saque de R${valor} realizado com sucesso!")
    else:
        print("Saldo insuficiente ou limite de saques atingido.")


def exibir_saldo(conta):
    print(f"Saldo atual: R${conta.saldo}")


def exibir_historico(conta):
    print("\n--- Histórico de Transações ---")
    for transacao, data in conta.historico.transacoes:
        print(f"{transacao} - Data: {data}")


def main():
    clientes = []
    contas = []

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cliente = criar_cliente()
            clientes.append(cliente)
            print("Cliente criado com sucesso!")

        elif opcao == "2":
            if not clientes:
                print("Nenhum cliente cadastrado. Crie um cliente primeiro.")
            else:
                for i, cliente in enumerate(clientes):
                    print(f"{i + 1}. {cliente.nome} - CPF: {cliente.cpf}")
                cliente_escolhido = int(input("Escolha um cliente (número): ")) - 1
                conta = criar_conta(clientes[cliente_escolhido])
                clientes[cliente_escolhido].adicionar_conta(conta)
                contas.append(conta)
                print("Conta criada com sucesso!")

        elif opcao == "3":
            if not contas:
                print("Nenhuma conta cadastrada. Crie uma conta primeiro.")
            else:
                for i, conta in enumerate(contas):
                    print(f"{i + 1}. Conta {conta.numero} - Cliente: {conta.cliente.nome}")
                conta_escolhida = int(input("Escolha uma conta (número): ")) - 1
                realizar_deposito(contas[conta_escolhida])

        elif opcao == "4":
            if not contas:
                print("Nenhuma conta cadastrada. Crie uma conta primeiro.")
            else:
                for i, conta in enumerate(contas):
                    print(f"{i + 1}. Conta {conta.numero} - Cliente: {conta.cliente.nome}")
                conta_escolhida = int(input("Escolha uma conta (número): ")) - 1
                realizar_saque(contas[conta_escolhida])

        elif opcao == "5":
            if not contas:
                print("Nenhuma conta cadastrada. Crie uma conta primeiro.")
            else:
                for i, conta in enumerate(contas):
                    print(f"{i + 1}. Conta {conta.numero} - Cliente: {conta.cliente.nome}")
                conta_escolhida = int(input("Escolha uma conta (número): ")) - 1
                exibir_saldo(contas[conta_escolhida])

        elif opcao == "6":
            if not contas:
                print("Nenhuma conta cadastrada. Crie uma conta primeiro.")
            else:
                for i, conta in enumerate(contas):
                    print(f"{i + 1}. Conta {conta.numero} - Cliente: {conta.cliente.nome}")
                conta_escolhida = int(input("Escolha uma conta (número): ")) - 1
                exibir_historico(contas[conta_escolhida])

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()
