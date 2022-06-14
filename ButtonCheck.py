from time import sleep
import RPi.GPIO as GPIO
# import keyboard


PIN_TEST = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_TEST, GPIO.IN)


# target_key = ['space', 'a']


try:
    while True:
        sleep(0.02)
        if GPIO.input(PIN_TEST) == GPIO.HIGH:
            print("HIGH")
        if GPIO.input(PIN_TEST) == GPIO.LOW:
            print("LOW")
except(KeyboardInterrupt, SystemExit, SystemError):
    print('exit')
    GPIO.cleanup()
