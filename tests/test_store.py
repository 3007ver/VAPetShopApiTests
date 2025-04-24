
import allure
import jsonschema
import pytest
import requests
from .schemas.store_schema import ORDER_SCHEMA, INVENTORY_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3/store"

@allure.feature("Store")
class TestStore:
    @allure.title("Размещение заказа")
    def test_place_an_order(self):
        with allure.step("Подготовка данных для размещения заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }

        with allure.step("Отправка запроса на размещение заказа"):
            response = requests.post(url=f"{BASE_URL}/order", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпадает с ожидаемым"
            jsonschema.validate(response_json, ORDER_SCHEMA)

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == payload['id'], "ID не совпадает с ожидаемым"
            assert response_json['petId'] == payload['petId'], "PetID не совпадает с ожидаемым"
            assert response_json['quantity'] == payload['quantity'], "Количество не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус не совпадает с ожидаемым"
            assert response_json['complete'] == payload['complete'], "Состояние не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID ")
    def test_get_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order['id']

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(url=f"{BASE_URL}/order/{order_id}")
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпадает с ожидаемым"

        with allure.step("Проверка параметров заказа в ответе"):
            assert response_json['id'] == create_order['id'], "ID не совпадает с ожидаемым"
            assert response_json['petId'] == create_order['petId'], "PetID не совпадает с ожидаемым"
            assert response_json['quantity'] == create_order['quantity'], "Количество не совпадает с ожидаемым"
            assert response_json['status'] == create_order['status'], "Статус не совпадает с ожидаемым"
            assert response_json['complete'] == create_order['complete'], "Состояние не совпадает с ожидаемым"

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            order_id = create_order['id']

        with allure.step("Отправка запроса на удаление заказа по ID"):
            response = requests.delete(url=f"{BASE_URL}/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпадает с ожидаемым"

        with allure.step("Отправка запроса на получение информации об удаленном заказе"):
            response = requests.get(f"{BASE_URL}/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "код ответа не совпадает с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_information_about_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step(" Проверка текстового содержимого ответа"):
            assert response.text == "Order not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Отправка запроса на получение инвентаря"):
            response = requests.get(url=f"{BASE_URL}/inventory")
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Код ответа не совпадает с ожидаемым"
            jsonschema.validate(response_json, INVENTORY_SCHEMA)






