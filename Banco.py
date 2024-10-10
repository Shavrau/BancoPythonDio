class ContaBancaria:
    def __init__(self):
        self.saldo = 0
    
    def deposito(self, valor):
        self.saldo += valor
    
    def saque(self, valor):
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= valor
    
    def consultar_saldo(self):
        return self.saldo

conta = ContaBancaria()

while True:
    print("\n--- Menu ---")
    print("1. Depósito")
    print("2. Saque")
    print("3. Consultar saldo")
    print("4. Sair")
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        valor = float(input("Digite o valor para depósito: "))
        conta.deposito(valor)
        print(f"Depósito de R$ {valor} realizado com sucesso.")
    
    elif opcao == "2":
        valor = float(input("Digite o valor para saque: "))
        try:
            conta.saque(valor)
            print(f"Saque de R$ {valor} realizado com sucesso.")
        except ValueError as e:
            print(e)
    
    elif opcao == "3":
        print(f"Seu saldo é R$ {conta.consultar_saldo()}")
    
    elif opcao == "4":
        print("Saindo...")
        break
    
    else:
        print("Opção inválida, tente novamente.")
