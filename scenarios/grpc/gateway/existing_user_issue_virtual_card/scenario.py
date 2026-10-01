from locust import task, events
from locust.env import Environment

from clients.grpc.gateway.locust import GatewayGRPCTaskSet
from seeds.scenarios.existing_user_issue_virtual_card import ExistingUserIssueVirtualCardSeedsScenario
from seeds.schema.result import SeedUserResult
from tools.locust.user import LocustBaseUser


@events.init.add_listener
def init(environment: Environment, **kwargs):
    """
    Хук инициализации Locust — вызывается один раз до старта виртуальных пользователей.

    Выполняем сидинг: создаём пользователей с дебетовым счётом,
    затем загружаем результат в environment.seeds, чтобы данные были доступны
    всем виртуальным пользователям.
    """
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()  # Генерируем данные через gRPC-сидинг

    environment.seeds = seeds_scenario.load()  # Загружаем результат сидинга в окружение Locust


class IssueVirtualCardTaskSet(GatewayGRPCTaskSet):
    """
    Нагрузочный сценарий выпуска виртуальной карты существующим пользователем через grpc-gateway.

    Существующий пользователь (из сидинга) в произвольном порядке, с учётом весов:
    1. Получает список своих счетов (в ответе есть и карты, привязанные к счёту).
    2. Выпускает новую виртуальную карту к своему дебетовому счёту.

    Использует базовый GatewayGRPCTaskSet и уже созданных в нём gRPC API клиентов.
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

    @task(3)
    def get_accounts(self):
        """
        Получаем список счетов пользователя. Это базовое действие при входе в приложение,
        и после выпуска карты пользователь повторно запрашивает список счетов,
        чтобы убедиться, что новая карта появилась.
        """
        self.accounts_gateway_client.get_accounts(user_id=self.seed_user.user_id)

    @task(1)
    def issue_virtual_card(self):
        """
        Выпускаем новую виртуальную карту к дебетовому счёту пользователя.
        Выпуск карты — редкое действие, поэтому у задачи минимальный вес.
        """
        self.cards_gateway_client.issue_virtual_card(
            user_id=self.seed_user.user_id,
            account_id=self.seed_user.debit_card_accounts[0].account_id
        )


class IssueVirtualCardScenarioUser(LocustBaseUser):
    """
    Виртуальный пользователь Locust, исполняющий сценарий выпуска виртуальной карты
    существующим пользователем.
    """
    tasks = [IssueVirtualCardTaskSet]
