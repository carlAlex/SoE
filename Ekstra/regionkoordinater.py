import pyautogui

def on_click(x, y, button, pressed):
    if pressed:
        print(f"Mouse clicked at coordinates: {x}, {y}")



pyautogui.displayMousePosition()

# Keep the script running
pyautogui.alert("Click OK to exit the script.")
