from unittest import TestCase

from test.post import Post


class Blog:
    def __init__(self, title, content):
        self.title=title
        self.content=content
        self.posts=[]


    def form_data(self):
        data=f"Hello My Name is {self.title} and I'm a {self.content}."
        return data

    def create_post(self,title,content):
        self.posts.append(Post(title,content))

    def json(self):
        return {
            "title":self.title,
            "content":self.content,
            "posts":[post.json() for post in self.posts]
        }

    def __repr__(self):
        return "{}({} Post{})".format(self.title,len(self.posts), 's' if len(self.posts)>1 else '')
