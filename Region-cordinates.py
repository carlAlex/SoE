import pyautogui
import time

# Prompt the user to prepare
print("Move the mouse to the top-left corner of the region and wait...")
time.sleep(6)  # Wait for 3 seconds

# Get the coordinates of the top-left corner
start_x, start_y = pyautogui.position()

# Prompt the user to prepare for the bottom-right corner
print("Move the mouse to the bottom-right corner of the region and wait...")
time.sleep(6)  # Wait for 3 seconds

# Get the coordinates of the bottom-right corner
end_x, end_y = pyautogui.position()

# Calculate width and height
width = end_x - start_x
height = end_y - start_y

# Display the coordinates and dimensions of the selected region
print(f"Selected Region: x={start_x}, y={start_y}, width={width}, height={height}")
