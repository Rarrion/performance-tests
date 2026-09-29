from typing import TypedDict

from httpx import Response, QueryParams

from clients.http.client import HTTPClient
from clients.http.gateway.client import build_gateway_http_client


class OperationDict(TypedDict):
    """
    Описание структуры операции.
    """
    id: str
    type: str
    status: str
    amount: float
    cardId: str
    category: str
    createdAt: str
    accountId: str


class OperationReceiptDict(TypedDict):
    """
    Описание структуры чека по операции.
    """
    url: str
    document: str


class OperationsSummaryDict(TypedDict):
    """
    Описание структуры статистики по операциям.
    """
    spentAmount: float
    receivedAmount: float
    cashbackAmount: float


class GetOperationResponseDict(TypedDict):
    """
    Описание структуры ответа получения операции.
    """
    operation: OperationDict


class GetOperationReceiptResponseDict(TypedDict):
    """
    Описание структуры ответа получения чека по операции.
    """
    receipt: OperationReceiptDict


class GetOperationsQueryDict(TypedDict):
    """
    Структура данных для получения списка операций по счету.
    """
    accountId: str


class GetOperationsResponseDict(TypedDict):
    """
    Описание структуры ответа получения списка операций.
    """
    operations: list[OperationDict]


class GetOperationsSummaryQueryDict(TypedDict):
    """
    Структура данных для получения статистики по операциям счета.
    """
    accountId: str


class GetOperationsSummaryResponseDict(TypedDict):
    """
    Описание структуры ответа получения статистики по операциям.
    """
    summary: OperationsSummaryDict


class MakeOperationRequestDict(TypedDict):
    """
    Базовая структура данных для создания операции.
    """
    status: str
    amount: float
    cardId: str
    accountId: str


class MakeFeeOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для создания операции комиссии.
    """


class MakeFeeOperationResponseDict(TypedDict):
    """
    Описание структуры ответа создания операции комиссии.
    """
    operation: OperationDict


class MakeTopUpOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для создания операции пополнения.
    """


class MakeTopUpOperationResponseDict(TypedDict):
    """
    Описание структуры ответа создания операции пополнения.
    """
    operation: OperationDict


class MakeCashbackOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для создания операции кэшбэка.
    """


class MakeCashbackOperationResponseDict(TypedDict):
    """
    Описание структуры ответа создания операции кэшбэка.
    """
    operation: OperationDict


class MakeTransferOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для создания операции перевода.
    """


class MakeTransferOperationResponseDict(TypedDict):
    """
    Описание структуры ответа создания операции перевода.
    """
    operation: OperationDict


class MakePurchaseOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для создания операции покупки.
    """
    category: str


class MakePurchaseOperationResponseDict(TypedDict):
    """
    Описание структуры ответа создания операции покупки.
    """
    operation: OperationDict


class MakeBillPaymentOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для создания операции оплаты по счету.
    """


class MakeBillPaymentOperationResponseDict(TypedDict):
    """
    Описание структуры ответа создания операции оплаты по счету.
    """
    operation: OperationDict


class MakeCashWithdrawalOperationRequestDict(MakeOperationRequestDict):
    """
    Структура данных для создания операции снятия наличных денег.
    """


class MakeCashWithdrawalOperationResponseDict(TypedDict):
    """
    Описание структуры ответа создания операции снятия наличных денег.
    """
    operation: OperationDict


class OperationsGatewayHTTPClient(HTTPClient):
    """
    Клиент для взаимодействия с /api/v1/operations сервиса http-gateway.
    """

    def get_operation_api(self, operation_id: str) -> Response:
        """
        Выполняет GET-запрос на получение информации об операции.

        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/operations/{operation_id}")

    def get_operation_receipt_api(self, operation_id: str) -> Response:
        """
        Выполняет GET-запрос на получение чека по операции.

        :param operation_id: Идентификатор операции.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get(f"/api/v1/operations/operation-receipt/{operation_id}")

    def get_operations_api(self, query: GetOperationsQueryDict) -> Response:
        """
        Выполняет GET-запрос на получение списка операций по счету.

        :param query: Словарь с параметрами запроса, например: {'accountId': '123'}.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get("/api/v1/operations", params=QueryParams(**query))

    def get_operations_summary_api(self, query: GetOperationsSummaryQueryDict) -> Response:
        """
        Выполняет GET-запрос на получение статистики по операциям счета.

        :param query: Словарь с параметрами запроса, например: {'accountId': '123'}.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.get("/api/v1/operations/operations-summary", params=QueryParams(**query))

    def make_fee_operation_api(self, request: MakeFeeOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос на создание операции комиссии.

        :param request: Словарь со статусом, суммой, cardId и accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-fee-operation", json=request)

    def make_top_up_operation_api(self, request: MakeTopUpOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос на создание операции пополнения.

        :param request: Словарь со статусом, суммой, cardId и accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-top-up-operation", json=request)

    def make_cashback_operation_api(self, request: MakeCashbackOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос на создание операции кэшбэка.

        :param request: Словарь со статусом, суммой, cardId и accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-cashback-operation", json=request)

    def make_transfer_operation_api(self, request: MakeTransferOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос на создание операции перевода.

        :param request: Словарь со статусом, суммой, cardId и accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-transfer-operation", json=request)

    def make_purchase_operation_api(self, request: MakePurchaseOperationRequestDict) -> Response:
        """
        Выполняет POST-запрос на создание операции покупки.

        :param request: Словарь со статусом, суммой, категорией, cardId и accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-purchase-operation", json=request)

    def make_bill_payment_operation_api(
            self, request: MakeBillPaymentOperationRequestDict
    ) -> Response:
        """
        Выполняет POST-запрос на создание операции оплаты по счету.

        :param request: Словарь со статусом, суммой, cardId и accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-bill-payment-operation", json=request)

    def make_cash_withdrawal_operation_api(
            self, request: MakeCashWithdrawalOperationRequestDict
    ) -> Response:
        """
        Выполняет POST-запрос на создание операции снятия наличных денег.

        :param request: Словарь со статусом, суммой, cardId и accountId.
        :return: Ответ от сервера (объект httpx.Response).
        """
        return self.post("/api/v1/operations/make-cash-withdrawal-operation", json=request)

    def get_operation(self, operation_id: str) -> GetOperationResponseDict:
        """
        Получить информацию об операции и вернуть распарсенный JSON-ответ.

        :param operation_id: Идентификатор операции.
        :return: Словарь с данными операции.
        """
        response = self.get_operation_api(operation_id)
        return response.json()

    def get_operation_receipt(self, operation_id: str) -> GetOperationReceiptResponseDict:
        """
        Получить чек по операции и вернуть распарсенный JSON-ответ.

        :param operation_id: Идентификатор операции.
        :return: Словарь с данными чека по операции.
        """
        response = self.get_operation_receipt_api(operation_id)
        return response.json()

    def get_operations(self, account_id: str) -> GetOperationsResponseDict:
        """
        Получить список операций по счету и вернуть распарсенный JSON-ответ.

        :param account_id: Идентификатор счета.
        :return: Словарь со списком операций.
        """
        query = GetOperationsQueryDict(accountId=account_id)
        response = self.get_operations_api(query)
        return response.json()

    def get_operations_summary(self, account_id: str) -> GetOperationsSummaryResponseDict:
        """
        Получить статистику по операциям счета и вернуть распарсенный JSON-ответ.

        :param account_id: Идентификатор счета.
        :return: Словарь со статистикой по операциям.
        """
        query = GetOperationsSummaryQueryDict(accountId=account_id)
        response = self.get_operations_summary_api(query)
        return response.json()

    def make_fee_operation(self, card_id: str, account_id: str) -> MakeFeeOperationResponseDict:
        """
        Создать операцию комиссии и вернуть распарсенный JSON-ответ.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с данными созданной операции.
        """
        request = MakeFeeOperationRequestDict(
            status="COMPLETED",
            amount=55.77,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_fee_operation_api(request)
        return response.json()

    def make_top_up_operation(
            self, card_id: str, account_id: str
    ) -> MakeTopUpOperationResponseDict:
        """
        Создать операцию пополнения и вернуть распарсенный JSON-ответ.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с данными созданной операции.
        """
        request = MakeTopUpOperationRequestDict(
            status="COMPLETED",
            amount=1500.11,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_top_up_operation_api(request)
        return response.json()

    def make_cashback_operation(
            self, card_id: str, account_id: str
    ) -> MakeCashbackOperationResponseDict:
        """
        Создать операцию кэшбэка и вернуть распарсенный JSON-ответ.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с данными созданной операции.
        """
        request = MakeCashbackOperationRequestDict(
            status="COMPLETED",
            amount=25.5,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_cashback_operation_api(request)
        return response.json()

    def make_transfer_operation(
            self, card_id: str, account_id: str
    ) -> MakeTransferOperationResponseDict:
        """
        Создать операцию перевода и вернуть распарсенный JSON-ответ.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с данными созданной операции.
        """
        request = MakeTransferOperationRequestDict(
            status="COMPLETED",
            amount=300.99,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_transfer_operation_api(request)
        return response.json()

    def make_purchase_operation(
            self, card_id: str, account_id: str
    ) -> MakePurchaseOperationResponseDict:
        """
        Создать операцию покупки и вернуть распарсенный JSON-ответ.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с данными созданной операции.
        """
        request = MakePurchaseOperationRequestDict(
            status="COMPLETED",
            amount=77.99,
            cardId=card_id,
            accountId=account_id,
            category="taxi"
        )
        response = self.make_purchase_operation_api(request)
        return response.json()

    def make_bill_payment_operation(
            self, card_id: str, account_id: str
    ) -> MakeBillPaymentOperationResponseDict:
        """
        Создать операцию оплаты по счету и вернуть распарсенный JSON-ответ.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с данными созданной операции.
        """
        request = MakeBillPaymentOperationRequestDict(
            status="COMPLETED",
            amount=100.0,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_bill_payment_operation_api(request)
        return response.json()

    def make_cash_withdrawal_operation(
            self, card_id: str, account_id: str
    ) -> MakeCashWithdrawalOperationResponseDict:
        """
        Создать операцию снятия наличных денег и вернуть распарсенный JSON-ответ.

        :param card_id: Идентификатор карты.
        :param account_id: Идентификатор счета.
        :return: Словарь с данными созданной операции.
        """
        request = MakeCashWithdrawalOperationRequestDict(
            status="COMPLETED",
            amount=500.0,
            cardId=card_id,
            accountId=account_id
        )
        response = self.make_cash_withdrawal_operation_api(request)
        return response.json()


def build_operations_gateway_http_client() -> OperationsGatewayHTTPClient:
    """
    Функция создаёт экземпляр OperationsGatewayHTTPClient с уже настроенным HTTP-клиентом.

    :return: Готовый к использованию OperationsGatewayHTTPClient.
    """
    return OperationsGatewayHTTPClient(client=build_gateway_http_client())
