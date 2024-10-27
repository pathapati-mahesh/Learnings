import random
"""
*****
Random Module
--------------------
1.random()  -->This method is used to generate the random float values. No arguments are required
2.randint() -->This method is used to generate the sequence of integer Numbers. Arguments are required start and end of the numbers to generate
3.choice()  -->This method is used to generate the random choices from the provided Data. Arguments are required
4.shuffle() --> This method is used to shuffle the provided data in to various no of sequences. Arguments are required
"""
generate_rand_num=random.random()
print(generate_rand_num)
new_num=random.randint(20,200)
print(new_num)

cards=[1,2,3,4,5,6,7,8,9,"K","Q","J","A"]
random.shuffle(cards)
print(cards)

choosen_card=random.choice(cards)
print("Choices---------->",choosen_card)