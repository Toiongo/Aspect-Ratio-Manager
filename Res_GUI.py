import PySimpleGUI as sg
import os, sys, math, re
from PIL import Image
from colorama import init
import winshell

init()


def deletefile(filename):
    if not os.path.exists(filename):
        return True
    filepath = os.path.abspath(filename)
    winshell.delete_file(filepath)


def t(number, decimals=0):
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def getaspectratio(aspectRatio):
    return {
        "4:3": [4, 3],
        "16:9": [16, 9],
        "16:10": [16, 10],
        "21:9": [21, 9],
        "32:9": [32, 9]
    }.get(aspectRatio, [16, 9])


aspect_ratios = ["4:3", "16:9", "16:10", "21:9", "32:9"]

sg.theme('DarkAmber')
layout = [[sg.Text("This program will delete every image that doesn't match chosen aspect ratio.")],
          [sg.Text("Image Directory:"), sg.InputText(), sg.FolderBrowse()],
          [sg.Text("Aspect ratio:"), sg.Combo(default_value="16:9", values=aspect_ratios, size=(11, 5), key='-LIST-', enable_events=True, readonly=True)],
          [sg.Button('Start', size=(10, 1)), sg.Button('Close', size=(10, 1))],
          [sg.Text("Made by: Toiongog@gmail.com")]]

window = sg.Window('Aspect Ratio Manager', layout)
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        break
    if event == 'Start':

        folder = None
        if len(values[0]) == 0:
            print("Error, choose existing folder with your image files.")
            continue
        folder = re.findall("^.:\/\w+$", values[0])
        if not folder or folder is None or len(folder) == 0:
            print("Error, choose existing folder with your image files.")
            continue

        folder[0] = folder[0].replace("/", "\\") + "\\"

        os.chdir(folder[0])

        for infile in os.listdir(folder[0]):
            if os.path.isdir(os.path.abspath(infile)) or infile == "Res_GUI.py":
                continue

            try:
                with Image.open(infile) as im:
                    if t(im.size[0] / im.size[1], 2) == t(getaspectratio(values['-LIST-'])[0] / getaspectratio(values['-LIST-'])[1], 2):
                        print(BColors.OKGREEN + infile, im.format, "%dx%d" % im.size, im.mode, t(im.size[0] / im.size[1], 2))
                    else:
                        print(BColors.FAIL + infile, im.format, "%dx%d" % im.size, im.mode, t(im.size[0] / im.size[1], 2))
                        im.close()
                        deletefile(infile)
            except OSError:
                print(OSError)

window.close()
