from unittest import TestCase
class Blog(TestCase):
    def __init__(self, name,profession,hobbies,sequence):
        self.name=name
        self.profession=profession
        self.hobbies=hobbies
        self.evensequence=[]
        self.oddsequence=[]
        self.sequence=sequence
    
    def form_data(self):
        data=f"Hello My Name is {self.name} and I'm a {self.profession}. My Hobbies are{self.hobbies}"
        return data

    def define_sequence(self):
        for num in self.sequence:
            if num%2==0:
                self.evensequence.append(num)
            else:
                self.oddsequence.append(num)
        return (self.evensequence,self.oddsequence)