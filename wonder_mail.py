import pyautogui
import sys
import formatter
import os.path
from os import path
import time

pyautogui.PAUSE = 0.04

PASSWORD_LENGTH = (34)

PASSWORD_DICT = {"C": (1275, 690), "F": (1448, 690), "H": (1560, 690), "J": (1681, 690), "K": (1729, 690), "M": (1848, 690),
                 "N": (1168, 746), "P": (1281, 746), "Q": (1340, 746), "R": (1396, 746), "S": (1457, 746), "T": (1507, 746),
                 "W": (1675, 746), "X": (1733, 746), "Y": (1790, 746), "0": (1168, 792), "1": (1229, 792), "2": (1281, 792),
                 "3": (1337, 792), "4": (1393, 792), "5": (1451, 792), "6": (1504, 792), "7": (1562, 792), "8": (1619, 792),
                 "9": (1672, 792), "@": (1730, 792), "&": (1839, 792), "-": (1165, 845), "#": (1278, 845), "%": (1392, 845),
                 "+": (1628, 845), "=": (1733, 845), "END": (1033, 845)}

MENU_DICT = {"DIALOG_BOX": (1440, 840), "RECIEVE_ENTRY": (
    1440, 560), "PASSWORD_ENTRY": (1320, 520)}


def EnterPassword(password_string: str):
    for letter in password_string:
        if letter in PASSWORD_DICT:
            pyautogui.moveTo(PASSWORD_DICT.get(letter))
            Click()
    pyautogui.moveTo(PASSWORD_DICT.get("END"))
    Click()
    pass


def NavigatePostEntryDialog():
    print("Assuming dialog ready")
    pyautogui.moveTo(MENU_DICT.get("DIALOG_BOX"))
    Click()
    # Wait for save time
    time.sleep(6)
    print("Assuming saving done now")
    Click()
    # Wait for dialog write time
    time.sleep(2)
    print("Assuming dialog writing done")
    Click()
    pass


def NavigatePostEntryMenus():
    NavigatePostEntryDialog()
    time.sleep(1)
    NavigateToPasswordEntry()
    pass


def NavigateToPasswordEntry():
    print("Assuming menu up")
    pyautogui.moveTo(MENU_DICT.get("RECIEVE_ENTRY"))
    Click()
    time.sleep(1.5)
    pyautogui.moveTo(MENU_DICT.get("PASSWORD_ENTRY"))
    Click()
    time.sleep(1)
    pass


def Click():
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    pass


def CheckArgs(args):
    if len(args) <= 1:
        raise RuntimeError("Cannot do anything.\nCall again with an argument.")
    pass


def ParsePassFile(filename):
    with open(filename, "r") as file:
        password_characters = [letter for line in file if not line.strip(
        ).startswith("//") for letter in line if letter in PASSWORD_DICT]
        passwords = ["".join(password_characters[i:i+PASSWORD_LENGTH])
                     for i in range(0, len(password_characters), PASSWORD_LENGTH)]
        for password in passwords:
            EnterPassword(password)
            time.sleep(1)
            if(password) is not passwords[-1]:
                NavigatePostEntryMenus()
            else:
                NavigatePostEntryDialog()
    pass


def CallCorrectFunction(argument):
    if path.exists(argument):
        ParsePassFile(argument)
    else:
        EnterPassword(argument)
    pass


if __name__ == "__main__":
    try:
        CheckArgs(sys.argv)
        for arg in sys.argv[1:]:
            CallCorrectFunction(arg)
    except RuntimeError as exc:
        print(exc)
    pass
