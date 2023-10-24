import tkinter as tk
from win32gui import SetWindowLong, GetWindowLong, SetLayeredWindowAttributes
from win32con import WS_EX_LAYERED, WS_EX_TRANSPARENT, GWL_EXSTYLE
import keyboard
import numpy as np
import cv2
from PIL import ImageGrab, ImageTk
from utils import process_image

def set_clickthrough(hwnd):
    try:
        styles = GetWindowLong(hwnd, GWL_EXSTYLE)
        styles = WS_EX_LAYERED | WS_EX_TRANSPARENT
        SetWindowLong(hwnd, GWL_EXSTYLE, styles)
        SetLayeredWindowAttributes(hwnd, 0, 255, 0x00000001)
    except Exception as e:
        print(e)

isActivated = True

width = 700
height = 870
offset_x = 280
offset_y = 330

def capture_screenshot():
    screenshot = ImageGrab.grab(bbox=(offset_x, offset_y, offset_x + width, offset_y + height))
    return screenshot

def update_screenshot_label():
    screenshot = capture_screenshot()
    if isActivated:
        processed_image = process_image(screenshot)
    else:
        processed_image = screenshot
    screenshot_image = ImageTk.PhotoImage(processed_image)
    screenshot_label.config(image=screenshot_image)
    screenshot_label.image = screenshot_image  # keep a reference to the image
    root.after(100, update_screenshot_label) 

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

    keyboard.add_hotkey('tab', toggle_isActivated)


    keyboard.add_hotkey('esc', lambda: root.destroy())

    root.mainloop()


    
