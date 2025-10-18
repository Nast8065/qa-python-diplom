import pytest
from unittest.mock import patch
from praktikum.database import Database
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestDatabase:

    def test_available_buns_returns_list(self):
        db = Database()
        buns = db.available_buns()
        assert isinstance(buns, list)
        assert len(buns) == 3  # black bun, white bun, red bun

    def test_available_ingredients_returns_list(self):
        db = Database()
        ingredients = db.available_ingredients()
        assert isinstance(ingredients, list)
        assert len(ingredients) == 6  # 3 sauces + 3 fillings

    def test_buns_have_name_and_price(self):
        db = Database()
        buns = db.available_buns()

        for bun in buns:
            # Проверяем, что объект является экземпляром Bun
            assert isinstance(bun, Bun)
            # Проверяем, что методы возвращают значения правильного типа
            name = bun.get_name()
            price = bun.get_price()
            assert isinstance(name, str)
            assert isinstance(price, (int, float))
            assert len(name) > 0
            assert price >= 0

    def test_ingredients_have_type_name_and_price(self):
        db = Database()
        ingredients = db.available_ingredients()

        for ingredient in ingredients:
            # Проверяем, что объект является экземпляром Ingredient
            assert isinstance(ingredient, Ingredient)
            # Проверяем, что методы возвращают значения правильного типа
            ingredient_type = ingredient.get_type()
            name = ingredient.get_name()
            price = ingredient.get_price()

            assert isinstance(ingredient_type, str)
            assert ingredient_type in [INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING]
            assert isinstance(name, str)
            assert isinstance(price, (int, float))
            assert len(name) > 0
            assert price >= 0

    def test_database_contains_correct_buns(self):
        db = Database()
        buns = db.available_buns()
        bun_names = [bun.get_name() for bun in buns]
        bun_prices = [bun.get_price() for bun in buns]

        expected_buns = [
            ("black bun", 100),
            ("white bun", 200),
            ("red bun", 300)
        ]

        for expected_name, expected_price in expected_buns:
            assert expected_name in bun_names
            # Находим бун с нужным именем и проверяем цену
            for i, name in enumerate(bun_names):
                if name == expected_name:
                    assert bun_prices[i] == expected_price

    def test_database_contains_correct_ingredients(self):
        db = Database()
        ingredients = db.available_ingredients()

        expected_ingredients = [
            (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
            (INGREDIENT_TYPE_SAUCE, "sour cream", 200),
            (INGREDIENT_TYPE_SAUCE, "chili sauce", 300),
            (INGREDIENT_TYPE_FILLING, "cutlet", 100),
            (INGREDIENT_TYPE_FILLING, "dinosaur", 200),
            (INGREDIENT_TYPE_FILLING, "sausage", 300)
        ]

        for expected_type, expected_name, expected_price in expected_ingredients:
            found = False
            for ingredient in ingredients:
                if (ingredient.get_type() == expected_type and
                    ingredient.get_name() == expected_name and
                    ingredient.get_price() == expected_price):
                    found = True
                    break
            assert found, f"Не найден ингредиент: {expected_type}, {expected_name}, {expected_price}"

    def test_database_contains_sauces_and_fillings(self):
        db = Database()
        ingredients = db.available_ingredients()

        sauce_count = 0
        filling_count = 0

        for ingredient in ingredients:
            if ingredient.get_type() == INGREDIENT_TYPE_SAUCE:
                sauce_count += 1
            elif ingredient.get_type() == INGREDIENT_TYPE_FILLING:
                filling_count += 1

        assert sauce_count == 3, f"Ожидалось 3 соуса, но найдено {sauce_count}"
        assert filling_count == 3, f"Ожидалось 3 начинки, но найдено {filling_count}"
