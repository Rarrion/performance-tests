from locust import HttpUser, between, task

from tools.fakers import fake  # генератор случайных данных


class OpenDebitCardAccountScenarioUser(HttpUser):
    # Пауза между запросами для каждого виртуального пользователя (в секундах)
    wait_time = between(1, 3)

    # В этой переменной будем хранить ID созданного пользователя
    user_id: str

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы создаем нового пользователя, отправляя POST-запрос к /api/v1/users.
        """
        request = {
            "email": fake.email(),
            "lastName": fake.last_name(),
            "firstName": fake.first_name(),
            "middleName": fake.middle_name(),
            "phoneNumber": fake.phone_number()
        }
        response = self.client.post("/api/v1/users", json=request)

        # Сохраняем ID созданного пользователя из ответа
        self.user_id = response.json()["user"]["id"]

    @task
    def open_debit_card_account(self):
        """
        Основная нагрузочная задача: открытие дебетового счёта.
        Здесь мы выполняем POST-запрос к /api/v1/accounts/open-debit-card-account,
        передавая в теле запроса ID ранее созданного пользователя.
        """
        self.client.post(
            "/api/v1/accounts/open-debit-card-account",
            json={"userId": self.user_id}
        )
