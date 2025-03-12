from os.path import exists
import os
from sympy.physics.units import percent

from operations.string_operations import StringOperations
import json
import  pandas as pd

class PersonDetails(StringOperations):
    data=[]
    def __init__(self, name: str, age: int, profession: str):
        super().__init__(name, age, profession)
        assert age > 0, "Age has to be greater than 0"


    def json(self):
        return {
            "name":self.name,
            "age":self.age,
            "profession":self.profession
        }

    def list_dicts(self, new_data):
        self.data.append(new_data)  # Add new dictionary to list
        return self.data  # Return updated list

    def save_details(self):
        filename = "file.json"
        """Save data to JSON file without overwriting."""
        if os.path.exists(filename):  # Check if file exists
            try:
                with open(filename, 'r+') as file:
                    existing_data = json.load(file)  # Load existing data
                    if not isinstance(existing_data, list):  # Ensure it's a list
                        existing_data = []
            except json.JSONDecodeError:
                existing_data = []  # Handle empty or invalid JSON file
        else:
            existing_data = []

        existing_data.extend(self.data)  # Add new entries to existing data

        # Write back to the file
        with open(filename, 'w') as file:
            json.dump(existing_data, file, indent=4)

        self.data.clear()  # Clear in-memory list after saving to avoid duplicates

    def convert_data_df(self):
        data_json=self.json()
        df=pd.DataFrame(data=data_json,index=1)
        return df

if __name__=="__main__":
    p1=PersonDetails("Mahesh Kumar",20,"Senior CEO")
    p2=PersonDetails("Anil Humble",99,"Cricketer")

    if not exists("file.json"):
        f=open("file.json","x")

    else:
        p1.list_dicts(p1.json())
        p2.list_dicts(p2.json())
        p1.list_dicts(p1.json())
        p2.list_dicts(p2.json())
        p1.list_dicts(p1.json())
        p2.list_dicts(p2.json())
        p1.save_details()