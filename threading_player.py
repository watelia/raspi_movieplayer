import json
import os
import sys
from VideoPlayer import VideoPlayer
import RPi.GPIO as GPIO
from time import sleep
import msvcrt

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


def keyboard_event():
    print("1")


try:
    while True:
        if msvcrt.kbhit():
            kb = msvcrt.getch

        if cnt >= movies_num:
            cnt = 0

        # print("動画を再生してください")

        if GPIO.input(PIN_INPUT) == GPIO.LOW:
            # print("path = " + path_next)
            vp.play(path_next)
            path = path_next
            sleep(1)

            while vp.playing is True:
                continue

            path_next = str(json_data["movies"][cnt]["next"])

            cnt += 1

        if GPIO.input(PIN_PAUSE) == GPIO.LOW:
            # print("もう一度再生", end="/n")
            # print("path = " + path)
            vp.play(path)

            while vp.playing is True:
                continue
except(KeyboardInterrupt, SystemExit, SystemError):
    sys.quit()
