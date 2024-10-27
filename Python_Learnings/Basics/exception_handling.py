"""
Exception Handling

Events detected during the execution that interrupt the normal flow of a program.
Using the try except block we are going to
"""
a=""
try:
    while(a==""):
        a=input("Please enter Your Name :")
except Exception as e:
    print(e)
else:
    print(a)
finally:
    print("Hipp Hupp Hurray")