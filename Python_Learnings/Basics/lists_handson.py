"""
*****
    Lists
    List is an array which is used to store the Multiple items irrespective of type

    List Methods:
    ----------------
    append()-->Used to add the elements in to the existing or new list

    remove(element)--->Used to remove the particular element from the list

    pop(index or nothing)-->By default the pop method removes the last element from the list if we mention
    the index number then the element in that index will be deleted Permanently.

    insert(index,data_you_need_to_add) --> Method is used to insert the elements at the particular index.

    sort(reverse=False) --->This element is used to sort the elements in a list.
    By default the elements will be in ascending order. If we set the reverse=True then the list
    will be ordered in descending order.

    clear()--->Clear method is used to empty the list it wont delete the list. After clearing it will give us the
    empty list

    copy()--> This method is used to copy the one list in to the other one.

    count() --> Count() method is used to count the no of occurance of a element in a string.

    extend() --> Extend () method is used to add the elements from one list to the other list at the end.

    index() --> This method returns the index of first occurance of an  element in a list.

    reverse() --> This method is used to reverse the elements  in a list

"""
a=["JAI BALAYYA",["Mahesh","Anil","PSPK","NTR"]]
from Python_Learnings.Object_oriented.classes import MyClass


export_class=MyClass("Pathapati Mahesh Kumar",2024,"December","16",23,"USA","Python Developer")
export_class.study_plans()
export_class.alternative_plans()
export_class.create_dict()

print("----------------------")
for j in range(len(a)):
    # print(a[j])
    for i in range(0,len(a[j])):
        print(a[j][i]+" ",end="")
# a.insert(1,"NTR")
for i in range(len(a)):
    if a[i]=="JAI BALAYYA"or a[i]=="NTR":
        # a.pop(1)
        continue
    else:
        for j in range(len(a[i])):
            # a[i][j].capitalize()
            if a[i][j]=="Mahesh" :
                continue
            else:
                # print(a,end="")
                print(a[i][j])
# # a.remove(a[1][0])
print("----------------------")
# # print(a)
#
#
# #

new_list=["Mahesh","Anil","Likitha","Renu"]
new_list.sort()
print(new_list)
# # Doubt here
number=[12,1221,121,212,222,1,3,2,4,6,5,7]
# print(number.pop(1))
print("-------------------")
number.sort(reverse=False)
print(number)
# new_list.clear()
# print(new_list)

#2d lists

# class
# def personal_info(MyClass)
fruits=["Orange","Apple","Kiwi"]
Biryani=["Dum","chicken","Mutton"]
desserts=["Cake","Lassi","Gulab Jamun"]

food=[fruits,Biryani,desserts]
for i in range(len(food)):
    for j in range(len(food[i])):
        print(food[j][0])

samp_lst=["Mahesh","Samba","NTR","RRR"]
new_lst=["DEVARA","NEILS_FLM"]
samp_lst.extend(new_lst)
print(samp_lst)

new_list=samp_lst.copy()
new_list.remove("Mahesh")
print("New_lst--------",new_lst)
print("NEW_LIST----------",new_list)
samp_lst.reverse()
print(samp_lst)
# new_list.clear()
# # del new_list
# print(new_list)
# print("CLEARED_LIST---------",new_list)
# print(samp_lst)