import numpy as np
import win32gui, win32ui, win32con
import mss
import cv2 as cv
from threading import Thread, Lock
import pyautogui
from find_food_test import WindowCapture, Detection
import time
import dxcam
import pyautogui
from pynput.keyboard import Controller, Key


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
    # print(f"width: {width}, height: {height}")

    if width == 0 or height == 0:
        return 0.0

    gray_pixels = width
    for x in range(width-1, -1, -step):
        r, g, b = screenshot.getpixel((x, 0))
        if (60 <= r <= 90) and (60 <= g <= 90) and (60 <= b <= 90):  # Check if the pixel is gray
            gray_pixels -= 1
        else:
            # print(f'Pixel color: {r, g, b}')
            return (gray_pixels / width) * 100

    return 0.0

def bw_entity_state(region):
    x, y, width, height = region
    ent_in_battlewindow = 0

    for i in range(0, 10):
        region = (x, y + (i * 25), width, height)
        # print(f'Current x, y is {x}, {y + (i * 25)}')
        screenshot = pyautogui.screenshot(region=region)
        width, height = screenshot.size
        entity_found = False
        # print(f'Looking for entity at slot {i}')
        for pix in range(width):
            if not entity_found:
                # Looks where the name is. If it finds gray letters...
                r, g, b = screenshot.getpixel((pix, 0))
                if r == 136 and g == 136 and b == 136:
                    # print(f'  **Entity FOUND at slot {i}')
                    ent_in_battlewindow += 1
                    entity_found = True
        if not entity_found:
            #print(f'  **No entity found at slot {i}')
            pass
    return ent_in_battlewindow

def click_food_if_req():
    region = (2375, 184, 174, 1)
    target_color = (255, 68, 68)
    percentage = get_progress_percentage(region, target_color)
    print(f"Health: {percentage:.2f}%")
    if percentage < 85.0:
        print("Health: **LOW** Eating food..")
        pyautogui.moveTo(2421, 483)
        pyautogui.click(button='right')
        time.sleep(0.1)

# using pynput because SoE did not like pyautogui
keyboard = Controller()
print("waiting..")
time.sleep(2)
print("move to spiders..")

# Farm spiders script - SETUP:
BW_MENU_CLICK = (1296, 138)
ATTACK_CLICK_OFFS = (20, 20)
FOLLOW_CLICK_OFFS = (20, 40)

camera = dxcam.create()  # returns a DXCamera instance on primary monitor
left, top = 2372, 36
right, bottom = 2550, 175
region = (left, top, right, bottom)

for _ in range(3):
    # Player starts at base of stairs
    # Player walks up stairs
    print("Walking up stairs..")
    for _ in range(5):
        keyboard.press(Key.right)
        keyboard.release(Key.right)
        time.sleep(0.5)
    # wait for player to move
    time.sleep(1.5)
    # Spiders move towards player, get_battlewindow_health() is called
    region_health = (1313, 145, 138, 1)
    health = get_battlewindow_health(region_health) 
    while health > 0.0:
        click_food_if_req()
        print("**ATTACKING spiders..")
        keyboard.press(Key.f1)
        keyboard.release(Key.f1)
        time.sleep(3)
        pyautogui.moveTo(x=BW_MENU_CLICK[0], y=BW_MENU_CLICK[1])
        pyautogui.click(button='right')
        time.sleep(0.1)
        print("FOLLOWING spiders..")
        pyautogui.moveTo(x=BW_MENU_CLICK[0] + FOLLOW_CLICK_OFFS[0], y=BW_MENU_CLICK[1] + FOLLOW_CLICK_OFFS[1])
        pyautogui.click(button='left')
        time.sleep(2)
        health = get_battlewindow_health(region_health)
    # Wait in case player still moving
    print("All dead, waiting to find the stairs..")
    time.sleep(1)
    # Right click dead spider
    det = Detection()
    det.set_needle_image('SoE\\img\\dn_arrow.png')

    
    frame = camera.grab(region=region)
    det.update(frame)
    if det.find_needle():
        print('Found!')
        pyautogui.moveTo(left + det.needle_point[0] + 5, top + det.needle_point[1] - 26)
        pyautogui.click(button='left')
        print("**WALKING to stairs..")
        time.sleep(7.5)
        print("Resetting position..")
        for _ in range(6):
            keyboard.press(Key.left)
            keyboard.release(Key.left)
            time.sleep(0.6)
        print("Give spiders some time to respawn..")
        time.sleep(3)
    else:
        print('Not found!')
    # Hover mouse over loot slot, see if "Gold coin" is found
    # If found, drag coin to inventory
    # If not found, right click again to close loot dlg, drag corpse to inventory
    # Click OK button if required
    # Close loot window
    # Drag corpse to inventory
    # Click flower to move to it
    # Walk back down stairs and move away
    # Drop corpses
    # Repeat
