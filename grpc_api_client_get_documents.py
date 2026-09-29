"""
Сценарий получения документов по счету через gRPC API-клиенты:
создание пользователя, открытие кредитного счета, получение документов тарифа и контракта.
"""

# Импортируем фабричные функции для создания API-клиентов
from clients.grpc.gateway.accounts.client import build_accounts_gateway_grpc_client
from clients.grpc.gateway.documents.client import build_documents_gateway_grpc_client
from clients.grpc.gateway.users.client import build_users_gateway_grpc_client

# Создаём API-клиенты для работы с сервисами Users, Accounts и Documents
users_gateway_client = build_users_gateway_grpc_client()
accounts_gateway_client = build_accounts_gateway_grpc_client()
documents_gateway_client = build_documents_gateway_grpc_client()

# Шаг 1. Создаём пользователя
create_user_response = users_gateway_client.create_user()
print('Create user response:', create_user_response)

# Шаг 2. Открываем кредитный счёт для только что созданного пользователя
open_credit_card_account_response = accounts_gateway_client.open_credit_card_account(
    user_id=create_user_response.user.id
)
print('Open credit card account response:', open_credit_card_account_response)

# Шаг 3. Получаем документ тарифа по открытому счёту
get_tariff_document_response = documents_gateway_client.get_tariff_document(
    account_id=open_credit_card_account_response.account.id
)
print('Get tariff document response:', get_tariff_document_response)

# Шаг 4. Получаем документ контракта по открытому счёту
get_contract_document_response = documents_gateway_client.get_contract_document(
    account_id=open_credit_card_account_response.account.id
)
print('Get contract document response:', get_contract_document_response)
