import os

path="C:/Users/prmah/OneDrive/Desktop/Python/PYTHON-LEARNINGS/ReactProject/Python_Learnings/Object_oriented"
if os.path.exists(path):
    print("Yes,Path is there.....")
    if os.path.isfile(path):
        print("File is also there....")
    elif os.path.isdir(path):
        print("Its a directory")
    else:
        print("Its not neither a file nor a directory....")
else:
    print("Location doesnot exist..")

# Reading a file
"""
Note
--------------
1.if the file that you want to read or write.
Then we dont have to provide the path to that file to read we just need to give the file name
2.If the file is out some where else then we need to provide the path of it.

Reading a file in Python:
******************************
1.There are entirely three mode 
   i. 'r' and 'rt' ---->This is used to read a text or any format file[both are same]
   ii. 'a' ------------>This is used to append the information in to the existing file.
   iii. 'w' ----------->Using this we can write a file. But this one will over ride the existing content
    in the file.
   iv. 'x' ------------>This is used to create the specified file and returns an error.
    if the file already exists.

"""
content="""Name,COMPANY,QUALIFICATION
P Mahesh Kumar,Persistent,Btech
P Chandana,Empasis,Degree
Vidhyasagar,CGI,Btech
Likkitha Chowdary,Infosys,Btech"""

file="practise.txt"
if not os.path.isfile(file):
    with open(file,"x") as file:
        file=file.write(content)

else:
    print("File already exists")