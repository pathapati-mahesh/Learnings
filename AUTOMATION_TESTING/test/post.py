from logging import Logger
from venv import logger


class Post:
    def __init__(self, title:str, content:str):
        self.title = title
        self.content = content


    def json(self):
        data={
            'title':self.title,
            'content':self.content,
        }
        return data
    
    def __repr__(self):
        return "{},{}".format(self.title,self.content)


