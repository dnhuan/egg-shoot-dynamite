import time
import tkinter as tk
import keyboard
from PIL import ImageGrab, ImageTk
from utils import process_image
from directKeys import click

isDetecting = False
isActivated = True

width = 700
height = 870
offset_x = 280
offset_y = 330
lastClick = time.time()

# delete and recreate tmp folder
import shutil
import os

if os.path.exists("tmp"):
    shutil.rmtree("tmp")

os.mkdir("tmp")


def capture_screenshot():
    screenshot = ImageGrab.grab(bbox=(offset_x, offset_y, offset_x + width, offset_y + height))
    return screenshot

def process_target(target):
    target = target.tolist()
    if isActivated:
        global lastClick
        if time.time() - lastClick > 0.1:
            lastClick = time.time()
            click(target[0] + offset_x, target[1] + offset_y)


def update_screenshot_label():
    screenshot = capture_screenshot()
    if isActivated:
        processed_image, target = process_image(screenshot)
    else:
        processed_image, target = screenshot, None
    screenshot_image = ImageTk.PhotoImage(processed_image)
    screenshot_label.config(image=screenshot_image)
    screenshot_label.image = screenshot_image
    root.after(1, update_screenshot_label) 
    if isDetecting and target is not None:
        process_target(target)

    

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f"{width}x{height}+1050+450")
    root.title("Controls")
    root.resizable(False, False)
    root.wm_attributes("-topmost", 1)
    root.attributes('-topmost', 1)
    screenshot_label = tk.Label(root)
    screenshot_label.pack()
    update_screenshot_label()

    
    def toggle_isActivated():           
        global isActivated
        isActivated = not isActivated

    def toggle_isDetecting():
        global isDetecting
        if isActivated:
         isDetecting = not isDetecting

    keyboard.add_hotkey('tab', toggle_isActivated)
    keyboard.add_hotkey('space', toggle_isDetecting)

    keyboard.add_hotkey('esc', lambda: root.destroy())

    root.mainloop()


    
