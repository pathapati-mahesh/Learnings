# for numbers we have to import the math module
import math
import random
# round()--->Round of method is used to round the number /values to the nearest value
number=21.5 #if the number is >=.5 then the rounded of to the next number.
# otherewise it will be rounded to the same number
print(round(number))

# math.ceil() this method is used to round up the value-->This method is used to round off to the next value
a=2
print(math.ceil(a))

# math.floor() this method is used to round down the value
print(math.floor(a))

# math.pow() -->This method is used to determine the power of a number. This method takes two arguments
print(math.pow(a,4)) # Here in this example this method will get the power of the 2 by raising it four times
#arg01: will be our number which we want to find the power
#arg02: will be the no of times that we want for the number

# min() , max()
list1=[5,9]
list2=[12,9]

print(max(list2,list1))
print(min(list2,list1))

# abs()-->This method returns the absolute value of a given/provided number
print(abs(math.sin(30)))
# math.sqrt()--> Used to find the sqare root of a number
print(int(math.sqrt(16)))

# Python does not have a random() function to make a random number, but Python has a
# built-in module called random that can be used to make random numbers:
# random()-->Used to generate the random of numbers between the mentioned range
# randrange()	Returns a random number between the given range
# randint()	Returns a random number between the given range
print(random.randint(-2,220))