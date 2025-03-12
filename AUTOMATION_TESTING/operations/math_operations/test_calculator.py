import pytest
from operations.math_operations.calculator import Calculator


class TestCalculator:

    @pytest.fixture
    def calc(self):
        return Calculator(10, 20)

    def test_add(self,calc):
        assert calc.add() == 30

    def test_sub(self,calc):
        assert calc.sub() == 10

    def test_modulus(self,calc):
        assert calc.modulus() == 0

    def test_divide(self,calc):
        assert calc.divide() == 2

    def test_multiplication(self,calc):
        assert calc.multiplication() == 200

    def test_square(self,calc):
        assert calc.square() == (20**10)

    def test_even_sequence(self,calc):

        assert calc.return_even() == [10,12,14,16,18]

    def test_lambda_fun(self,calc):
        assert  calc.lambda_fun(10,20)==30