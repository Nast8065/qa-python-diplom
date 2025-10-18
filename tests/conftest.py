import pytest
from unittest.mock import Mock


@pytest.fixture
def mock_bun():
    bun = Mock()
    bun.get_name.return_value = "black bun"
    bun.get_price.return_value = 100.0
    return bun


@pytest.fixture
def mock_ingredient_sauce():
    ingredient = Mock()
    ingredient.get_type.return_value = "SAUCE"
    ingredient.get_name.return_value = "hot sauce"
    ingredient.get_price.return_value = 100.0
    return ingredient


@pytest.fixture
def mock_ingredient_filling():
    ingredient = Mock()
    ingredient.get_type.return_value = "FILLING"
    ingredient.get_name.return_value = "cutlet"
    ingredient.get_price.return_value = 100.0
    return ingredient


@pytest.fixture
def empty_burger():
    from praktikum.burger import Burger
    return Burger()


@pytest.fixture
def burger_with_bun(mock_bun):
    from praktikum.burger import Burger
    burger = Burger()
    burger.set_buns(mock_bun)
    return burger


@pytest.fixture
def burger_with_ingredients(mock_bun, mock_ingredient_sauce, mock_ingredient_filling):
    from praktikum.burger import Burger
    burger = Burger()
    burger.set_buns(mock_bun)
    burger.add_ingredient(mock_ingredient_sauce)
    burger.add_ingredient(mock_ingredient_filling)
    return burger
