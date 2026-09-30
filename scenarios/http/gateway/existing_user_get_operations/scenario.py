from locust import task, events
from locust.env import Environment

from clients.http.gateway.locust import GatewayHTTPTaskSet
from seeds.scenarios.existing_user_get_operations import ExistingUserGetOperationsSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


@events.init.add_listener
def init(environment: Environment, **kwargs):
    """
    Хук инициализации Locust — вызывается один раз до старта виртуальных пользователей.

    Выполняем сидинг: создаём пользователей с кредитным счётом и историей операций,
    сохраняем результат в JSON-файл, затем загружаем его в environment.seeds,
    чтобы данные были доступны всем виртуальным пользователям.
    """
    seeds_scenario = ExistingUserGetOperationsSeedsScenario()
    seeds_scenario.build()  # Генерируем данные и сохраняем их в ./dumps

    environment.seeds = seeds_scenario.load()  # Загружаем результат сидинга в окружение Locust


class GetOperationsTaskSet(GatewayHTTPTaskSet):
    """
    Нагрузочный сценарий получения операций существующим пользователем.

    Существующий пользователь (из сидинга) в произвольном порядке, с учётом весов:
    1. Получает список своих счетов.
    2. Получает список операций по кредитному счёту.
    3. Получает статистику по операциям кредитного счёта.

    Использует базовый GatewayHTTPTaskSet и уже созданных в нём API клиентов.
    """

    # Shared state — пользователь из сидинга, от имени которого выполняются запросы
    seed_user: SeedUserResult

    def on_start(self) -> None:
        """
        Инициализируем API клиентов (родительский on_start) и выбираем
        случайного пользователя из подготовленных сидингом данных.
        """
        super().on_start()

        self.seed_user = self.user.environment.seeds.get_random_user()

    @task(1)
    def get_accounts(self):
        """
        Получаем список счетов пользователя — обычно один раз при входе в приложение.
        """
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(3)
    def get_operations(self):
        """
        Получаем список операций по счёту — пользователь несколько раз обновляет
        историю операций, чтобы убедиться, что платёж прошёл.
        """
        self.operations_gateway_client.get_operations(
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )

    @task(2)
    def get_operations_summary(self):
        """
        Получаем статистику по операциям — пользователь может неоднократно
        открывать или обновлять вкладку со статистикой расходов.
        """
        self.operations_gateway_client.get_operations_summary(
            account_id=self.seed_user.credit_card_accounts[0].account_id
        )


class GetOperationsScenarioUser(LocustBaseUser):
    """
    Виртуальный пользователь Locust, исполняющий сценарий получения операций
    существующим пользователем.
    """
    tasks = [GetOperationsTaskSet]
