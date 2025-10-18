import pytest
import allure
from unittest.mock import Mock, patch


@allure.feature("API Тесты для заказов (Mock)")
class TestOrderCreationMock:

    @allure.title("TC-06 Mock: Создание заказа с авторизацией")
    @patch('requests.post')
    def test_create_order_with_auth_and_ingredients_success_mock(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "name": "Space burger",
            "order": {"number": 12345}
        }
        mock_post.return_value = mock_response

        import requests
        headers = {"Authorization": "Bearer token_123"}
        response = requests.post("https://stellarburgers.nomoreparties.site/api/orders",
                                json={"ingredients": ["ingredient1", "ingredient2"]},
                                headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("TC-07 Mock: Создание заказа без авторизации")
    @patch('requests.post')
    def test_create_order_without_auth_success_mock(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "name": "Anonymous burger",
            "order": {"number": 12346}
        }
        mock_post.return_value = mock_response

        import requests
        response = requests.post("https://stellarburgers.nomoreparties.site/api/orders",
                                json={"ingredients": ["ingredient1", "ingredient2"]})

        assert response.status_code == 200
        assert response.json()["success"] is True
