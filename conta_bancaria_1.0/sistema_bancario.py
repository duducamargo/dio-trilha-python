saldo_inicial = 0.0
limite = 500.0
LIMITE_SAQUES = 3

menu = """
================= MENU =================

[1] Depositar
[2] Sacar
[3] Extrato
[4] Criar Conta
[5] Cadastrar Pessoa
[6] Sair

========================================

=> """

def cadastrar_pessoa():
    pessoas = {}
    
    while True:
        nome = input("Nome: ")
        data_nascimento = input("Data de Nascimento: ")
        cpf = input("CPF: ")
        endereco = input("Endereço (logradouro, número - bairro - cidade/sigla estado): ")
        
        pessoa = {
            'nome': nome,
            'data_nascimento': data_nascimento,
            'cpf': cpf,
            'endereco': endereco
        }
        
        if cpf in pessoas:
            print("CPF já cadastrado. Tente novamente.")
        else:
            pessoas[cpf] = pessoa
            
        opc = input("Deseja cadastrar outra pessoa? (s/n): ")
        if opc.lower() != 's':
            break
    
    return pessoas

def criar_conta(pessoas, contas):
    while True:
        cpf_conta = input("Insira o CPF da pessoa para criar a conta (ou digite 'sair' para voltar ao menu principal): ")
        
        if cpf_conta.lower() == 'sair':
            break
        
        if cpf_conta not in pessoas:
            print("CPF não encontrado. Tente novamente.")
            continue
        
        numero_conta = len(contas.get(cpf_conta, [])) + 1
        
        conta = {
            'numero_conta': f'0001-{numero_conta:04}',
            'cpf': cpf_conta,
            'saldo': saldo_inicial,
            'limite': limite,
            'extrato': "",
            'numero_saques': 0,
            'LIMITE_SAQUES': LIMITE_SAQUES
        }
        
        if cpf_conta in contas:
            contas[cpf_conta].append(conta)
        else:
            contas[cpf_conta] = [conta]
        
        print(f"Conta criada com sucesso para o CPF {cpf_conta}.")
        
        opc = input("Deseja criar outra conta? (s/n): ")
        if opc.lower() != 's':
            break
    
    return contas

def depositar(contas):
    cpf = input("Insira o seu CPF: ")

    if cpf in contas:
        contas_pessoa = contas[cpf]
        valor = float(input("Insira o valor que deseja depositar: "))
        
        if valor > 0:
            for conta in contas_pessoa:
                conta['saldo'] += valor
                conta['extrato'] += f"Depósito: R$ {valor:.2f}\n"
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")
    else:
        print("Não há contas com esse CPF!")

def sacar(contas):
    cpf = input("Insira o seu CPF: ")
    
    if cpf in contas:
        contas_pessoa = contas[cpf]
        valor = float(input("Informe o valor que deseja sacar: "))
        
        for conta in contas_pessoa:
            if valor <= 0:
                print("Operação inválida! O valor informado é inválido.")
            elif valor > conta['saldo']:
                print("Operação falhou! Você não tem saldo suficiente.")
            elif valor > conta['limite']:
                print("Operação falhou! O valor do saque excede o limite.")
            elif conta['numero_saques'] >= conta['LIMITE_SAQUES']:
                print("Operação falhou! Número máximo de saques excedido.")
            else:
                conta['saldo'] -= valor
                conta['extrato'] += f"Saque: R$ {valor:.2f}\n"
                conta['numero_saques'] += 1
                print("Saque realizado com sucesso!")
                return
    else:
        print("Não há contas com esse CPF!")

def exibir_extrato(contas):
    cpf = input("Insira o seu CPF: ")
    
    if cpf in contas:
        contas_pessoa = contas[cpf]
        
        for conta in contas_pessoa:
            print("\n================ EXTRATO ================")
            if not conta['extrato']:
                print("Não foram realizadas movimentações.")
            else:
                print(conta['extrato'])
            print(f"\nSaldo: R$ {conta['saldo']:.2f}")
            print(f"\nNúmero da conta: {conta['numero_conta']}")
            print("========================================")
            return
    else:
        print("Não há contas com esse CPF!")

def main():
    pessoas = cadastrar_pessoa()
    contas = {}
    
    while True:
        opc = input(menu)
        
        if opc == "1":
            depositar(contas)
        
        elif opc == "2":
            sacar(contas)
        
        elif opc == "3":
            exibir_extrato(contas)
        
        elif opc == "4":
            contas = criar_conta(pessoas, contas)
            
        elif opc == "5":
            pessoas = cadastrar_pessoa()
        
        elif opc == "6":
            print("Saindo...")
            break
        
        else:
            print("Operação Inválida!")
    
    print("Programa encerrado.")

if __name__ == "__main__":
    main()
