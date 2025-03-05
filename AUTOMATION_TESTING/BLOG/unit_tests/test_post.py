from unittest import TestCase
from BLOG.post import Post


class PostTest(TestCase):

    def test_create_post(self):
        func=Post("P Mahesh Kumar","Software Engineer",[10,20,30,20,40,50,60,70])
        self.assertEqual("P Mahesh Kumar",func.title)
        self.assertEqual("Software Engineer",func.content)
        
    def test_data_json(self):
        func=Post("P Mahesh Kumar","Software Engineer",[10,20,30,20,40,50,60,70])
        expected={"title":"P Mahesh Kumar","content":"Software Engineer"}
        self.assertDictEqual(expected,func.data_json())

    def test_identif_odd_seq(self):
        func=Post('P Mahesh Kumar','Software Engineer',[10,20,30,20,40,50,60,70])
        expected=list([30,50,70])
        data=func.identif_odd_sequence()
        self.assertListEqual(func.identif_odd_sequence(),expected)
        self.assertEqual('P Mahesh Kumar',func.title)
        self.assertEqual('Software Engineer',func.content)
