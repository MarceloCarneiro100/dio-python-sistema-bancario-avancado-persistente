from datetime import datetime, timezone
from abc import ABC, abstractmethod
import textwrap, platform, os


class ContaIterador:
    def __init__(self, contas):
        self._contas = contas
        self._contador = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            conta = self._contas[self._contador]
            self._contador += 1
            return conta
        except IndexError:
            raise StopIteration


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 10:
            print("\n<<< Você excedeu o número de transações permitidas para hoje! >>>")
            return
        
        transacao.registrar(conta)
    

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
    
    def __str__(self):
        return f"""
          Nome:\t{self.nome}
          CPF:\t{self.cpf}
        """


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
        saldo = self._saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n<<< Operação falhou! Você não tem saldo suficiente. >>>")
        
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
        
        else:
            print("\n<<< Operação falhou! O valor informado é inválido. >>>")
        
        return False
    
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
        else:
            print("\n<<< Operação falhou! O valor informado é inválido. >>>")
            return False
        
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n<<< Operação falhou! O valor do saque excede o limite. >>>")
        elif excedeu_saques:
            print("\n<<< Operação falhou! Número máximo de saques excedido. >>>")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            CPF:\t\t{self.cliente.cpf}
        """

            
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S"),
            }
    )
        
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

    
    def transacoes_do_dia(self):
        data_atual = datetime.now(timezone.utc).date()
        transacoes = []

        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao["data"], "%d-%m-%Y %H:%M:%S").date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes
    

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def log_transacao(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)

        tipo = func.__name__.replace("_", " ").capitalize()
        data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"\nLOG {tipo} realizado em {data_hora}")

        return resultado
    return wrapper


def menu():
    menu = f"""\n
    {" MENU ".center(40, '=')}
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [lu]\tListar clientes
    [nu]\tNovo cliente
    [q]\tSair 
    ==> Escolha uma das opções: """
    return input(textwrap.dedent(menu))


@log_transacao
def depositar(clientes):
    cliente, conta = obter_cliente_e_conta(clientes)

    if not cliente or not conta:
        return
    
    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("<<< Valor inválido. >>>")
        return
    
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def sacar(clientes): 
    cliente, conta = obter_cliente_e_conta(clientes)

    if not cliente or not conta:
        return
    
    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("<<< Valor inválido. >>>")
        return
    
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


@log_transacao
def exibir_extrato(clientes):
    cliente, conta = obter_cliente_e_conta(clientes)

    if not cliente or not conta:
        return
    
    print()
    print(" EXTRATO ".center(40, '='))
    extrato = ""

    transacoes = [
        f"\n({t['data']})\n{t['tipo']}: \n\tR$ {t['valor']:.2f}\n"
        for t in conta.historico.gerar_relatorio()
    ]
    
    if not transacoes:
        extrato = "Não foram realizadas movimentações"
    else:
        extrato = "".join(transacoes)
        
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print('=' * 40)


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    cliente = obter_cliente(clientes)
    
    if not cliente:
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    cliente.adicionar_conta(conta)
    contas.append(conta)

    print("\nConta criada com sucesso!")
    

def listar_contas(contas):
    if not contas:
        print("Não existem contas cadastradas")
        return
    
    print()
    print(" LISTA DE CONTAS ".center(40, '='))
    for conta in ContaIterador(contas):
        print(textwrap.dedent(str(conta)))
        print('-' * 40)

@log_transacao
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n<<< Já existe cliente com este CPF! >>>")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, número, bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)
    print("\nCliente criado com sucesso!")


def listar_clientes(clientes):
    if not clientes:
        print("Não existem clientes cadastrados")
        return
    
    print()
    print(" LISTA DE CLIENTES ".center(40, '='))
    for cliente in clientes:
        print(textwrap.dedent(str(cliente)))
        print('-' * 40)


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def filtrar_conta(numero_conta, contas):
    contas_filtradas = [conta for conta in contas if conta.numero == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n<<< Cliente não possui conta! >>>")
        return
    
    try:
        numero_conta = int(input("Insira o número da conta: "))
    except ValueError:
        print("\n<<< Número de conta inválido! >>>")
        return
    
    conta = filtrar_conta(numero_conta, cliente.contas)

    if not conta:
        print("\n<<< Conta não encontrada! >>>>")

    return conta

  
def obter_cliente_e_conta(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("<<< Cliente não encontrado. >>>")
        return None, None
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return cliente, None
    
    return cliente, conta


def obter_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("<<< Cliente não encontrado. >>>")
        return None
    
    return cliente


def limpar_tela():
    sistema = platform.system()
    if sistema == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def pausar():
    input("Pressione qualquer tecla para continuar....")


def main():
    clientes = []
    contas = []

    while True:
        limpar_tela()
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
            pausar()

        elif opcao == "s":
            sacar(clientes)
            pausar()

        elif opcao == "e":
            exibir_extrato(clientes)
            pausar()
        
        elif opcao == "nu":
            criar_cliente(clientes)
            pausar()
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
            pausar()
        
        elif opcao == "lc":
            listar_contas(contas)
            pausar()
        
        elif opcao == "lu":
            listar_clientes(clientes)
            pausar()
        
        elif opcao == "q":
            print("Encerrando a aplicação...")
            break

        else:
            print("\n<<< Operação inválida, por favor selecione novamente a opção desejada. >>>")
            pausar()

main()