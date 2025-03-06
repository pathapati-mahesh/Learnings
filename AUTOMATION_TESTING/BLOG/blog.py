from unittest import TestCase
class Blog(TestCase):
    def __init__(self, name,profession,hobbies,sequence):
        self.name=name
        self.profession=profession
        self.hobbies=hobbies
        self.posts=[]
        self.sequence=sequence
    
    def form_data(self):
        data=f"Hello My Name is {self.name} and I'm a {self.profession}. My Hobbies are{self.hobbies}"
        return data


    def __repr__(self):
        return "{}({} Post{})".format(self.name,len(self.posts), 's' if len(self.posts)>1 else '')

