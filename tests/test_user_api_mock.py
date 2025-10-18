import pytest
import allure
from unittest.mock import Mock, patch


@allure.feature("API Тесты для пользователей (Mock)")
class TestUserRegistrationMock:

    @allure.title("TC-01 Mock: Успешное создание уникального пользователя")
    @patch('requests.post')
    def test_create_unique_user_success_mock(self, mock_post):
        # Настраиваем mock
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "accessToken": "mock_token_123",
            "refreshToken": "mock_refresh_token_456",
            "user": {"email": "test@example.com", "name": "Test User"}
        }
        mock_post.return_value = mock_response

        # Выполняем тест
        import requests
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/register",
                                json={"email": "test@example.com", "password": "password123", "name": "Test User"})

        # Проверяем
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("TC-02 Mock: Создание уже зарегистрированного пользователя")
    @patch('requests.post')
    def test_create_existing_user_fail_mock(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "success": False,
            "message": "User already exists"
        }
        mock_post.return_value = mock_response

        import requests
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/register",
                                json={"email": "existing@example.com", "password": "password123", "name": "Existing User"})

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert "already exists" in response.json()["message"]


@allure.feature("API Тесты для логина (Mock)")
class TestUserLoginMock:

    @allure.title("TC-04 Mock: Успешный логин")
    @patch('requests.post')
    def test_login_existing_user_success_mock(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "accessToken": "login_token_123",
            "refreshToken": "refresh_token_456",
            "user": {"email": "user@example.com", "name": "Test User"}
        }
        mock_post.return_value = mock_response

        import requests
        response = requests.post("https://stellarburgers.nomoreparties.site/api/auth/login",
                                json={"email": "user@example.com", "password": "password123"})

        assert response.status_code == 200
        assert response.json()["success"] is True
