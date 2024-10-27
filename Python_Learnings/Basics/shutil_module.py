import os
import os.path
import shutil
path='/home/mahesh/Desktop/'
# text_file_1='samp.txt'
# text_file_2 = "samp2.txt"
path_one=f"{path}"
print("--------------------")
# if  os.path.isdir(path):
#     with open(text_file_2, 'x') as file:
#         file = file.write("XweqX")
if os.path.isdir(path_one):
    copy_file=shutil.copyfile(src="/home/mahesh/Desktop/MY_LEARNINGS/ReactProject/Python_Learnings/Object_oriented/text.csv",dst='/home/mahesh/Desktop/practice_copying/temp.txt')

copy_method = shutil.copy(
    src="/home/mahesh/Desktop/MY_LEARNINGS/ReactProject/Python_Learnings/Object_oriented/text.csv",
    dst='/home/mahesh/Desktop/practice_copying/copy_method.txt')
# cpy_meta=os.stat(copy_method)
# print(cpy_meta)
copy2_method = shutil.copy2(
    src="/home/mahesh/Desktop/MY_LEARNINGS/ReactProject/Python_Learnings/Object_oriented/text.csv",
    dst="/home/mahesh/Desktop/practice_copying/copy_two.txt")
# meta_data=os.stat(copy2_method)
# print(meta_data)