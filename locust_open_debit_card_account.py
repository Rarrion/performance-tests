from locust import User, between, task

from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_gateway_locust_http_client
from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_locust_http_client
from clients.http.gateway.users.schema import CreateUserResponseSchema


class OpenDebitCardAccountScenarioUser(User):  # Наследуемся от User вместо HttpUser
    # Обязательное поле, требуемое Locust. Будет проигнорировано, но его нужно указать, иначе будет ошибка запуска.
    host = "localhost"
    # Пауза между запросами для каждого виртуального пользователя (в секундах)
    wait_time = between(1, 3)

    # Поля, в которых будут храниться экземпляры наших API клиентов
    users_gateway_client: UsersGatewayHTTPClient
    accounts_gateway_client: AccountsGatewayHTTPClient
    # Поле, куда мы сохраним ответ после создания пользователя
    create_user_response: CreateUserResponseSchema

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы создаем API клиенты и нового пользователя через UsersGatewayHTTPClient.
        """
        # Создаем API клиенты, встроенные в экосистему Locust (с хуками и поддержкой сбора метрик)
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)
        self.accounts_gateway_client = build_accounts_gateway_locust_http_client(self.environment)

        # Создаем пользователя через API
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        """
        Основная нагрузочная задача: открытие дебетового счёта.
        Здесь мы выполняем POST-запрос к /api/v1/accounts/open-debit-card-account
        через AccountsGatewayHTTPClient, передавая ID ранее созданного пользователя.
        """
        self.accounts_gateway_client.open_debit_card_account(self.create_user_response.user.id)
