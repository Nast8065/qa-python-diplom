import pytest
import requests
import allure
import random
import string
from faker import Faker
from requests.exceptions import ConnectionError, Timeout


class DataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_user_data(self):
        return {
            "email": self.fake.email(),
            "password": self.fake.password(length=10),
            "name": self.fake.first_name()
        }


@pytest.fixture
def base_url():
    return "https://stellarburgers.nomoreparties.site/api"


@pytest.fixture(scope="session")
def api_available(base_url):
    """Проверяет доступность API перед запуском тестов"""
    try:
        response = requests.get(f"{base_url}/ingredients", timeout=5)
        response.raise_for_status()
        return True
    except (ConnectionError, Timeout):
        pytest.skip("API недоступно, пропускаем тесты")
    except Exception:
        pytest.skip("Проблема с API, пропускаем тесты")


@pytest.fixture
def data_generator():
    return DataGenerator()


@pytest.fixture
def user_data(data_generator):
    return data_generator.generate_user_data()


@pytest.fixture
def registered_user(base_url, user_data, api_available):
    """Фикстура для создания и удаления зарегистрированного пользователя"""
    try:
        response = requests.post(f"{base_url}/auth/register", json=user_data, timeout=10)
        response.raise_for_status()
        token = response.json()["accessToken"]

        yield {
            "email": user_data["email"],
            "password": user_data["password"],
            "name": user_data["name"],
            "token": token
        }

        # Удаление пользователя после теста
        headers = {"Authorization": token}
        requests.delete(f"{base_url}/auth/user", headers=headers, timeout=10)

    except (ConnectionError, Timeout) as e:
        pytest.skip(f"API недоступно: {e}")
    except Exception as e:
        pytest.skip(f"Ошибка при создании пользователя: {e}")


@pytest.fixture
def auth_header(registered_user):
    return {"Authorization": registered_user["token"]}


@pytest.fixture
def ingredient_data(base_url, api_available):
    """Фикстура для получения данных об ингредиентах"""
    try:
        response = requests.get(f"{base_url}/ingredients", timeout=10)
        response.raise_for_status()
        ingredients = response.json()["data"]
        return ingredients
    except (ConnectionError, Timeout) as e:
        pytest.skip(f"API недоступно: {e}")
    except Exception as e:
        pytest.skip(f"Ошибка при получении ингредиентов: {e}")
