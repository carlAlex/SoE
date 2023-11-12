import pyautogui
import time

# Function to get the progress percentage
def get_progress_percentage(region, target_color):
    screenshot = pyautogui.screenshot(region=region)
    width, height = screenshot.size

    target_pixels = 0
    for x in range(width):
        for y in range(height):
            pixel_color = screenshot.getpixel((x, y))
            if pixel_color == target_color:
                target_pixels += 1

    total_pixels = width * height
    percentage = (target_pixels / total_pixels) * 100

    return percentage

# Specify the region and target color
region = (1731, 258, 177, 0)
target_color = (68, 68, 255)

# Example: Track the progress every 1 second for 10 seconds
for _ in range(10):
    percentage = get_progress_percentage(region, target_color)
    print(f"Progress: {percentage:.2f}%")
    time.sleep(1)








#import pyautogui


#pyautogui.displayMousePosition()
#print()
