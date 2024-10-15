from datetime import datetime

class ContaBancaria:
    def __init__(self):
        self.saldo = 0
        self.transacoes_por_dia = {}
    
    def deposito(self, valor):
        if self.pode_realizar_transacao():
            self.saldo += valor
            self.adicionar_transacao(f"Depósito de R$ {valor:.2f}")
            return True
        return False

    def saque(self, valor):
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente")
        if self.pode_realizar_transacao():
            self.saldo -= valor
            self.adicionar_transacao(f"Saque de R$ {valor:.2f}")
            return True
        return False

    def pode_realizar_transacao(self):
        data = datetime.now().strftime("%d/%m/%Y")
        if data not in self.transacoes_por_dia:
            return True
        return len(self.transacoes_por_dia[data]) < 10 

    def adicionar_transacao(self, descricao):
        data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data = datetime.now().strftime("%d/%m/%Y")
        transacao = f"{descricao} - {data_hora}"

        if data not in self.transacoes_por_dia:
            self.transacoes_por_dia[data] = []

        self.transacoes_por_dia[data].append(transacao)

    def obter_extrato(self):
        extrato = f"Saldo: R$ {self.saldo:.2f}\n\nÚltimas Transações:\n"
        for transacoes in self.transacoes_por_dia.values():
            extrato += "\n".join(transacoes) + "\n"
        return extrato.strip() if transacoes else "Nenhuma transação realizada."

class Usuario:
    def __init__(self, nome, endereco, data_nascimento, cpf):
        self.nome = nome
        self.endereco = endereco
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.conta = ContaBancaria()

usuarios_cadastrados = []

def cadastrar_usuario():
    while True:
        nome = input("Digite o nome do usuário: ")
        endereco = input("Digite o endereço do usuário: ")
        data_nascimento = input("Digite a data de nascimento do usuário (dd/mm/aaaa): ")
        cpf = input("Digite o CPF do usuário: ")

        if not verificar_cpf_unico(cpf):
            print("Erro: Já existe um usuário cadastrado com esse CPF. Tente novamente.")
            continue
        
        usuario = Usuario(nome, endereco, data_nascimento, cpf)
        usuarios_cadastrados.append(usuario)
        return usuario

def verificar_cpf_unico(cpf):
    for usuario in usuarios_cadastrados:
        if usuario.cpf == cpf:
            return False
    return True

def menu_usuario(usuario):
    while True:
        print("\n--- Menu ---")
        print("1. Depósito")
        print("2. Saque")
        print("3. Extrato")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            valor = float(input("Digite o valor para depósito: "))
            if usuario.conta.deposito(valor):
                print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
            else:
                print("Limite de 10 transações por dia atingido. Não é possível realizar o depósito.")
        
        elif opcao == "2":
            valor = float(input("Digite o valor para saque: "))
            try:
                if usuario.conta.saque(valor):
                    print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
                else:
                    print("Limite de 10 transações por dia atingido. Não é possível realizar o saque.")
            except ValueError as e:
                print(e)
        
        elif opcao == "3":
            print(usuario.conta.obter_extrato())
        
        elif opcao == "4":
            print("Saindo...")
            break
        
        else:
            print("Opção inválida, tente novamente.")

def main():
    usuario = cadastrar_usuario()
    print(f"Usuário {usuario.nome} cadastrado com sucesso.")
    menu_usuario(usuario)

if __name__ == "__main__":
    main()
