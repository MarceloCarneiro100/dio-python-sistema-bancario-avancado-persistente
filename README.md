#  DIO -💰 Sistema Bancário Persistente em Python


<div align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python Badge">
</div>

Este é um projeto de sistema bancário desenvolvido em Python, com suporte a múltiplos clientes e contas, além de persistência de dados em arquivos `.txt` no formato JSON. Consiste em uma evolução das versões anteriores, também executada em terminal. O sistema permite criar clientes e contas, realizar depósitos, saques, emitir extratos e manter os dados salvos mesmo após encerrar a aplicação.


---

## 🚀 Funcionalidades

- Criar clientes com CPF, nome, data de nascimento e endereço
- Criar contas bancárias vinculadas a clientes
- Realizar depósitos e saques com regras de limite e quantidade
- Emitir extrato com histórico de transações
- Persistência automática de dados em arquivos de texto (`clientes.txt` e `contas.txt`)
- Registro de logs de transações em `log.txt`
- Limite de 10 transações por dia por cliente
- Limite de 3 saques diários por conta

---


## 🗃️ Estrutura de arquivos

- `app/`
  - `desafio.py` → Arquivo principal da aplicação
  - `persistencia.py` → Módulo responsável por salvar e carregar dados
  - `clientes.txt` → Armazena os dados dos clientes em JSON
  - `contas.txt` → Armazena os dados das contas e histórico de transações
  - `log.txt` → Armazena logs de todas as transações realizadas
  - `erro_log.txt` → Armazena erros de gravação, se ocorrerem
  - `__pycache__/` → Pasta automática do Python (pode ser ignorada)


---

## 🧠 Como funciona a persistência

- Ao iniciar o programa, os dados de `clientes.txt` e `contas.txt` são carregados automaticamente.
- Ao criar um novo cliente, ele é salvo com `salvar_cliente_individual()`.
- Ao criar uma nova conta ou realizar uma transação, a conta é atualizada com `atualizar_conta()`, substituindo a versão anterior no arquivo.
- O histórico de transações é salvo junto com a conta.
- O sistema nunca sobrescreve todos os dados — apenas atualiza ou adiciona o necessário.

---

## 🛠️ Como executar

1. Certifique-se de ter o Python 3 instalado.
2. Clone este repositório:
   ```bash
   https://github.com/MarceloCarneiro100/dio-python-sistema-bancario-avancado-persistente.git
   cd dio-python-sistema-bancario-avancado-persistente
   ```
3. Execute o programa:
   ```bash
   python app/desafio.py
   ```

---

## 📦 Dependências

Nenhuma dependência externa. O projeto utiliza apenas bibliotecas padrão do Python:

- `json`
- `datetime`
- `os`
- `platform`
- `textwrap`
- `pathlib`

---

## 🧑‍💻 Autor

Desenvolvido por Marcelo Carneiro como parte de um projeto de estudo em Python.

---
