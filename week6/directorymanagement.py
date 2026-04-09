#1
import os

os.makedirs("folder/subfolder", exist_ok=True)

#2
files = os.listdir(".")
print(files)

#3
files = os.listfir(".")
txt_files = [f for f in files if f.endswith(".txt")]

print(txt_files)

#4
import shutil

shutil.move("text.txt", "folder/text.txt")