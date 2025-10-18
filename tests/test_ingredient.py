import pytest
from praktikum.ingredient import Ingredient
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestIngredient:

    def test_get_price_returns_correct_price(self):
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100.0)
        assert ingredient.get_price() == 100.0

    def test_get_name_returns_correct_name(self):
        ingredient = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 100.0)
        assert ingredient.get_name() == "cutlet"

    def test_get_type_returns_correct_type_sauce(self):
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "sour cream", 200.0)
        assert ingredient.get_type() == INGREDIENT_TYPE_SAUCE

    def test_get_type_returns_correct_type_filling(self):
        ingredient = Ingredient(INGREDIENT_TYPE_FILLING, "dinosaur", 200.0)
        assert ingredient.get_type() == INGREDIENT_TYPE_FILLING

    def test_ingredient_with_minimal_price(self):
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "minimal sauce", 0.01)
        assert ingredient.get_price() == 0.01
