from locust import User, between, task

from clients.grpc.gateway.accounts.client import AccountsGatewayGRPCClient, build_accounts_gateway_locust_grpc_client
from clients.grpc.gateway.users.client import UsersGatewayGRPCClient, build_users_gateway_locust_grpc_client
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse


class OpenDebitCardAccountScenarioUser(User):
    # Атрибут host обязателен для Locust, даже если он не используется напрямую в gRPC.
    host = "localhost"
    # Время ожидания между задачами от 1 до 3 секунд.
    wait_time = between(1, 3)

    # Аннотации для клиентов и ответов
    users_gateway_client: UsersGatewayGRPCClient
    accounts_gateway_client: AccountsGatewayGRPCClient
    create_user_response: CreateUserResponse

    def on_start(self) -> None:
        """
        Метод, вызываемый при старте каждого виртуального пользователя.
        Здесь происходит инициализация gRPC API клиентов и создание пользователя.
        """
        # Инициализируем gRPC-клиенты, пригодные для Locust, с интерцептором метрик.
        self.users_gateway_client = build_users_gateway_locust_grpc_client(self.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_grpc_client(self.environment)

        # Создаём пользователя один раз в начале сессии.
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        """
        Основная задача виртуального пользователя — открытие дебетового счёта.
        Метод будет многократно вызываться Locust-агентами.
        """
        self.accounts_gateway_client.open_debit_card_account(self.create_user_response.user.id)
