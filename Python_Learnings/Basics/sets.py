# Sets are used to store multiple items in a single variable.
# Set is one of 4 built-in data types in Python used to store collections of data, the other 3 are List, Tuple, and Dictionary, all with different qualities and usage.
# A set is a collection which is unordered, unchangeable*, and unindexed.
# Sets cannot have two items with the same value.
# Set is represented as {}

fruits={"Mahesh","Anil","Onkar","Manas","Prabhat"}
#
# print(fruits)

# sets Methods
# add,copy,pop,clear,union,discard,difference,difference_update,discard,intersection,
# intersection_update,isdisjoint,
# issubset,issuperset,remove,symmetric_difference,symmetric_difference_update,update

# # add()
# # ---------we can add the new items in to the set once the set is created  so using the add() mthod we can add the items in to the set--
#
print(fruits.add("Maaaaaaaaaaaaahi"))
# ---->Duplicate values are not allowed and also unordered
print(fruits)
#
temp_set={"Mahesh","Manas","Onkar","Ankit","Prabhat","Adil"}
new_set=temp_set.copy()
print("New SET using the COPY()",new_set)
temp_set.clear()
print("Cleared Set using the Clear()",temp_set)#--Returns the empty Set

# difference()--->this method is used to compare two sets

set_1={"Amazon","Google","Persistent","Infosys"}
set_2={"MaheshIL","OIL","MasterIS","Amazon","Google","Persistent","Infosys"}
final_set=set_2.difference(set_1)
print(final_set)
print("COMPARED SET ELEMENTS",final_set)
#
# # difference_update()
# # The difference_update() method removes the items that exist in both sets.
# #
# # The difference_update() method is different from the difference() method, because the difference() method returns a new set,
# # without the unwanted items, and the difference_update() method removes the unwanted items from the original set.
#
# x={"a","b","c","d","e"}
# y={"1","2","3","4","a","b"}
# x.difference_update(y)
# print(x)


# remove() & discard()

# -->both the Methods are used to remove the particular key from the set but if the key is not there in the set the remove() method will raise an error but the discard() wont raise any error

# example={"Nan","don","Son"}
# print(example.discard("Nan"))
# print(example)
# print(example.remove("Nann"))--->Raises a Key error

# intersection()
# -->returns the common elements from all the sets
x = {"apple", "banana", "cherry"}
y = {"goomhbgle", "mickbrosoft","banana","apkjple"}
a = {"appjle", "banana", "hk"}
b = {"goohjgle", "microsokft", "apphbjle","banana", "cherrb my"}
z = x.intersection(y,a,b)
# print(a,b)
print(z)


# intersection_update()
# The intersection_update() method removes the items that is not present in both sets (or in all sets if the comparison is done between more than two sets).

# The intersection_update() method is different from the intersection() method, because the intersection() method returns a new set,
# without the unwanted items, and the intersection_update() method removes the unwanted items from the original set.

z=x.intersection_update(y,a,b)
print(x)
# print(z)
