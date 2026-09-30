from locust import User, between, task

# Импортируем схемы ответов, чтобы типизировать shared state
from clients.http.gateway.locust import GatewayHTTPTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema


class GetAccountsTaskSet(GatewayHTTPTaskSet):
    """
    Нагрузочный сценарий, который в произвольном порядке (с учётом весов задач):
    1. Создаёт нового пользователя.
    2. Открывает депозитный счёт.
    3. Получает список счетов пользователя.

    Использует базовый GatewayHTTPTaskSet и уже созданных в нём API клиентов.
    """

    # Shared state — сохраняем результаты запросов для дальнейшего использования
    create_user_response: CreateUserResponseSchema | None = None

    @task(2)
    def create_user(self):
        """
        Создаём нового пользователя и сохраняем результат для последующих задач.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self):
        """
        Открываем депозитный счёт для созданного пользователя.
        Проверяем, что пользователь уже был создан.
        """
        if not self.create_user_response:
            return  # Если пользователь не был создан, нет смысла продолжать

        self.accounts_gateway_client.open_deposit_account(user_id=self.create_user_response.user.id)

    @task(6)
    def get_accounts(self):
        """
        Получаем список счетов пользователя, если пользователь уже был создан.
        """
        if not self.create_user_response:
            return  # Если пользователь не был создан, запрос счетов невозможен

        self.accounts_gateway_client.get_accounts(user_id=self.create_user_response.user.id)


class GetAccountsScenarioUser(User):
    """
    Пользователь Locust, исполняющий сценарий получения счетов пользователя.
    """
    host = "localhost"
    tasks = [GetAccountsTaskSet]
    wait_time = between(1, 3)  # Имитируем паузы между выполнением задач
