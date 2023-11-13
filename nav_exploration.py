import numpy as np
import win32gui, win32ui, win32con
import mss
import cv2 as cv
from threading import Thread, Lock
import pyautogui
from find_food_test import WindowCapture, Detection
import time

def get_progress_percentage(region, target_color, step=1):
    screenshot = pyautogui.screenshot(region=region)
    width, height = screenshot.size

    if width == 0 or height == 0:
        return 0.0

    for x in range(width-1, -1, -step):
        for y in range(height-1, -1, -step):
            pixel_color = screenshot.getpixel((x, y))
            if pixel_color == target_color:
                return (x / width) * 100

    return 0.0

def get_battlewindow_health(region, step=1):
    screenshot = pyautogui.screenshot(region=region)
    width, height = screenshot.size
    print(f"width: {width}, height: {height}")

    if width == 0 or height == 0:
        return 0.0

    gray_pixels = width
    for x in range(width-1, -1, -step):
        r, g, b = screenshot.getpixel((x, 0))
        if (60 <= r <= 90) and (60 <= g <= 90) and (60 <= b <= 90):  # Check if the pixel is gray
            gray_pixels -= 1
        else:
            print(f'Pixel color: {r, g, b}')
            return (gray_pixels / width) * 100

    return 0.0

def bw_has_names(region):
    x, y, width, height = region

    for i in range(0, 10):
        region = (x, y + (i * 25), width, height)
        # print(f'Current x, y is {x}, {y + (i * 25)}')
        screenshot = pyautogui.screenshot(region=region)
        width, height = screenshot.size
        entity_found = False
        # print(f'Looking for entity at slot {i}')
        for pix in range(width):
            if not entity_found:
                r, g, b = screenshot.getpixel((pix, 0))
                if r == 136 and g == 136 and b == 136:
                    print(f'  **Entity FOUND at slot {i}')
                    entity_found = True
        if not entity_found:
            print(f'  **No entity found at slot {i}')
        
                        

# If there is a name above the health bar, rgb(136, 136, 136)
# the names start at 1313, 130(155 etc + 25)
region_entity_start = (1313, 130, 60, 1)
bw_has_names(region_entity_start)

# The first bar is at (1313, 145) and is 138 pixels wide
# 145, 170, 195
# region_health = (1313, 145, 138, 1)
# for i in range(15):
#     print(get_battlewindow_health(region_health))
#     time.sleep(1)

# wc = WindowCapture('Souls Of Elysium - BRUKERNAVN')
# Uncomment denne for å ta screenshot med win32gui
# image = wc.get_screenshot()
# cv.imwrite('SoE\img\get_screenshot.png', image)

# det = Detection()
# det.update(wc.get_screenshot())
# if det.find_needle():
#     print('Found!')
#     game_win_x = wc.offset_x
#     game_win_y = wc.offset_y
#     # move mouse with pyautogui to the center of the needle image
#     pyautogui.moveTo(game_win_x + det.needle_point[0], game_win_y + det.needle_point[1])
# else:
#     print('Not found!')