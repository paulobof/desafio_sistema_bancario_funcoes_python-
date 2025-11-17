# 🏦 Sistema Bancário com Funções Python

## 📋 Descrição

Este projeto é parte do **Desafio DIO (Digital Innovation One)** para **Otimização do Sistema Bancário com Funções Python**. 

Neste desafio, tive a oportunidade de otimizar um Sistema Bancário previamente desenvolvido com o uso de **funções Python avançadas**. O objetivo foi aprimorar a estrutura e a eficiência do sistema, implementando as operações de depósito, saque e extrato em funções específicas com diferentes tipos de argumentos.

O código foi refatorado e dividido em **funções reutilizáveis**, facilitando a manutenção e o entendimento do sistema como um todo, aplicando conceitos avançados de programação Python.

## ✨ Funcionalidades

### 🔹 Operações Bancárias
- **💰 Depósito**: Adicionar valores à conta com validação
- **💸 Saque**: Retirar valores com limites diários e por transação
- **📄 Extrato**: Visualizar histórico de transações com formatação brasileira

### 🔹 Gestão de Clientes
- **👤 Criar Cliente**: Cadastro com validações robustas
- **👥 Listar Clientes**: Visualizar todos os clientes cadastrados
- **🗑️ Remover Cliente**: Exclusão segura com confirmação

### 🔹 Gestão de Contas
- **💳 Criar Conta**: Vinculação de contas a clientes existentes
- **📋 Listar Contas**: Overview de todas as contas do sistema
- **❌ Remover Conta**: Remoção segura de contas zeradas

## 🚀 Tecnologias Utilizadas

- **Python 3.10+** (Match/Case statements)
- **Regex** (Validação de CPF)
- **OS Module** (Clear screen multiplataforma)
- **Datetime** (Manipulação de datas)
- **Conventional Commits** (Padronização de commits)

## 🎯 Conceitos Python Aplicados

### 📌 Tipos de Argumentos de Função

```python
# Argumentos apenas posicionais (/)
def deposit(balance, amount, statement, /):
    """Função de depósito com argumentos posicionais"""
    
# Argumentos apenas por palavra-chave (*)
def withdraw(*, balance, amount, statement, limit, withdrawal_count, withdrawal_limit):
    """Função de saque com argumentos nomeados"""
    
# Argumentos mistos (posicionais + nomeados)
def statement_display(balance, /, *, statement):
    """Função de extrato com argumentos híbridos"""
```

### 📌 Outras Características Técnicas

- **🔧 Configuração Centralizada**: Constantes em dicionários CONFIG
- **💬 Mensagens Padronizadas**: Sistema de mensagens centralizadas
- **🎨 Interface Amigável**: Menu formatado com bordas e emojis
- **💰 Formatação Brasileira**: Valores monetários no padrão nacional (R$ 1.500,00)
- **🛡️ Validações Robustas**: CPF, nome completo e dados obrigatórios
- **⚠️ Tratamento de Exceções**: KeyboardInterrupt e ValueError
- **🧪 Dados Mock**: Sistema pré-carregado para testes

## 🏗️ Estrutura do Projeto

```
desafio_sistema_bancario_funcoes_python/
│
├── main.py              # Sistema bancário completo
├── README.md            # Este arquivo
└── .git/                # Controle de versão Git
```

## 🔧 Como Executar

### Pré-requisitos
- Python 3.10+ instalado
- Git (opcional, para clonagem)

### Passos

1. **Clone o repositório:**
```bash
git clone https://github.com/paulobof/desafio_sistema_bancario_funcoes_python-.git
cd desafio_sistema_bancario_funcoes_python-
```

2. **Execute o sistema:**
```bash
python3 main.py
```

3. **Navegue pelo menu:**
```
┌─────────────────────────────────┐
│       🏦 SISTEMA BANCÁRIO       │
├─────────────────────────────────┤
│ OPERAÇÕES                       │
│ [D] 💰 Depositar                │
│ [S] 💸 Sacar                    │
│ [E] 📄 Extrato                  │
├─────────────────────────────────┤
│ CLIENTES                        │
│ [C] 👤 Criar Cliente            │
│ [L] 👥 Listar Clientes          │
│ [R] 🗑️  Remover Cliente         │
├─────────────────────────────────┤
│ CONTAS                          │
│ [B] 💳 Criar Conta              │
│ [M] 📋 Listar Contas            │
│ [O] ❌ Remover Conta            │
├─────────────────────────────────┤
│ [Q] 🚪 Sair                     │
└─────────────────────────────────┘
```

## 📊 Exemplo de Uso

### Extrato Formatado
```
========================================
Movimentações:
Saldo inicial:          R$ 0,00
Depósito:         R$ 2.000,00
Saque:              R$ 500,00
========================================
Saldo atual:        R$ 1.500,00
========================================
```

### Dados Mock Pré-carregados
O sistema vem com **5 clientes** e **4 contas** já cadastrados para facilitar os testes:

- **João Silva Santos**: 2 contas (R$ 1.500,00 e R$ 750,00)
- **Maria Oliveira Costa**: 1 conta (R$ 3.200,50)  
- **Pedro Souza Lima**: 1 conta (R$ 0,00)
- **Ana Carolina Ferreira**: Sem contas
- **Carlos Eduardo Mendes**: Sem contas

## 🛡️ Regras de Negócio

- **💸 Limite de Saque**: R$ 500,00 por transação
- **📊 Limite Diário**: Máximo 3 saques por dia
- **🏦 Agência Padrão**: 0001
- **🔢 CPF**: Deve ter exatamente 11 dígitos numéricos
- **👤 Nome**: Deve ser completo (nome + sobrenome)
- **💳 Remoção de Conta**: Apenas contas com saldo R$ 0,00
- **🗑️ Remoção de Cliente**: Apenas clientes sem contas vinculadas

## 🎓 Aprendizados do Desafio

- ✅ **Refatoração de Código**: Divisão em funções especializadas
- ✅ **Tipos de Argumentos**: Posicionais, nomeados e híbridos  
- ✅ **Boas Práticas**: Separation of Concerns e DRY
- ✅ **Validações**: Entrada de dados robusta
- ✅ **UX/UI**: Interface amigável e intuitiva
- ✅ **Tratamento de Erros**: Exceções e edge cases
- ✅ **Padrões de Código**: Conventional Commits e Clean Code

## 👨‍💻 Autor

**Paulo Bof** - [GitHub](https://github.com/paulobof)

## 📜 Licença

Este projeto é parte de um desafio educacional da **Digital Innovation One (DIO)** e está disponível para fins de aprendizado.

---

⭐ **Se este projeto te ajudou, deixe uma estrela!** ⭐