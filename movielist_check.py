import tkinter as tk
import os
import sys
from concurrent.futures import ThreadPoolExecutor


os.environ.__setitem__('DISPLAY', ':0.0')

__display = tk.Tk()


def keyboard_event(event):
    key = event.keysym
    if key == "Escape":
        sys.exit()


with ThreadPoolExecutor(2) as e:
    vp.bind_press_event(keyboard_event)


__display.bind("<KeyPress>", keyboard_event)
__display.mainloop()
