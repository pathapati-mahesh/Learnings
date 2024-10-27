import csv

class MyClass:
    courses=["AI","CS","Data Science","Data Analytics"]
    list_all_values=[]

    def __init__(self,name:str,year:int,month:str,date:str,age:int,country:str,domain:str):
        self.name = name
        self.year = year
        self.month = month
        self.age=age
        self.country=country
        self.date=date
        self.domain=domain
        MyClass.list_all_values.append(self)

    def study_plans(self):
        print(f"My name is {self.name} and Im going to USA on {self.date}/{self.month}/{self.year}")
        if self.year<2025:
            print("Best option you have opted to go there and do the education Now")

    def alternative_plans(new):
        if new.year>2025:
            print(f"{new.name} please go for switching the job roles it may offer you around 17 LPA")
        else:
            print(f"{new.name} you did it never stop working hard for your goal it may take time but you will achieve what you want")

    def course_list(self):
        return self.courses
    
    def create_dict(self):
        new_dict={
            "Name":self.name,
            "Age":self.age,
            "Country":self.country
        }

        #Extracting the keys in the dictionary
        print(new_dict.keys())

        #Extracting the values in the dictionary
        print(new_dict.values())

        #Extracting the keys & Values in the dictionary using the items()
        for i,j in new_dict.items():
            print(f"{i}:{j}")

        #Copying the dictionaries 1.copy() 2.dict()
        temp_dict=new_dict.copy()
        print("Original Dictionary :",new_dict)

        #Updating the dictionary with the new keys & values
        temp_dict.update({
            "Domain ":self.domain
        })
        print("Temp dictionary after copying :",temp_dict)
        test_dict=dict(temp_dict)

        # Using the popitem() method it will remove the last inserted key value pair from the dictionary
        test_dict.popitem()
        test_dict.pop("Country")
        print(test_dict)
        test_dict.setdefault("Country","Germany")

        # clearing the test_dict using the clear () method
        test_dict.clear()
        print("Test-dict after setting the new key in to it",test_dict)

    # Creating the class Method which will create the Objects/instances automatically we based on the vlues in the CSV
    @classmethod
    def instance_automatically(cls):
        with open('text.csv','r',) as f:
            reader=csv.DictReader(f)
            read_values=list(reader)
            print(read_values)
            for item in read_values:
                MyClass(name=item.get('name'),year=int(item.get('year')),month=item.get('month'),date=item.get('date'),age=int(item.get('age')),country=item.get('country'),domain=item.get('domain'))

    @staticmethod
    def method_stat(name,age):
        return "Hi my name is {name} and I'm {age} years old".format(name=name,age=age)



    # Magic Method 2 Which will be helpful to Customize the object name and can be useful to identify the instances/objects easily
    def __repr__(self):
        return f"MyClass({self.name},{self.domain})"




MyClass.instance_automatically()
#Create an object where we can able to access the methods in side the class
det_name=MyClass("Mahesh",2024,"August","16/08/2024",24,"Gernmany","Data Science")
print(det_name.study_plans())
print(det_name.list_all_values)
print("det---Name",det_name)#---->object name
print(det_name.instance_automatically())
print(det_name.method_stat("ANIL",24))


# type checking

