import pyautogui
import time

# Get the current mouse cursor position
mouse_x, mouse_y = pyautogui.position()

# Wait for a moment to give you time to check the location
time.sleep(5)  # You can adjust the delay time as needed

# Get the RGB color at the mouse cursor position
color = pyautogui.pixel(mouse_x, mouse_y)

# Print the RGB values
print(f"RGB values at mouse cursor ({mouse_x}, {mouse_y}): ({color[0]}, {color[1]}, {color[2]})")
