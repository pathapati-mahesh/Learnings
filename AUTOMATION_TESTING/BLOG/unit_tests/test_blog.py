from unittest import TestCase
from BLOG.blog import Blog
class BlogTest(TestCase):
    def test_attributes(self):
        func=Blog("Mahesh Kumar","Software Engineer",["Football,Volleyball,Computer Gaming"],[1,2,4,5,6])
        self.assertEqual(func.name,"Mahesh Kumar")
        self.assertEqual(func.profession, "Software Engineer")
        self.assertListEqual(func.hobbies,["Football,Volleyball,Computer Gaming"])
        self.assertListEqual(func.sequence, [1,2,3,4,5,5,6])