"""
    Deleting the files/folders using the os and shutil module
    *****
    remove()---->This method removes the file in the mentioned path but it cant remove the directory it wil give the file permission error
    if we want to delete the entire file and the folder then we have to use the rmdir()
    rmdir()--->Removes the folder in the specified path if we have content in files in the folder then it wont delete all the files in the folder.
    -->If we want to delete the entire files and folder as well then we have to use the shutil Module.

    rmtree(path_od_folder_to_delete)---->This method is used to delete the folder
    and all the files inside the  folder no permission errors or os errors will not come up if we use shutil to remove the directory
    -->This method will remove the directory and all the other files present in it
"""
import os.path
# import shutil
import kwargs_lrn

kwargs_lrn.personal_details(name="P Mahesh Kumar",country="Germany",specialization="Datascience")

file_path="/home/mahesh/Desktop/practice_copying"
file_name=""
while file_name=="":
    file_name=input("Enter the name of the file to Delete in the path :")
    if os.path.exists(f"{file_path}/{file_name}.txt"):
        file_name=file_name
    else:
        if not os.path.isfile(f"{file_path}/{file_name}.txt"):
            with open(f"{file_name}.txt",'x') as file:
                file=file.write("kjhgfdghj")
            os.replace(f"{file_name}.txt",f"{file_path}/{file_name}.txt")

# Using remove(///)
file_deleted_path=f"{file_path}/{file_name}.txt"
if os.path.exists(f"{file_path}/{file_name}.txt"):
    try:
        os.remove(file_deleted_path)
    except OSError as e:
        print(str(e))
    print("Deleted the file successully")
#
# ------->This method will give me permission error because the directory that i mentioned it has some other files if we
# --->Want to remove all those files then we have to use the nshutil module to delete all the other files
# if os.path.isdir(f"{file_path}/"):
#     try:
#         os.rmdir(f"{file_path}/")
#     except OSError:
#         shutil.rmtree(f"{file_path}/")
#     print("Removed the folder succesfully!!")
# else:
#     print("Its Not a directory Please check the path")