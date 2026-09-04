# performance-tests

Учебный проект по курсу «Нагрузочное тестирование на Python. Расширенный».

## Структура

- `main.py` — проверочный скрипт из урока по настройке PyCharm.
- `docker_example.py`, `Dockerfile.example` — практика по Docker.
- `docker_compose_example.py`, `Dockerfile.compose-example`, `docker-compose.example.yaml` — практика по Docker Compose.

## Запуск примеров

```bash
# Docker
docker build -f Dockerfile.example -t docker-example .
docker run docker-example

# Docker Compose
docker compose -f docker-compose.example.yaml up
```
