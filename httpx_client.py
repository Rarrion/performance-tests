import time

import httpx

# Инициализируем клиент с base_url, timeout и авторизационными заголовками
client = httpx.Client(
    base_url="http://localhost:8003",
    timeout=100,  # Таймаут в секундах
    headers={"Authorization": "Bearer ..."}
)

payload = {
    "email": f"user.{time.time()}@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string",
    "phoneNumber": "string"
}

# Выполняем POST-запрос, используя относительный путь
response = client.post("/api/v1/users", json=payload)

# Выводим ответ в консоль
print(response.text)
