from

Name="Anil Kumar"

print("FIRST NAME",Name[:6])
print("Last Name",Name[6:])

print("REVERSED NAME",Name[::-1])
print(len(Name))
print("USING THE STEP VALUE",Name[0:len(Name):2])
print("USING THE STEP EXTRACTING THE START AND END LETTERS OF  NAME",Name[0:len(Name):len(Name)-1])

#USING THE SLICE() METHOD TO SLICE THE STRING

website="https://google.com"
splitted_string=website.split("//")
print("Splitted string:",splitted_string)
new_substring=splitted_string[1]
r=new_substring.split(".")
print("Extracted website Name :",r[0])


# ----->Slice() Method

Slice=slice(8,-4)
print("USING THE SLICE() METHOD :",website[Slice])


# String slicing
name="Mahesh Kumar"
print(name[(len(name)//2):len(name)].strip())