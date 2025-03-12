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

    def return_even(self):
        even_sequence = []
        for i in range(self.number1,self.number2):
            if i%2==0:
                even_sequence.append(i)
        return even_sequence

    @staticmethod
    def lambda_fun(num1, num2):
        expression=lambda x:num1+num2
        print(expression)
        return expression
