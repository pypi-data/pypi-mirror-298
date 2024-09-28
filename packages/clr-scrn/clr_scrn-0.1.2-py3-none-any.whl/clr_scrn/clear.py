import os

def clr_screen():
    if os.system == 'nt':
        os.system('cls')
    else:
        os.system('clear')