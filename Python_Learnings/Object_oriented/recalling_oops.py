import csv


class MyDetails:
   def __init__(_self,name,country,designation,company):
         _self.name=name
         _self.country=country
         _self.designation=designation
         _self.company=company
   def peronal_information(self):
      return f"Hi This is {self.name}. Im working as a {self.designation} in {self.company}. I live in {self.country}"



print("------------------------------------------------->")
self_personal_details=MyDetails("P Mahesh Kumar","Germany","Data Scientist","JP Morgan")
print(self_personal_details.peronal_information())
print("------------------------------------------------->")
Bfriend_personal_details=MyDetails("K Surya Teja","Germany","Data Engineer","JP Morgan")
print("Type :",type(Bfriend_personal_details))
Bfriend_personal_details.company="Apple"
Bfriend_personal_details.designation="Data Analyst"
print(Bfriend_personal_details.peronal_information())
print("------------------------------------------------->")
friend_personal_details=MyDetails("Vidhya Sagar","Germany","Data Analyst","JP Morgan")
print(friend_personal_details.peronal_information())
print("------------------------------------------------->")


# <class '__main__.MyDetails'>

# creating our own class

class Practice:
    test="emp"
    def __init__(self,name:str,age:int,company:str,country:str):
        # How to validate the values using the assert
        assert age>21, f"{age} is not greater than 21"
        self.name=name
        self.age=age
        self.company=company
        self.country=country

    def personal_details(self):
        return f"My name is {self.name} \nI'm {self.age} Years Old\nI'm working for {self.company} in {self.country} Country"

details_one=Practice("P Mahesh Kumar",24,"Persistent Systems","German")
print(details_one.personal_details())

print("Accessing the class attributes at the Instance Level :",details_one.test)
print("Accessing the Class attributes using the class name :",Practice.test)
"""
# Checking the no of attributes in the class / in the instance level usng the MAGIC ATTRIBUTE 
-------------
1.__dict__---->GIves the no of attributes in the class loevel / in the instance level
"""
print("INSTANCE LEVEL",details_one.__dict__)
print("CLASS LEVEL",MyDetails.__dict__)


class Sample:
    instances_list=[]
    def __init__(self,name,age):
        self.name=name
        self.age=age
        Sample.instances_list.append(self)


obj_one=Sample("Anil",24)
obj_two=Sample("Sunil",24)
obj_three=Sample("Ramandeep",24)
obj_four=Sample("deepak",24)
print(Sample.instances_list)

# To list out the Name of all the instances
instance_names=[]
for instance in Sample.instances_list:
    instance_names.append(instance.name)
print(instance_names)



# customizing the object address based on the instance is created
class SubSample:
    instance_names=[]
    def __init__(self,age,name):
        self.name=name
        self.age=age
        SubSample.instance_names.append(self)

    def __repr__(self):
        return f"PersonalDetails({self.name},{self.age})"

obj_one_child=SubSample("KUMAR",24)
obj_two_child=SubSample("Poojith",27)
obj_three_child=SubSample("Nalini",23)
obj_four_child=SubSample("Himavan",22)

print(obj_one_child.instance_names)


# Instantiating the data from the csv file

"""
Convert the method as a class method instance of the instance 

Decorators :
Using the decorators it is possible to convert the behaviour of functions that we write inside the class by calling them just before the line of the 
function that we write

 Using the @classmethod we can convert the method inside the class in to a class method
 
 when we create the class method the first paramater to the method is most likely to be the name of the class as (CLS)
 
 example:
 
 class Name:
     def __init__(self,name,age):
        self.name=name
        self.age=age
    @classmethod
    def name_details(cls):
        return f"My Name is {cls.name}"
"""
# Initiating the instances using the csv Data
class csvReader:
    all_instances=[]
    def __init__(self,name,country,domain,number):
        self.name=name
        self.course=domain
        self.country=country
        self.number=number
        csvReader.all_instances.append(self)
    def get_details(self):
        return f"Hi My Name is {self.name}\nIm from {self.country}\nI'm Working as a {self.course}"
    @classmethod
    def instantiate_csv(cls):
        with open('samp.csv','r') as data:
            data=csv.DictReader(data)
            for i in data:
                csvReader(i.get("name"),i.get('country'),i.get('domain'))
    def check_dtype(self):
        if isinstance(self.number,int):
            print("Yes the Number is Interger")
        else:
            print("Not an interger Number")
    def __repr__(self):
        return f"Person({self.name},{self.country})"
# print(csvReader.get_details())
# print(csvReader.instantiate_csv())
with open('samp.csv','r') as data:
    data = csv.DictReader(data)
    for i in data:
        obj=csvReader(i.get("name"),i.get('country'),i.get('domain'),int(i.get('number')))
        print(obj.get_details())
        print(obj.check_dtype())
    print(end=" ")

print(csvReader.all_instances)

# print(csvReader.all_instances)
# Reference to the static method