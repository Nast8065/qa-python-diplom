import pytest
from praktikum.bun import Bun


class TestBun:

    def test_get_name_returns_correct_name(self):
        bun = Bun("black bun", 100.0)
        assert bun.get_name() == "black bun"

    def test_get_price_returns_correct_price(self):
        bun = Bun("white bun", 200.0)
        assert bun.get_price() == 200.0

    def test_bun_with_zero_price(self):
        bun = Bun("free bun", 0.0)
        assert bun.get_price() == 0.0

    def test_bun_with_special_characters_in_name(self):
        bun = Bun("bun #1", 150.0)
        assert bun.get_name() == "bun #1"

    def test_bun_with_float_price(self):
        bun = Bun("precise bun", 99.99)
        assert bun.get_price() == 99.99
