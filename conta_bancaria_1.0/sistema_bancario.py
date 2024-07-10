saldo = 0.0
limite = 500.0
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
menu = """
================= MENU =================

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

========================================

=> """

while True:
    opc = input(menu) 

    if opc == "1":
        valor = float(input("Insira o valor que deseja depositar: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido.")
            input("Pressione Enter para voltar ao menu...") 


    elif opc == "2":
        valor = float(input("Informe o valor que deseja sacar: "))

        if valor > saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            input("Pressione Enter para voltar ao menu...") 

        elif valor > limite:
            print("Operação falhou! O valor do saque excede o limite.")
            input("Pressione Enter para voltar ao menu...") 
            
        elif numero_saques >= LIMITE_SAQUES:
            print("Operação falhou! Número máximo de saques excedido.")
            input("Pressione Enter para voltar ao menu...") 

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação inválida! O valor informado é inválido")
            input("Pressione Enter para voltar ao menu...") 

    elif opc == "3":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}") 
        print("==========================================")

        input("Pressione Enter para voltar ao menu...") 

    elif opc == "4":
        print("Saindo...")
        break

    else:
        print("Operação Inválida!")
        input("Pressione Enter para voltar ao menu...") 
