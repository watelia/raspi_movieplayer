import json
import os
import sys
from VideoPlayer import VideoPlayer
import RPi.GPIO as GPIO
# from time import sleep
# import keyboard
# import tkinter as Tk


os.environ.__setitem__('DISPLAY', ':0.0')


vp = VideoPlayer()


PIN_INPUT = 12
PIN_PAUSE = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_INPUT, GPIO.IN)
GPIO.setup(PIN_PAUSE, GPIO.IN)


json_open = open('MovieList.json', 'r')
json_data = json.load(json_open)
movies_num = len(json_data["movies"])


ENTRY_PATH_ID = json_data["entry"]
ENTRY_PATH = json_data["movies"][ENTRY_PATH_ID]["path"]
ENTRY_PATH_NEXT = json_data["movies"][ENTRY_PATH_ID]["next"]
ENTRY_PATH_PREVIOUS = json_data["movies"][ENTRY_PATH_ID]["previous"]

path = ""
path_next = ""
path_previous = ""


cnt = 0


def emptycb():
    print("No Signal")


vp.set_callback_end(emptycb)

path = ENTRY_PATH
path_next = ENTRY_PATH
path_previous = ENTRY_PATH_PREVIOUS


def keyboard_event(event):
    key = event.keysym
    if key == "Escape":
        GPIO.cleanup()
        vp.destroy()
        sys.exit()


vp.bind_press_event(keyboard_event)
vp.update()

try:
    while True:
        vp.update()

        if cnt >= movies_num:
            cnt = 0

        if GPIO.input(PIN_INPUT) == GPIO.LOW:
            vp.play(path_next)
            path = path_next

            while vp.playing is True:
                vp.update()
                continue

            path_next = str(json_data["movies"][cnt]["next"])

            cnt += 1

        if GPIO.input(PIN_PAUSE) == GPIO.LOW:
            vp.play(path)

            while vp.playing is True:
                vp.update()
                continue
except(KeyboardInterrupt, SystemExit, SystemError):
    GPIO.cleanup()
    sys.exit()
