from os import name, system

def clear_screen():
    if name == "posix":
        system("clear")
    else:
        system("cls")
