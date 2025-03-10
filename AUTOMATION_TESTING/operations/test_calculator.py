import pytest
from operations.calculator import Calculator, PersonDetails


class TestCalculator:

    @pytest.fixture
    def calc(self):
        return Calculator(30, 30)

    def test_add(self,calc):
        assert calc.add() == 60

    def test_sub(self,calc):
        assert calc.sub() == 0

    def test_modulus(self,calc):
        assert calc.modulus() == 0

    def test_divide(self,calc):
        assert calc.divide() == 1

    def test_multiplication(self,calc):
        assert calc.multiplication() == 900

    def test_square(self,calc):
        assert calc.square() == (30**30)


class TestPersonDetails:
    @pytest.fixture
    def test_details(self):
        return PersonDetails("P Mahesh Kumar",25,"Machine Learning Engineer")

    def test_json(self,test_details):
       assert test_details.json()=={"name":"P Mahesh Kumar","age":25,"profession":"Machine Learning Engineer"}