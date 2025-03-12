from unittest import TestCase
from test.post import Post


class PostTest(TestCase):

    def test_create_post(self):
        func=Post("P Mahesh Kumar","Software Engineer")
        self.assertEqual("P Mahesh Kumar",func.title)
        self.assertEqual("Software Engineer",func.content)
        
    def test_json(self):
        func=Post("P Mahesh Kumar","Software Engineer")
        expected={"title":"P Mahesh Kumar","content":"Software Engineer"}
        self.assertDictEqual(expected,func.json())

    def test_attributes(self):
        func=Post('P Mahesh Kumar','Software Engineer')
        self.assertEqual('P Mahesh Kumar',func.title)
        self.assertEqual('Software Engineer',func.content)
