import os



file_name=""
while file_name=="":
    file_name=input("Please give the filename to create :)")

if not os.path.exists(f"/home/mahesh/Desktop/practice_copying/{file_name}.txt"):
    try:
        with open(f"{file_name}.txt","x") as file:
            file=file.write("wretyuiopsdfdghjkxdcgfvjbknl//netryuioetyuyudfghjkldgfhjksfdghjk//nsfdghjklfdghjkl")
            print("File is created success fully and the content is written in to the file")
    except FileExistsError as e:
        print("File is ther already in the directory",e)
    
if os.path.exists(f"/home/mahesh/Desktop/practice_copying/{file_name}.txt"):
    with open(f"{file_name}.txt",'a') as file_write:
        file_write=file_write.write("Hello We have the content overridden.....Beacuse the file is already there in the mentioned path")
        print("File is already there and the content is over written")
if os.path.isfile(f"{file_name}.txt"):
# Using the python replace() method we can do that for that we need the path of the directory to store the files
    file_replce=os.replace(src=f"{file_name}.txt",dst=f"/home/mahesh/Desktop/practice_copying/{file_name}.txt")
else:
    print("File Not found")