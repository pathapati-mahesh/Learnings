personal_details={
    "Name":"P Mahesh Kumar",
    "Age":20,
    "Country":"Germany"
}
print(personal_details.get("Age"))
print(personal_details.keys())
print(personal_details.values())
# Set the values for all the keys as same using the dict.fromkeys() method
persons_info=["Mahesh","Gowtham","Gowtham k","Anil","Lokesh"]
new_dict=dict.fromkeys(persons_info,"Germany")
print(new_dict)
samp_dict=new_dict.get("Mahesh")
print(samp_dict)
print(personal_details.items())
update_dct={
    "Occupation":"Software Engineer"
}
personal_details.update(update_dct)
print(personal_details)

# Multiple_keys=["Shasank","Mahesh","Gowtham","Gowtham K","Lokesh"]
# new_ky_pair=dict.fromkeys((Multiple_keys,'australians'))
# print(new_ky_pair)

# personal_details.popitem()
print(personal_details)

# personal_details.clear()
# print(personal_details)

# Copying the dictionary in 2 ways
# 1.copy() 2.dict()
# 1.copy():
cpy_dict=personal_details.copy()
cpy_dict["Name"]="Likkitha Chowdary"
print(cpy_dict)

# 2.dict()
new_cpy=dict(personal_details)
new_cpy["Name"]="Praveen"
new_cpy["Age"]=2
new_cpy.pop("Occupation")
print(new_cpy)
