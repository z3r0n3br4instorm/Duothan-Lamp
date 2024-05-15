import os
x = input("Enter Your Interface :\n1. Arduino\n2. Raspberry Pi\n>")

if x == "1":
    os.system("/home/zerone/duothanEnv/bin/python main_arduino.py")
elif x == "2":
    os.system("/home/zerone/duothanEnv/bin/python main_raspberry.py")
else:
    print("Invalid Input")
    exit()