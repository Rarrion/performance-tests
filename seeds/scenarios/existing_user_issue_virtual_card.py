from seeds.scenario import SeedsScenario
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedAccountsPlan


class ExistingUserIssueVirtualCardSeedsScenario(SeedsScenario):
    """
    Сценарий сидинга для существующего пользователя, который выпускает новую виртуальную карту.
    Создаёт 300 пользователей, каждому из которых открывается один дебетовый счёт.
    Виртуальная карта выпускается уже в самом нагрузочном сценарии.
    """

    @property
    def plan(self) -> SeedsPlan:
        """
        План сидинга, который описывает, сколько пользователей нужно создать
        и какие именно данные для них генерировать.
        В данном случае создаём 300 пользователей, каждому открываем один дебетовый счёт.
        """
        return SeedsPlan(
            users=SeedUsersPlan(
                count=300,  # Создаём 300 пользователей
                debit_card_accounts=SeedAccountsPlan(count=1)  # Один дебетовый счёт на пользователя
            ),
        )

    @property
    def scenario(self) -> str:
        """
        Название сценария сидинга, которое будет использоваться для сохранения данных.
        """
        return "existing_user_issue_virtual_card"


if __name__ == '__main__':
    # Если файл запускается напрямую, создаём объект сценария и запускаем его.
    seeds_scenario = ExistingUserIssueVirtualCardSeedsScenario()
    seeds_scenario.build()  # Стартуем процесс сидинга
