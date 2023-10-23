import tkinter as tk
from win32gui import SetWindowLong, GetWindowLong, SetLayeredWindowAttributes
from win32con import WS_EX_LAYERED, WS_EX_TRANSPARENT, GWL_EXSTYLE
import keyboard

def set_clickthrough(hwnd):
    try:
        styles = GetWindowLong(hwnd, GWL_EXSTYLE)
        styles = WS_EX_LAYERED | WS_EX_TRANSPARENT
        SetWindowLong(hwnd, GWL_EXSTYLE, styles)
        SetLayeredWindowAttributes(hwnd, 0, 255, 0x00000001)
    except Exception as e:
        print(e)

isActivated = False

width = 680
height = 1080

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry(f'{width}x{height}+282+150')
    # root.overrideredirect(True)
    root.attributes("-alpha", 0.10)
    root.wm_attributes("-topmost", 1)
    root.attributes('-transparentcolor', '#ffffff', '-topmost', 1)
    root.resizable(False, False)
    set_clickthrough(root.winfo_id())

    canvas = tk.Canvas(root, width=width, height=height, bd=0, highlightthickness=6, highlightbackground="green")
    canvas.pack()

    size_position_label = tk.Label(root, text="", font=("Arial", 12))
    size_position_label.pack()



    # create a separate window for controls
    controls = tk.Toplevel(root)
    controls.geometry("300x200+1400+400")
    controls.title("Controls")
    controls.resizable(False, False)

    # create a label for isActivated
    isActivated_label = tk.Label(controls, text=f"isActivated: {isActivated}", font=("Arial", 12))
    isActivated_label.pack()
    
    # use spacebar to toggle isActivated
    def toggle_isActivated():
        global isActivated
        isActivated = not isActivated
        isActivated_label.config(text=f"isActivated: {isActivated}")

    keyboard.add_hotkey('space', toggle_isActivated)

    # use escape to quit
    def quit():
        root.destroy()
        controls.destroy()

    keyboard.add_hotkey('esc', quit)

    root.mainloop()


    
