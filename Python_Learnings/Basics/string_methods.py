#replace() ,strip(),lower(),casefold(),center(),count(),encode(),expandtabs(),upper(),capitalize(),isdigit(),isalpha(),startswith(),endswith(),find()
# format(),format_map()
"""
****
String Methods:
****
Methods which will be useful to create or modify or replace the certain part in the string

-------Built in string methods------------
len()--->to find the length of a string.

find()-->returns the index of a character or a part of the first occurance of a string.

capitalize()--->Converts the first character of a string in to upper cases.

lower()--->converts all the characters in to lower cases.

upper()--->converts all the characters in to upper case.

center()-->This method is useful to align the string to the center using a specified character, SPace is the default character.

expandtabs()-->The expandtabs() method sets the tabsize to the specified no of whitespaces.

format()-->Used to format the strings. Bysing the curley Brackets{} we can achieve this.
    The Placeholders can be identified using the named indexes {prices}, numbered indexes{0}, or even empty brackets {}

startswith()-->returns true if the part of the string is started with the mentioned characters.

endswith()-->returns true if the string ends with the mentioned part of the string.

replace()-->Used to replace the part of the string or the word with the other part of the text or characeter.

casefold()--->It is as same as the lower() method [Converts the characters in to lower case].

isdigit()--->If the entered string has all the digits then it returns True.

strip()-->Used to remove the space from the start and the end of the string.

split()-->The split() method returns a list where the text between the specified separator
becomes the list items.

encode()-->Used to encode the part of string in to the required format.

isalpha()-->returns True if the string has all the characters with out any special characters in the string.
"""

#len() Function
name="m\ta\th\te\ts\th"
print("Length of the string :",len(name))

#find()
print("using the find() method :",name.find("h"))

#captalize()
print("capitalize() :",name.capitalize())

#lower()
print("lower() :",name.lower())

# upper()
print("upper() :",name.upper())

# center(Noof characters,"Special character")
print("center() :",name.center(10,"#"))

# expandtabs(tabsize)
print("expandtabs() :",name.expandtabs(3))

# format()
text="My Name is {name}. Im going to {country} in the month of  {month}"
text.format(name="P Mahesh Kumar",country="Germany",month="August")
print(text.format(name="P Mahesh Kumar",country="Germany",month="August"))
# startswith()
print("startswith() :",name.startswith("aM"))

# endswith()
print("endswith() :",name.endswith("ah"))

#replace()
print("replace() :",name.replace("ah","eyu"))

# casefold()
print("casefold() :",name.casefold())

# isdigit()
print("isdigit() :",name.isdigit())

# strip()
print("strip() :",name.strip())

#isalpha()
print("isalpha() :",name.isalpha())

# split()
new_design="My Name is Mahesh, and Im from from Chittoor"
print("split()",new_design.split(" "))

# encode()
txt = "My name is Ståle"
# print(txt.encode(encoding="ascii",errors="strict"))#strict method will raise an error if the character is not able to encode
print(txt.encode(encoding="ascii",errors="backslashreplace"))#replaces the character is not encoded with the backslash [//]
print(txt.encode(encoding="ascii",errors="ignore"))#Ignores the character which is unable to encode
print(txt.encode(encoding="ascii",errors="namereplace"))#Replaces the character with the text explaining the character
print(txt.encode(encoding="ascii",errors="replace"))#Replaces the character with the question mark which is not able to encode
print(txt.encode(encoding="ascii",errors="xmlcharrefreplace"))#Replaces the character with the xml character

# Fomatting syles
# 1.<:--->Left aligns the results based on the no of spaces in the below example 20 is the number so 20 tabspaces will be

text="My Name is {:<20}"
print(text.format("Mahesh"))

#2. :> ---->Used to align the result to the right side with in the available space
news="Hello good afternoon this is {:>20}"
print(news.format("Mahesh"))

#:^ center aligns the result with in the available space
news="Hello {:^10} welcome to Germany"
print(news.format("Mahesh"))

#:=   -->Aligns the sign to the left most position

news="This is a {:20} Number"
print(news.format(-30))
# : -->adds an extra space before the positive number and use a - before the negative number to add the extra space
text="I always like {: 30} Numbers"
print(text.format(30))

#:+ --->use a plus symbol to indicate whether the results are positive or negative

text="I always like {:+14} Numbers"
print(text.format(-30))


# :, --->	Use a comma as a thousand separator
# :_  -->used underscore as a thousand seperator

# example:
text="My dream is to earn {:,}"
print(text.format(1000000000000000))
text="My dream is to earn {:_}"
print(text.format(1000000000000000))

# :c  -->Converts the value in to a corresponding unicode character
text="I always like {:c} Numbers"
print(text.format(110))
# :b -->Converts the value in to the Binary format

text="THe Binary Value of {value} is {value:b}"
print(text.format(value=20))

# :d  -->Converts the value in to the decimal format
text="THe Decimal Value of {value} is {value:d}"
print(text.format(value=0b10))

# :e --> converts the given value in to the scientific format in lower case
text="New number format is {:e}"
print(text.format(1.2))

# :E --> converts the given value in to the scientific format in Uppercase case
text="New number format is {:E}"
print(text.format(1.2))

# :f--->.2f will set the limit of the decimal points to 2 Fix point number format-->This will be used to restrict the No of decimal points appearance
text="I want to convert the {num} to fixed decimal point as {num:.2f}"
print(text.format(num=20.23456))
# :F Fix point number format, in uppercase format (show inf and nan as INF and NAN)
x = float('inf')
txt = "The price is {:F} dollars."
print(txt.format(x))

#same example, but with a lower case f:
txt = "The price is {:f} dollars."
print(txt.format(x))



# :g		General format
# :G		General format (using a upper case E for scientific notations)
# :o		Octal format
# :x		Hex format, lower case
# :X		Hex format, upper case
# :n		Number format
# :%		Percentage format
