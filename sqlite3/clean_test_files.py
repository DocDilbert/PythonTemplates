import os
import glob 

for fl in glob.glob("*.bin"):
    #Do what you want with the file
    os.remove(fl)


for fl in glob.glob("*.db"):
    #Do what you want with the file
    os.remove(fl)
