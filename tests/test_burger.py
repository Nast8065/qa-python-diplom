import pytest
from unittest.mock import Mock
from praktikum.burger import Burger
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestBurger:

    def test_set_buns_sets_correct_bun(self, empty_burger, mock_bun):
        empty_burger.set_buns(mock_bun)
        assert empty_burger.bun == mock_bun

    def test_add_ingredient_adds_to_list(self, burger_with_bun, mock_ingredient_sauce):
        initial_count = len(burger_with_bun.ingredients)
        burger_with_bun.add_ingredient(mock_ingredient_sauce)
        assert len(burger_with_bun.ingredients) == initial_count + 1

    def test_remove_ingredient_removes_from_list(self, burger_with_ingredients):
        initial_count = len(burger_with_ingredients.ingredients)
        burger_with_ingredients.remove_ingredient(0)
        assert len(burger_with_ingredients.ingredients) == initial_count - 1

    def test_remove_ingredient_invalid_index_raises_error(self, burger_with_bun):
        with pytest.raises(IndexError):
            burger_with_bun.remove_ingredient(999)

    def test_move_ingredient_changes_position(self, burger_with_ingredients):
        first_ingredient_before = burger_with_ingredients.ingredients[0]
        burger_with_ingredients.move_ingredient(0, 1)
        assert burger_with_ingredients.ingredients[1] == first_ingredient_before

    def test_move_ingredient_invalid_index_raises_error(self, burger_with_ingredients):
        with pytest.raises(IndexError):
            burger_with_ingredients.move_ingredient(0, 999)

    @pytest.mark.parametrize("bun_price,ingredient_prices,expected_total", [
        (100, [50, 200], 450),  # (100*2) + 50 + 200 = 450
        (0, [50, 100], 150),    # (0*2) + 50 + 100 = 150
        (150, [], 300),         # (150*2) + 0 = 300
        (50, [10, 20, 30], 160) # (50*2) + 10 + 20 + 30 = 160
    ])
    def test_get_price_calculates_correctly(self, bun_price, ingredient_prices, expected_total):
        burger = Burger()

        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price

        mock_ingredients = []
        for price in ingredient_prices:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = price
            mock_ingredients.append(mock_ingredient)

        burger.set_buns(mock_bun)
        for ingredient in mock_ingredients:
            burger.add_ingredient(ingredient)

        assert burger.get_price() == expected_total

    def test_get_price_empty_burger_returns_zero(self, empty_burger):
        assert empty_burger.get_price() == 0

    def test_get_price_only_bun_returns_double_price(self, mock_bun):
        burger = Burger()
        burger.set_buns(mock_bun)
        expected_price = mock_bun.get_price() * 2
        assert burger.get_price() == expected_price

    def test_get_receipt_includes_bun_name(self, burger_with_bun, mock_bun):
        receipt = burger_with_bun.get_receipt()
        assert mock_bun.get_name() in receipt

    def test_get_receipt_includes_ingredient_names(self, burger_with_ingredients, mock_ingredient_sauce, mock_ingredient_filling):
        receipt = burger_with_ingredients.get_receipt()
        assert mock_ingredient_sauce.get_name() in receipt
        assert mock_ingredient_filling.get_name() in receipt

    def test_get_receipt_includes_total_price(self, burger_with_ingredients):
        receipt = burger_with_ingredients.get_receipt()
        total_price = burger_with_ingredients.get_price()
        assert str(total_price) in receipt

    def test_get_receipt_formats_correctly(self, burger_with_ingredients):
        receipt = burger_with_ingredients.get_receipt()
        assert "(==== " in receipt
        assert " ====)" in receipt
        assert "Price:" in receipt
        assert len(receipt) > 0

    def test_get_receipt_empty_burger(self, empty_burger):
        receipt = empty_burger.get_receipt()
        assert receipt is not None

    @pytest.mark.parametrize("ingredient_type,expected_in_receipt", [
        (INGREDIENT_TYPE_SAUCE, True),
        (INGREDIENT_TYPE_FILLING, True),
    ])
    def test_get_receipt_with_different_ingredient_types(self, ingredient_type, expected_in_receipt, mock_bun):
        burger = Burger()
        burger.set_buns(mock_bun)

        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = ingredient_type
        mock_ingredient.get_name.return_value = "Test Ingredient"
        mock_ingredient.get_price.return_value = 100

        burger.add_ingredient(mock_ingredient)
        receipt = burger.get_receipt()

        if expected_in_receipt:
            assert "Test Ingredient" in receipt

    def test_add_multiple_ingredients_preserves_order(self, burger_with_bun):
        mock_ingredient1 = Mock()
        mock_ingredient1.get_name.return_value = "First"

        mock_ingredient2 = Mock()
        mock_ingredient2.get_name.return_value = "Second"

        mock_ingredient3 = Mock()
        mock_ingredient3.get_name.return_value = "Third"

        burger_with_bun.add_ingredient(mock_ingredient1)
        burger_with_bun.add_ingredient(mock_ingredient2)
        burger_with_bun.add_ingredient(mock_ingredient3)

        assert burger_with_bun.ingredients[0] == mock_ingredient1
        assert burger_with_bun.ingredients[1] == mock_ingredient2
        assert burger_with_bun.ingredients[2] == mock_ingredient3

    def test_remove_ingredient_from_middle(self, burger_with_bun):
        mock_ingredient1 = Mock()
        mock_ingredient1.get_name.return_value = "First"

        mock_ingredient2 = Mock()
        mock_ingredient2.get_name.return_value = "Second"

        mock_ingredient3 = Mock()
        mock_ingredient3.get_name.return_value = "Third"

        burger_with_bun.add_ingredient(mock_ingredient1)
        burger_with_bun.add_ingredient(mock_ingredient2)
        burger_with_bun.add_ingredient(mock_ingredient3)

        burger_with_bun.remove_ingredient(1)

        assert len(burger_with_bun.ingredients) == 2
        assert burger_with_bun.ingredients[0] == mock_ingredient1
        assert burger_with_bun.ingredients[1] == mock_ingredient3

    def test_move_ingredient_to_same_position(self, burger_with_ingredients):
        ingredients_before = burger_with_ingredients.ingredients.copy()
        burger_with_ingredients.move_ingredient(0, 0)
        ingredients_after = burger_with_ingredients.ingredients
        assert ingredients_before == ingredients_after
