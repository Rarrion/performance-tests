from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, ConfigDict, HttpUrl

from tools.fakers import fake


class OperationType(StrEnum):
    FEE = "FEE"
    TOP_UP = "TOP_UP"
    PURCHASE = "PURCHASE"
    CASHBACK = "CASHBACK"
    TRANSFER = "TRANSFER"
    BILL_PAYMENT = "BILL_PAYMENT"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"


class OperationStatus(StrEnum):
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    UNSPECIFIED = "UNSPECIFIED"


class OperationSchema(BaseModel):
    """
    Описание структуры операции.
    """
    id: str
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: str = Field(alias="cardId")
    category: str
    created_at: datetime = Field(alias="createdAt")
    account_id: str = Field(alias="accountId")


class OperationReceiptSchema(BaseModel):
    """
    Описание структуры чека по операции.
    """
    url: HttpUrl
    document: str


class OperationsSummarySchema(BaseModel):
    """
    Описание структуры статистики по операциям.
    """
    spent_amount: float = Field(alias="spentAmount")
    received_amount: float = Field(alias="receivedAmount")
    cashback_amount: float = Field(alias="cashbackAmount")


class GetOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа получения операции.
    """
    operation: OperationSchema


class GetOperationReceiptResponseSchema(BaseModel):
    """
    Описание структуры ответа получения чека по операции.
    """
    receipt: OperationReceiptSchema


class GetOperationsQuerySchema(BaseModel):
    """
    Структура данных для получения списка операций по счету.
    """
    model_config = ConfigDict(populate_by_name=True)

    account_id: str = Field(alias="accountId")


class GetOperationsResponseSchema(BaseModel):
    """
    Описание структуры ответа получения списка операций.
    """
    operations: list[OperationSchema]


class GetOperationsSummaryQuerySchema(BaseModel):
    """
    Структура данных для получения статистики по операциям счета.
    """
    model_config = ConfigDict(populate_by_name=True)

    account_id: str = Field(alias="accountId")


class GetOperationsSummaryResponseSchema(BaseModel):
    """
    Описание структуры ответа получения статистики по операциям.
    """
    summary: OperationsSummarySchema


class MakeOperationRequestSchema(BaseModel):
    """
    Базовая структура данных для создания операции.
    """
    model_config = ConfigDict(populate_by_name=True)

    status: OperationStatus = Field(default_factory=lambda: fake.enum(OperationStatus))
    amount: float = Field(default_factory=fake.amount)
    card_id: str = Field(alias="cardId")
    account_id: str = Field(alias="accountId")


class MakeFeeOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура данных для создания операции комиссии.
    """


class MakeFeeOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа создания операции комиссии.
    """
    operation: OperationSchema


class MakeTopUpOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура данных для создания операции пополнения.
    """


class MakeTopUpOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа создания операции пополнения.
    """
    operation: OperationSchema


class MakeCashbackOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура данных для создания операции кэшбэка.
    """


class MakeCashbackOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа создания операции кэшбэка.
    """
    operation: OperationSchema


class MakeTransferOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура данных для создания операции перевода.
    """


class MakeTransferOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа создания операции перевода.
    """
    operation: OperationSchema


class MakePurchaseOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура данных для создания операции покупки.
    """
    category: str = Field(default_factory=fake.category)


class MakePurchaseOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа создания операции покупки.
    """
    operation: OperationSchema


class MakeBillPaymentOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура данных для создания операции оплаты по счету.
    """


class MakeBillPaymentOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа создания операции оплаты по счету.
    """
    operation: OperationSchema


class MakeCashWithdrawalOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура данных для создания операции снятия наличных денег.
    """


class MakeCashWithdrawalOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа создания операции снятия наличных денег.
    """
    operation: OperationSchema
