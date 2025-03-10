from unittest import TestCase
from BLOG.blog import Blog

class BlogTest(TestCase):
    def test_create_posts_in_blog(self):
        func = Blog("Mahesh Kumar", "Software Engineer")
        func.create_post("Test Post","Test Content")
        self.assertEqual(len(func.posts),1)
        self.assertEqual(func.posts[0].title,"Test Post")
        self.assertEqual(func.posts[0].content, "Test Content")

    def test_json(self):
        func = Blog("Adventure", "The King Maker")
        func.create_post("Test Post", "Test Content")
        expected={
            "title":"Adventure",
            "content":"The King Maker",
            "posts":[{
                "title":"Test Post",
                "content":"Test Content",
            }]
        }
        self.assertDictEqual(expected,func.json())