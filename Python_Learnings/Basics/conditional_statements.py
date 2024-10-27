#if statements

str_1="Mahesh"
str_2="Mani"

if str_1.startswith(("M")) and str_2.startswith("M"):
    print("Both the Names starts with the M")
    if str_1.isalpha() and str_2.isalpha():
        print("Both the strings are alphabets")
        for i in str_1:

            if i=="M":
                print(f"HIP HIP HURRAY NAME CONTAINS {i}")
            print(i)
elif len(str_1)==len(str_2):
    print("Length of both the names are same")

#CHECKING THE AGE GROP OF THE PERSONS IF THE AGE IS <18 then CHILDREN IF AGE is >18 and LESSTHAN 50 is ADULT then AGE>50 SENIOR CITIZEN

age=input("ENTER YOUR AGE :")
if age !="":
    if int(age)<18:
        print("CHILDREN")
    elif int(age)>=18 and int(age)<=50:
        print("YoUTH")
    elif int(age)>50:
        print("Senior Citizen")
else:
    print("Please enter your Age")

