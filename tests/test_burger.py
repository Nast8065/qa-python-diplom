import pytest
from unittest.mock import Mock
from tests import data


@pytest.fixture
def mock_bun():
    return data.get_mock_bun()


@pytest.fixture
def mock_ingredient_sauce():
    return data.get_mock_ingredient_sauce()


@pytest.fixture
def mock_ingredient_filling():
    return data.get_mock_ingredient_filling()


@pytest.fixture
def mock_ingredient_cheese():
    return data.get_mock_ingredient_cheese()


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


def test_burger_price(burger_with_ingredients, mock_bun, mock_ingredient_sauce, mock_ingredient_filling):
    expected_price = (mock_bun.get_price() * 2 +
                     mock_ingredient_sauce.get_price() +
                     mock_ingredient_filling.get_price())

    assert burger_with_ingredients.get_price() == expected_price
    assert burger_with_ingredients.get_price() == 400.0  # 100*2 + 100 + 100


def test_burger_receipt(burger_with_ingredients):
    receipt = burger_with_ingredients.get_receipt()

    # Ожидаемый формат чека
    expected_receipt_lines = [
        f"(==== {data.TEST_BUN_NAME} ====)",
        f"= {data.TEST_SAUCE_TYPE.lower()} {data.TEST_SAUCE_NAME} =",
        f"= {data.TEST_FILLING_TYPE.lower()} {data.TEST_FILLING_NAME} =",
        f"(==== {data.TEST_BUN_NAME} ====)",
        "",
        f"Price: {400.0}"
    ]

    expected_receipt = "\n".join(expected_receipt_lines)
    assert receipt == expected_receipt


def test_burger_receipt_structure(burger_with_ingredients):
    """Альтернативный вариант: проверка структуры чека по строкам"""
    receipt = burger_with_ingredients.get_receipt()
    receipt_lines = receipt.split('\n')

    # Проверяем количество строк
    assert len(receipt_lines) == 6  # 4 строки с содержимым + пустая строка + итог

    # Проверяем конкретное содержание каждой строки
    assert receipt_lines[0] == f"(==== {data.TEST_BUN_NAME} ====)"
    assert receipt_lines[1] == f"= {data.TEST_SAUCE_TYPE.lower()} {data.TEST_SAUCE_NAME} ="
    assert receipt_lines[2] == f"= {data.TEST_FILLING_TYPE.lower()} {data.TEST_FILLING_NAME} ="
    assert receipt_lines[3] == f"(==== {data.TEST_BUN_NAME} ====)"
    assert receipt_lines[4] == ""
    assert receipt_lines[5] == f"Price: {400.0}"


def test_empty_burger_receipt(empty_burger):
    """Тест чека для пустого бургера"""
    receipt = empty_burger.get_receipt()

    # Для пустого бургера должен быть только Price: 0
    expected_receipt = "\n".join([
        "(====  ====)",
        "(====  ====)",
        "",
        "Price: 0"
    ])

    assert receipt == expected_receipt


def test_burger_with_only_bun_receipt(burger_with_bun, mock_bun):
    """Тест чека для бургера только с булочкой"""
    receipt = burger_with_bun.get_receipt()

    expected_receipt_lines = [
        f"(==== {data.TEST_BUN_NAME} ====)",
        f"(==== {data.TEST_BUN_NAME} ====)",
        "",
        f"Price: {mock_bun.get_price() * 2}"
    ]

    expected_receipt = "\n".join(expected_receipt_lines)
    assert receipt == expected_receipt
