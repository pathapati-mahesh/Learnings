from logging import Logger
from venv import logger


class Post:
    data=list()
    def __init__(self, title:str, content:str,sequence):
        self.__title = title
        self.content = content
        self.sequence=sequence
        self.odd_sequence=[]

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
       self.__title = value

    def data_json(self):
        data={
            'title':self.title,
            'content':self.content,
        }
        return data

    def identif_odd_sequence(self):
        for i in range(len(self.sequence)):
            logger.warning("started")
            logger.info("Its odd")
            if self.sequence[i]%2!=0:

                self.odd_sequence.append(self.sequence[i])
                Post.data.append(self.sequence[i])
        # print(self.odd_sequence)
        return self.odd_sequence
    
    def __repr__(self):
        return self.odd_sequence


if __name__=='__main__':
    data_Post=Post("Mahesh","rtyuiop",[1,2,3,4,5,6,7,8,9])
    sequence=data_Post.identif_odd_sequence()
    print(data_Post.title)
    data_Post.title="nani"
    print(data_Post.title)
    print(data_Post.data)
