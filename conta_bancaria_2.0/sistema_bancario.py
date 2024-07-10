from abc import ABC, abstractmethod

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

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        conta._saldo += self._valor
        conta._historico.adicionar_transacao(self)
        conta.adicionar_extrato(f"Depósito: R$ {self._valor:.2f}\n")

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    def registrar(self, conta):
        conta._saldo -= self._valor
        conta._historico.adicionar_transacao(self)
        conta.adicionar_extrato(f"Saque: R$ {self._valor:.2f}\n")

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Cliente:
    def __init__(self, endereco, contas=None):
        self._endereco = endereco
        self._contas = contas if contas else []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, agencia, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()
        self._extrato = ""

    def adicionar_extrato(self, descricao):
        self._extrato += descricao

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        if not self._extrato:
            print("Não foram realizadas movimentações.")
        else:
            print(self._extrato)
        print(f"\nSaldo: R$ {self._saldo:.2f}")
        print("========================================")

    @staticmethod
    def nova_conta(cliente, numero, agencia):
        conta = Conta(numero, agencia, cliente)
        cliente.adicionar_conta(conta)
        return conta

class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite, limite_saques):
        super().__init__(numero, agencia, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        self._saques_realizados = 0

    def pode_sacar(self, valor):
        if valor <= 0:
            print("Operação inválida! O valor informado é inválido.")
            return False
        if valor > self._saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
            return False
        if valor > self._limite:
            print("Operação falhou! O valor do saque excede o limite.")
            return False
        if self._saques_realizados >= self._limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False
        return True

    def sacar(self, valor):
        if self.pode_sacar(valor):
            self._saques_realizados += 1
            saque = Saque(valor)
            saque.registrar(self)
            print("Saque realizado com sucesso!")
        else:
            print("Não foi possível realizar o saque.")

# Funções de menu

def cadastrar_pessoa(pessoas):
    while True:
        nome = input("Nome: ")
        data_nascimento = input("Data de Nascimento: ")
        cpf = input("CPF: ")
        endereco = input("Endereço (logradouro, número - bairro - cidade/sigla estado): ")
        
        pessoa = PessoaFisica(endereco, cpf, nome, data_nascimento)
        
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
        
        pessoa = pessoas[cpf_conta]
        numero_conta = len(contas) + 1
        agencia = '0001'
        conta = ContaCorrente(numero_conta, agencia, pessoa, limite=500, limite_saques=3)
        if cpf_conta in contas:
            contas[cpf_conta].append(conta)
        else:
            contas[cpf_conta] = [conta]
        pessoa.adicionar_conta(conta)
        
        print(f"Conta criada com sucesso para o CPF {cpf_conta}.")
        
        opc = input("Deseja criar outra conta? (s/n): ")
        if opc.lower() != 's':
            break
    
    return contas

def selecionar_conta(contas_pessoa):
    for i, conta in enumerate(contas_pessoa, start=1):
        print(f"{i}. Conta {conta._numero} - Saldo: R$ {conta._saldo:.2f}")
    opcao = int(input("Selecione o número da conta: "))
    return contas_pessoa[opcao - 1]

def depositar(contas):
    cpf = input("Insira o seu CPF: ")

    if cpf in contas:
        contas_pessoa = contas[cpf]
        conta = selecionar_conta(contas_pessoa)
        valor = float(input("Insira o valor que deseja depositar: "))
        
        if valor > 0:
            deposito = Deposito(valor)
            conta._cliente.realizar_transacao(conta, deposito)
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")
    else:
        print("Não há contas com esse CPF!")

def sacar(contas):
    cpf = input("Insira o seu CPF: ")
    
    if cpf in contas:
        contas_pessoa = contas[cpf]
        conta = selecionar_conta(contas_pessoa)
        valor = float(input("Informe o valor que deseja sacar: "))
        conta.sacar(valor)
    else:
        print("Não há contas com esse CPF!")

def exibir_extrato(contas):
    cpf = input("Insira o seu CPF: ")
    
    if cpf in contas:
        contas_pessoa = contas[cpf]
        conta = selecionar_conta(contas_pessoa)
        conta.exibir_extrato()
    else:
        print("Não há contas com esse CPF!")
        

def main():
    pessoas = {}
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
            pessoas = cadastrar_pessoa(pessoas)
        
        elif opc == "6":
            print("Saindo...")
            break
        
        else:
            print("Operação Inválida!")
    
    print("Programa encerrado.")

if __name__ == "__main__":
    main()
