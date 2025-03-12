from operations.string_operations.person_details import PersonDetails
import pytest

class TestPersonDetails:

    @pytest.fixture
    def test_details(self):
        return PersonDetails("P Mahesh Kumar",10,"Machine Learning Engineer")

    def test_json(self,test_details):
       assert test_details.json()=={"name":"P Mahesh Kumar","age":10,"profession":"Machine Learning Engineer"}

    def test_save_data(self,test_details):
        print(test_details.save_details())