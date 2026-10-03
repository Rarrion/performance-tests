import locust.stats  # Модуль Locust, отвечающий за сбор и хранение статистики
from pydantic_settings import BaseSettings, SettingsConfigDict

# Импортируем вложенные модели
from tools.config.grpc import GRPCClientConfig
from tools.config.http import HTTPClientConfig
from tools.config.locust import LocustUserConfig

# Настройка списка процентилей, которые будут попадать в отчёты Locust
locust.stats.PERCENTILES_TO_REPORT = [0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99, 1.0]

# Интервал (в секундах) между записями агрегированной статистики в CSV
locust.stats.CSV_STATS_INTERVAL_SEC = 5

# Интервал (в секундах) между записями "исторической" статистики (динамика значений)
locust.stats.HISTORY_STATS_INTERVAL_SEC = 5

# Интервал (в секундах) между обновлением статистики в консоли Locust
locust.stats.CONSOLE_STATS_INTERVAL_SEC = 5

# Интервал (в секундах) между принудительной записью CSV на диск
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 5


class Settings(BaseSettings):
    # Конфигурация загрузки — откуда брать переменные
    model_config = SettingsConfigDict(
        extra="allow",  # Разрешить дополнительные поля (например, неиспользуемые переменные)
        env_file=".env",  # Указываем имя основного .env файла
        env_file_encoding="utf-8",  # Кодировка файла
        env_nested_delimiter="."  # Позволяет использовать вложенные переменные, например: LOCUST_USER.WAIT_TIME_MIN
    )

    # Вложенные секции настроек
    locust_user: LocustUserConfig  # Настройки виртуального пользователя
    gateway_http_client: HTTPClientConfig  # Настройки HTTP-клиента
    gateway_grpc_client: GRPCClientConfig  # Настройки gRPC-клиента


# Глобальный объект настроек — его можно импортировать в любом месте проекта
settings = Settings()
