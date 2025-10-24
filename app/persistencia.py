import json
from pathlib import Path

ROOT_PATH = Path(__file__).parent

def carregar_json_de_arquivo(caminho):
    try:
        with open(ROOT_PATH / caminho, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Erro ao carregar {caminho}: {e}")
        return []
    

def adicionar_json_em_arquivo(caminho, novo_item):
    dados_existentes = carregar_json_de_arquivo(caminho)
    dados_existentes.append(novo_item)

    try:
        with open(ROOT_PATH / caminho, 'w', encoding='utf-8') as arquivo:
            json.dump(dados_existentes, arquivo, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar {caminho}: {e}")


def salvar_cliente_individual(cliente):
    dado = {
        "nome": cliente.nome,
        "cpf": cliente.cpf,
        "data_nascimento": cliente.data_nascimento,
        "endereco": cliente.endereco
    }

    adicionar_json_em_arquivo('clientes.txt', dado)



def atualizar_conta(conta):
    contas = carregar_json_de_arquivo('contas.txt')
    nova_conta = {
        "numero": conta.numero,
        "agencia": conta.agencia,
        "cpf_cliente": conta.cliente.cpf,
        "saldo": conta.saldo,
        "limite": conta.limite,
        "limite_saques": conta.limite_saques,
        "historico": conta.historico.transacoes
    }

    # Remove conta antiga com mesmo número
    contas = [c for c in contas if c["numero"] != conta.numero or c["cpf_cliente"] != conta.cliente.cpf]

    # Adiciona versão atualizada
    contas.append(nova_conta)

    # Salva tudo de volta
    try:
        with open(ROOT_PATH / 'contas.txt', 'w', encoding='utf-8') as arquivo:
            json.dump(contas, arquivo, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao atualizar conta: {e}")


