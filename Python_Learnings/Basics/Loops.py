import time
# #whileLoop-->A block of code will be executed continuously till the condition is remains as True
# Problem statement if the user had enteres the name then print the name is there but if user had forgot then display an error message
name=""
while(name==""):
    name=input("ENter your Name :")

print(f"Your Name is {name}")
for seconds in range(0,12,1):
    print(seconds)
    time.sleep(2)
print("HAPPY BIRTHDAY")

# PATTERN CODES
rows=int(input("ENter No of ROws :"))
columns=int(input("ENter No of columns :"))
for i in range(rows):
    for j in range(columns):
        if j<=i:
            print("*",end="")
    print()


#LOOP CONTROL STATEMENTS
#continue


fruits=["APPLE","BANANA","ORANGE","PINEAPPLE"]

vegetables=["Carrot","Brinjal","Drumsticks"]

for i in fruits:
    if i=="PINEAPPLE":
        for j in vegetables:
            if j=="Drumsticks":
                continue
            print(j)
        continue
    print(i)

# for i in range(20):
#     if i==0:
#         pass
#     else:
#         print(i)


















