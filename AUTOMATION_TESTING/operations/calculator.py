from torch.utils.hipify.hipify_python import value


class Calculator:

    def __init__(self,sum1,sum2):
        self.number1=sum1
        self.number2=sum2

    def add(self):
        return self.number1+self.number2

    def sub(self):
        return self.number2-self.number1

    def modulus(self):
        return self.number2%self.number1

    def divide(self):
        return self.number2/self.number1

    def multiplication(self):
        return self.number2*self.number1

    def square(self):
        return self.number2**self.number1

class PersonDetails:
    def __init__(self,name,age,profession):
        self.__name=name
        self.__age=age
        self.__profession=profession

    @property
    def name(self):
        """The getter is defined using the @property decorator.
            It retrieves the value of the attribute.
        """
        return self.__name

    @name.setter
    def name(self,value):
        """
        The setter is defined with the @<attribute>.setter decorator,
        which allows you to modify the value of the attribute.
         The setter can include validation checks to ensure proper values
         are assigned (for example, ensuring age is non-negative).
        """
        self.__name=value

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self,value):
        assert  value>0,"Age has to be greater than 0"
        self.__age=value

    @property
    def profession(self):
        return self.__profession

    @profession.setter
    def profession(self,value):
        self.__profession=value

    def json(self):
        return {
            "name":self.__name,
            "age":self.__age,
            "profession":self.__profession
        }
