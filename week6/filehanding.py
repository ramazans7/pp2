#1
with open("text.txt","w") as f:
    f.write("Hello\n")
    f.write("This is a test file\n")

#2
with open("text.txt","r") as f:
    content = f.read()
    print(content)

#3
with open("text.txt","a") as f:
    f.write("New line added\n")

#4
import shutil

shutil.copy("text.txt" , "copy_text.txt")

#5
import os

os.remove("copy_text.txt")