from Python_Learnings.Object_oriented.classes import MyClass

#Creating the instance of the class and trying to access all the methods in it
# instance1=MyClass("P Mahesh Kumar",2024,"September","24-08-2024",24,"Germany","Data scientist")
# print(instance1.course_list())

# #For the class  level
# print("Class LEvel Attributes",MyClass.__dict__)

# #At the instance level we are checking for the attributes that are related to this instance
# print("Instance Level OR Object Level Attributes",instance1.__dict__)

# print("CLASS LEVEL ATTRIBUTE BUT ACCESING FROM THE INSTANCE LEVEL",instance1.courses)
# print("CLASS LEVEL ATTIBUTE ACCESSING USING THE CLASS",MyClass.courses)

# instance2=MyClass("A Vidhya sagar",2024,"OCTOBER","20-10-2024",24,"Germany","Developer")
# instance3=MyClass("A Shashank",2024,"OCTOBER","20-10-2024",24,"Germany","Project Manager")
# instance6=MyClass("P BOBBY",2024,"OCTOBER","20-10-2025",24,"Germany","Developer")
# instance4=MyClass("P Likkitha",2024,"OCTOBER","20-10-2024",24,"Germany","Data Analyst")
# instance5=MyClass("P Renu",2024,"OCTOBER","20-10-2035",24,"Germany","Parents")
# instance6=MyClass("P Bujji",2024,"OCTOBER","20-10-2035",24,"Germany","Parents")
# instance5=MyClass("P Chandana",2024,"OCTOBER","20-10-2035",24,"Germany","Sister")
# instance2.courses.append(["Embedded","ML"])

# for instance in MyClass.list_all_values:
#     print(f"Names :{instance.name}\nRole :{instance.domain}")
# print(instance2.course_list())
# print("Instance Level OR Object Level Attributes",instance2.__dict__)

# Using the class method creating the instances or objects

MyClass.instance_automatically()

print("CUSTOMIZING THE INSTANCE NAMES WHICH WILL BE USEFUL FOR THE IDENTIFICATION USING THE MAGIC METHOD '__repr__()'",MyClass.list_all_values)