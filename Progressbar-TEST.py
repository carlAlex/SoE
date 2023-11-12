import pyautogui
import time

def get_progress_percentage(region, target_color):
    screenshot = pyautogui.screenshot(region=region)
    width, height = screenshot.size

    if width == 0 or height == 0:
        return 0.0

    total_pixels = width * height
    if total_pixels == 0:
        return 0.0

    target_pixels = 0
    x_position = 0  # Initialize x_position to handle the case where no target color is found
    for x in range(width):
        for y in range(height):
            pixel_color = screenshot.getpixel((x, y))
            if pixel_color == target_color:
                target_pixels += 1
                x_position = x

    # If no target color is found, return 0.0%
    if target_pixels == 0:
        return 0.0

    # Calculate progress based on the horizontal position
    progress_percentage = (x_position / width) * 100
    return progress_percentage

# Specify the region and target color
region = (1730, 258, 180, 4)
target_color = (68, 68, 255)  # Adjust the target color as needed

# Example: Track the progress every 1 second for 10 seconds
for _ in range(100):
    percentage = get_progress_percentage(region, target_color)
    print(f"Progress: {percentage:.2f}%")
    time.sleep(0.5)
