"""
Pydantic-модели запроса и ответа для эндпоинта POST /api/v1/users (создание пользователя).
"""
import time

import httpx
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSchema(BaseModel):
    """
    Описание структуры пользователя.

    Поля API в camelCase (lastName, firstName, middleName, phoneNumber)
    сопоставляются с полями модели в snake_case через alias.
    """
    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")


class CreateUserRequestSchema(BaseModel):
    """
    Структура данных для создания нового пользователя.

    populate_by_name=True позволяет создавать модель по именам полей (snake_case),
    а model_dump(by_alias=True) отдаёт данные в формате API (camelCase).
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")
    phone_number: str = Field(alias="phoneNumber")


class CreateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа создания пользователя.
    """
    user: UserSchema


if __name__ == "__main__":
    # Проверяем модели на тестовом стенде: отправляем запрос и валидируем ответ
    create_user_request = CreateUserRequestSchema(
        email=f"user.{time.time()}@example.com",
        last_name="string",
        first_name="string",
        middle_name="string",
        phone_number="string"
    )
    print('Create user request:', create_user_request.model_dump(by_alias=True))

    response = httpx.post(
        "http://localhost:8003/api/v1/users",
        json=create_user_request.model_dump(by_alias=True)
    )
    create_user_response = CreateUserResponseSchema.model_validate_json(response.text)
    print('Create user response:', create_user_response)
