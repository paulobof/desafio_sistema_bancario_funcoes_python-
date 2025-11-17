import re
import os
from datetime import datetime

CONFIG = {
    'MAX_DAILY_WITHDRAWALS': 3,
    'MAX_WITHDRAWAL_AMOUNT': 500.0,
    'AGENCY': "0001",
    'MIN_CPF_LENGTH': 11,
    'MAX_CPF_LENGTH': 11
}

MESSAGES = {
    'ACCOUNT_NOT_FOUND': "❌ Conta não encontrada!",
    'CLIENT_NOT_FOUND': "❌ Cliente não encontrado!",
    'INVALID_VALUE': "❌ Valor inválido!",
    'OPERATION_SUCCESS': "✅ Operação realizada com sucesso!",
    'OPERATION_CANCELLED': "❌ Operação cancelada pelo usuário!",
    'INVALID_NUMBER': "❌ Valor deve ser um número válido!",
    'ADDRESS_REQUIRED': "❌ Endereço é obrigatório!",
    'NAME_REQUIRED': "❌ Nome é obrigatório!",
    'BIRTH_DATE_REQUIRED': "❌ Data de nascimento é obrigatória!",
    'CPF_REQUIRED': "❌ CPF é obrigatório!",
    'ACCOUNT_NUMBER_REQUIRED': "❌ Número da conta é obrigatório!"
}

INITIAL_DAILY_WITHDRAWAL_LIMIT = CONFIG['MAX_DAILY_WITHDRAWALS']
INITIAL_DAILY_WITHDRAWAL_AMOUNT = CONFIG['MAX_WITHDRAWAL_AMOUNT']
AGENCY = CONFIG['AGENCY']

clients = [] 
accounts = []
client_accounts = {}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_cpf(cpf):
    if not cpf.isdigit():
        return False, "❌ CPF deve conter apenas números!"
    
    if len(cpf) != CONFIG['MIN_CPF_LENGTH']:
        return False, "❌ CPF deve ter exatamente 11 dígitos!"
    
    return True, ""

def validate_full_name(name):
    name_parts = name.split()
    if len(name_parts) < 2:
        return False, "❌ Digite o nome completo (nome e sobrenome)!"
    return True, ""

def format_currency(value):
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def create_mock_data():
    global clients, accounts, client_accounts
    
    mock_clients = [
        {
            'name': 'João Silva Santos',
            'birth_date': '15/03/1985',
            'cpf': '12345678901',
            'address': 'Rua das Flores - 123 - Centro - São Paulo/SP'
        },
        {
            'name': 'Maria Oliveira Costa',
            'birth_date': '22/07/1990',
            'cpf': '98765432109',
            'address': 'Avenida Brasil - 456 - Copacabana - Rio de Janeiro/RJ'
        },
        {
            'name': 'Pedro Souza Lima',
            'birth_date': '08/12/1978',
            'cpf': '11122233344',
            'address': 'Praça da Liberdade - 789 - Centro - Belo Horizonte/MG'
        },
        {
            'name': 'Ana Carolina Ferreira',
            'birth_date': '03/05/1992',
            'cpf': '55566677788',
            'address': 'Rua das Palmeiras - 321 - Jardins - Brasília/DF'
        },
        {
            'name': 'Carlos Eduardo Mendes',
            'birth_date': '10/11/1980',
            'cpf': '99988877766',
            'address': 'Alameda dos Anjos - 654 - Boa Viagem - Recife/PE'
        }
    ]

    clients.extend(mock_clients)

    for client in mock_clients:
        client_accounts[client['cpf']] = []

    mock_accounts = [
        {
            'agency': AGENCY,
            'account_number': '1',
            'client_cpf': '12345678901',
            'client_name': 'João Silva Santos',
            'balance': 1500.00,
            'statement': 'Saldo inicial: R$ 0,00\nDepósito: R$ 2.000,00\nSaque: R$ 500,00\n'
        },
        {
            'agency': AGENCY,
            'account_number': '2',
            'client_cpf': '12345678901',
            'client_name': 'João Silva Santos',
            'balance': 750.00,
            'statement': 'Saldo inicial: R$ 0,00\nDepósito: R$ 1.000,00\nSaque: R$ 250,00\n'
        },
        {
            'agency': AGENCY,
            'account_number': '3',
            'client_cpf': '98765432109',
            'client_name': 'Maria Oliveira Costa',
            'balance': 3200.50,
            'statement': 'Saldo inicial: R$ 0,00\nDepósito: R$ 3.000,00\nDepósito: R$ 200,50\n'
        },
        {
            'agency': AGENCY,
            'account_number': '4',
            'client_cpf': '11122233344',
            'client_name': 'Pedro Souza Lima',
            'balance': 0.00,
            'statement': 'Saldo inicial: R$ 0,00\nDepósito: R$ 500,00\nSaque: R$ 500,00\n'
        }
    ]

    accounts.extend(mock_accounts)

    client_accounts['12345678901'] = ['1', '2']
    client_accounts['98765432109'] = ['3']
    client_accounts['11122233344'] = ['4']

def show_menu():
    menu = """
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
=> """
    return menu

def deposit_operation():
    clear_screen()
    print("\n💰 === DEPÓSITO ===\n")
    
    account = select_account()
    if not account:
        return
    
    try:
        amount = float(input("Valor do depósito: R$ "))
        
        if amount > 0:
            new_balance, new_statement = deposit(
                account['balance'],
                amount,
                account['statement'] 
            )
            
            account['balance'] = new_balance
            account['statement'] = new_statement
            
            print(f"\n✅ Depósito realizado: {format_currency(amount)}")
            print(f"💰 Novo saldo: {format_currency(account['balance'])}")
        else:
            print(MESSAGES['INVALID_VALUE'])
            
    except ValueError:
        print(MESSAGES['INVALID_NUMBER'])
    except KeyboardInterrupt:
        print(f"\n{MESSAGES['OPERATION_CANCELLED']}")
        return

def deposit(balance, amount, statement, /):
    if amount > 0:
        balance += amount
        statement += f"Depósito: {format_currency(amount)}\n"
    else:
        print("❌ Valor inválido! O valor deve ser positivo.")
    
    return balance, statement

def withdraw_operation():
    clear_screen()
    print("💸 === SAQUE ===\n")
    
    account = select_account()
    if not account:
        return
    
    daily_withdrawals = account['statement'].count('Saque:')
    
    try:
        amount = float(input("Valor do saque: R$ "))
        
        new_balance, new_statement = withdraw(
            balance=account['balance'],
            amount=amount,
            statement=account['statement'],
            limit=INITIAL_DAILY_WITHDRAWAL_AMOUNT,
            withdrawal_count=daily_withdrawals,
            withdrawal_limit=INITIAL_DAILY_WITHDRAWAL_LIMIT
        )
        
        account['balance'] = new_balance
        account['statement'] = new_statement
        
        if new_statement != account['statement'] or account['statement'].endswith(f"Saque: {format_currency(amount)}\n"):
            print(f"💰 Novo saldo: {format_currency(account['balance'])}")
            
    except ValueError:
        print(MESSAGES['INVALID_NUMBER'])
    except KeyboardInterrupt:
        print(f"\n{MESSAGES['OPERATION_CANCELLED']}")
        return
  
def show_statement_operation():
    clear_screen()    
    print("\n📄 === EXTRATO ===\n")
    
    account = select_account()
    if not account:
        return
    
    print(f"\n🏦 Agência: {account['agency']} | Conta: {account['account_number']}")
    print(f"👤 Cliente: {account['client_name']}\n")

    statement_display(
        account['balance'],
        statement=account['statement']
    )

def withdraw(*, balance, amount, statement, limit, withdrawal_count, withdrawal_limit):
    if withdrawal_count >= withdrawal_limit:
        print(f"🚫 Limite diário excedido! Máximo: {withdrawal_limit} saques.")
        return balance, statement
    
    if amount > balance:
        print("❌ Saldo insuficiente!")
    elif amount > limit:
        print(f"❌ Limite por saque: {format_currency(limit)}")
    elif amount > 0:
        balance -= amount
        statement += f"Saque: {format_currency(amount)}\n"
        print(f"✅ Saque realizado: {format_currency(amount)}")
    else:
        print("❌ Valor inválido!")
    
    return balance, statement

def statement_display(balance, /, *, statement):
    print("=" * 40)
    
    if not statement:
        print("Nenhuma movimentação.")
    else:
        print("Movimentações:")
        
        lines = statement.strip().split('\n')
        for line in lines:
            if line.strip():
                if ':' in line:
                    operation, value = line.split(':', 1)
                    operation = operation.strip()
                    value = value.strip()
                    
                    if value.startswith('R$'):
                        try:
                            numeric_value = float(value.replace('R$', '').strip())
                            value = format_currency(numeric_value)
                        except ValueError:
                            pass
                    
                    print(f"{operation + ':': <25} {value: >15}")
                else:
                    print(line)
    
    print("=" * 40)
    print(f"{'Saldo atual:': <25} {format_currency(balance): >15}")
    print("=" * 40)

def create_client_operation():
    print("\n👤 === CRIAR CLIENTE ===\n")
    
    try:
        name = input("Nome completo: ").strip()
        if not name:
            print("❌ Nome é obrigatório!")
            return
        
        valid, message = validate_full_name(name)
        if not valid:
            print(message)
            return
        
        birth_date = input("Data de nascimento (DD/MM/AAAA): ").strip()
        if not birth_date:
            print("❌ Data de nascimento é obrigatória!")
            return
        
        cpf = input("CPF (apenas números): ").strip()
        cpf = re.sub(r'\D', '', cpf)
        
        valid, message = validate_cpf(cpf)
        if not valid:
            print(message)
            return
        
        print("Endereço (formato: logradouro - nro - bairro - cidade/sigla_estado)")
        address = input("Endereço completo: ").strip()
        if not address:
            print(MESSAGES['ADDRESS_REQUIRED'])
            return
        
        create_client(name, birth_date, cpf, address)
        
    except KeyboardInterrupt:
        print(f"\n{MESSAGES['OPERATION_CANCELLED']}")
        return

def create_client(name, birth_date, cpf, address): 
    for client in clients:
        if client['cpf'] == cpf:
            print("❌ Já existe cliente com este CPF!")
            return

    new_client = {
        'name': name,
        'birth_date': birth_date,
        'cpf': cpf,
        'address': address
    }
    
    clients.append(new_client)
    
    client_accounts[cpf] = []
    
    print(f"✅ Cliente {name} criado com sucesso!")

def list_clients_operation():
    print("\n👥 === LISTA DE CLIENTES ===\n")
    
    if not clients:
        print("❌ Nenhum cliente cadastrado!")
        return
    
    for i, client in enumerate(clients, 1):
        print(f"\n{i}. {client['name']}")
        print(f"   📅 Nascimento: {client['birth_date']}")
        print(f"   🆔 CPF: {client['cpf']}")
        print(f"   📍 Endereço: {client['address']}")
        
        num_accounts = len(client_accounts.get(client['cpf'], []))
        if num_accounts > 0:
            print(f"   💳 Contas: {num_accounts}")
        else:
            print(f"   💳 Contas: Nenhuma")
    
    print(f"\n📊 Total: {len(clients)} cliente(s) cadastrado(s)")
    print("=" * 30)

def remove_client_operation():
    print("\n🗑️ === REMOVER CLIENTE ===\n")
    
    if not clients:
        print("❌ Nenhum cliente cadastrado!")
        return
    
    cpf = input("CPF (apenas números): ").strip()
    cpf = re.sub(r'\D', '', cpf)
    
    valid, message = validate_cpf(cpf)
    if not valid:
        print(message)
        return
    
    remove_client(cpf)

def remove_client(cpf):
    client_found = None
    for client in clients:
        if client['cpf'] == cpf:
            client_found = client
            break
    
    if not client_found:
        print("❌ Cliente não encontrado!")
        return False
    
    client_account_list = client_accounts.get(cpf, [])
    if client_account_list:
        print(f"❌ Não é possível remover! Cliente possui {len(client_account_list)} conta(s).")
        print("💡 Remova todas as contas antes de excluir o cliente.")
        return False
    
    print(f"\n⚠️  CONFIRMAÇÃO DE REMOÇÃO")
    print(f"Cliente: {client_found['name']}")
    print(f"CPF: {client_found['cpf']}")
    
    confirm = input("Confirma a remoção? (S/N): ").upper().strip()
    
    if confirm == 'S':
        clients.remove(client_found)
        
        if cpf in client_accounts:
            del client_accounts[cpf]
        
        print(f"✅ Cliente {client_found['name']} removido com sucesso!")
        return True
    else:
        print("❌ Remoção cancelada.")
        return False

def create_account_operation():
    print("\n💳 === CRIAR CONTA ===\n")
    
    if not clients:
        print("❌ Nenhum cliente cadastrado! Crie um cliente primeiro.")
        return
    
    cpf = input("CPF do cliente (apenas números): ").strip()
    cpf = re.sub(r'\D', '', cpf)
    
    client_found = None
    for client in clients:
        if client['cpf'] == cpf:
            client_found = client
            break
    
    if not client_found:
        print("❌ Cliente não encontrado!")
        return
    
    account_number = len(accounts) + 1
    
    create_account(AGENCY, account_number, client_found)

def create_account(agency, account_number, client):
    new_account = {
        'agency': agency,
        'account_number': str(account_number),
        'client_cpf': client['cpf'],
        'client_name': client['name'],
        'balance': 0.0,
        'statement': "Saldo inicial: R$ 0,00\n"
    }
    
    accounts.append(new_account)
    
    client_accounts[client['cpf']].append(str(account_number))
    
    print(f"✅ Conta criada com sucesso!")
    print(f"   👤 Cliente: {client['name']}")
    print(f"   🏦 Agência: {agency}")
    print(f"   💳 Conta: {account_number}")

def list_account_operation():
    clear_screen()
    print("💳 === LISTA DE CONTAS ===\n")
    
    if not accounts:
        print("❌ Nenhuma conta cadastrada!")
        return
    
    for i, account in enumerate(accounts, 1):
        print(f"\n{i}. Conta: {account['account_number']}")
        print(f"   🏦 Agência: {account['agency']} ")
        print(f"   👤 Cliente: {account['client_name']}")
        print(f"   🆔 CPF: {account['client_cpf']}")
        print(f"   💰 Saldo: {format_currency(account['balance'])}")
    
    print(f"\n📊 Total: {len(accounts)} conta(s) cadastrada(s)")
    print("=" * 30)

def remove_account_operation():
    print("\n🗑️ === REMOVER CONTA ===\n")
    
    if not accounts:
        print("❌ Nenhuma conta cadastrada!")
        return
    
    account_number = input("Número da conta a remover: ").strip()
    if not account_number:
        print("❌ Número da conta é obrigatório!")
        return
    
    remove_account(account_number)

def remove_account(account_number):
    account_found = None
    account_index = -1
    
    for i, account in enumerate(accounts):
        if account['account_number'] == account_number:
            account_found = account
            account_index = i
            break
    
    if not account_found:
        print("❌ Conta não encontrada!")
        return False
    
    if account_found['balance'] != 0:
        print(f"❌ Não é possível remover! Conta possui saldo: R$ {account_found['balance']:.2f}")
        print("💡 A conta deve estar zerada para ser removida.")
        return False
    
    print(f"\n⚠️  CONFIRMAÇÃO DE REMOÇÃO")
    print(f"Conta: {account_found['account_number']}")
    print(f"Agência: {account_found['agency']}")
    print(f"Cliente: {account_found['client_name']}")
    print(f"Saldo: R$ {account_found['balance']:.2f}")
    
    confirm = input("Confirma a remoção? (S/N): ").upper().strip()
    
    if confirm == 'S':
        accounts.pop(account_index)
        
        client_cpf = account_found['client_cpf']
        if client_cpf in client_accounts:
            client_accounts[client_cpf].remove(account_number)
        
        print(f"✅ Conta {account_number} removida com sucesso!")
        return True
    else:
        print("❌ Remoção cancelada.")
        return False

def select_account():
    if not accounts:
        print("❌ Nenhuma conta cadastrada!")
        return None
    
    account_number = input("Número da conta: ").strip()
    if not account_number:
        print("❌ Número da conta é obrigatório!")
        return None
    
    for account in accounts:
        if account['account_number'] == account_number:
            return account
    
    print(MESSAGES['ACCOUNT_NOT_FOUND'])
    return None

def get_and_validate_cpf(prompt="CPF (apenas números): "):
    cpf = input(prompt).strip()
    cpf = re.sub(r'\D', '', cpf)
    
    valid, message = validate_cpf(cpf)
    if not valid:
        print(message)
        return None
    
    return cpf

def main():
    create_mock_data()
  
    while True:
        clear_screen()
        print("🏦 Bem-vindo ao Sistema Bancário!")

        option = input(show_menu()).upper().strip()
        
        match option:
            case "D":
                deposit_operation()
            case "S":
                withdraw_operation()
            case "E":
                show_statement_operation()
            case "C":
                create_client_operation()
            case "L":
                list_clients_operation()                
            case "R":
                remove_client_operation()
            case "B":
                create_account_operation()
            case "M":
                list_account_operation()                
            case "O":
                remove_account_operation()
            case "Q":
                print("🏦 Obrigado! Volte Sempre! 👋")
                break
            case _:
                print("❌ Opção inválida!")
        
        input("\n📋 Pressione ENTER...")
        
if __name__ == "__main__":
    main()