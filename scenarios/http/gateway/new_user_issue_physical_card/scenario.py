from locust import task

# Импортируем схемы ответов, чтобы типизировать shared state
from clients.http.gateway.accounts.schema import OpenDebitCardAccountResponseSchema
from clients.http.gateway.locust import GatewayHTTPSequentialTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema
from tools.locust.user import LocustBaseUser


class IssuePhysicalCardSequentialTaskSet(GatewayHTTPSequentialTaskSet):
    """
    Нагрузочный сценарий выпуска физической карты новым пользователем.

    Шаги выполняются строго последовательно, так как каждый следующий
    зависит от результата предыдущего:
    1. Создание нового пользователя.
    2. Открытие дебетового счёта для этого пользователя.
    3. Выпуск физической карты, привязанной к открытому счёту.

    Использует базовый GatewayHTTPSequentialTaskSet и уже созданных в нём API клиентов.
    """

    # Shared state — сохраняем ответы предыдущих шагов для использования в следующих задачах
    create_user_response: CreateUserResponseSchema | None = None
    open_debit_card_account_response: OpenDebitCardAccountResponseSchema | None = None

    @task
    def create_user(self):
        """
        Шаг 1. Создаём нового пользователя и сохраняем ответ для последующих шагов.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_debit_card_account(self):
        """
        Шаг 2. Открываем дебетовый счёт для созданного пользователя.
        """
        if not self.create_user_response:
            return  # Без созданного пользователя открыть счёт невозможно

        self.open_debit_card_account_response = self.accounts_gateway_client.open_debit_card_account(
            user_id=self.create_user_response.user.id
        )

    @task
    def issue_physical_card(self):
        """
        Шаг 3. Выпускаем физическую карту, привязанную к открытому дебетовому счёту.
        """
        if not self.open_debit_card_account_response:
            return  # Без открытого счёта выпустить карту невозможно

        self.cards_gateway_client.issue_physical_card(
            user_id=self.create_user_response.user.id,
            account_id=self.open_debit_card_account_response.account.id
        )


class IssuePhysicalCardScenarioUser(LocustBaseUser):
    """
    Виртуальный пользователь Locust, исполняющий последовательный сценарий
    выпуска физической карты новым пользователем.
    """
    tasks = [IssuePhysicalCardSequentialTaskSet]
