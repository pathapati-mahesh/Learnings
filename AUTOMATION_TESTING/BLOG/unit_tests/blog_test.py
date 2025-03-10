from unittest import TestCase
from BLOG.blog import Blog


class BlogTest(TestCase):
    def test_attributes(self):
        func=Blog("Mahesh Kumar","Software Engineer")
        self.assertEqual(func.title,"Mahesh Kumar")
        self.assertEqual(func.content, "Software Engineer")
        self.assertEqual(func.__repr__(),"Mahesh Kumar(0 Post)")

    def test_multiple_posts(self):
        func=Blog("Mahesh Kumar","Software Engineer")
        func.posts = ["Mahesh", "Anil"]
        self.assertEqual(func.__repr__(), "Mahesh Kumar(2 Posts)")
        func.posts = ["Mahesh", "Anil","Yuvaraj"]
        self.assertEqual(func.__repr__(), "Mahesh Kumar(3 Posts)")
