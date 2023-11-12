import pyautogui
from PIL import ImageGrab
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread

### hei ###

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixie")
        self.is_enabled = False  # To track whether automation is enabled or not
        self.running_thread = None

        ### Setter størrelsen på GUI
        self.root.minsize(400, 400)
        self.root.maxsize(400, 400)

        ### Disabler muligheten for å resize vinduet
        self.root.resizable(width=False, height=False)

        self.enable_button = ttk.Button(root, text="Enable", command=self.enable)
        self.enable_button.pack()
        
        self.disable_button = ttk.Button(root, text="Disable", command=self.disable)
        self.disable_button.pack()
        self.disable_button.state(['disabled'])  # Initially, disable the disable button
        
        self.start_button = ttk.Button(root, text="Start", command=self.start_autoclicker)
        self.start_button.pack()
        
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_autoclicker)
        self.stop_button.pack()
        self.stop_button.state(['disabled'])  # Initially, disable the stop button

                # Button to eat food
        self.eat_food_button = ttk.Button(root, text="Eat Food", command=eatFood)
        self.eat_food_button.pack()
        
        self.bilder = ['sopp.PNG', 'ham.PNG', 'meat.PNG']

    def enable(self):
        self.is_enabled = True
        self.enable_button.state(['disabled'])
        self.disable_button.state(['!disabled'])
        
    def disable(self):
        self.is_enabled = False
        self.enable_button.state(['!disabled'])
        self.disable_button.state(['disabled'])
        
    def start_autoclicker(self):
        if not self.is_enabled:
            return

        self.start_button.state(['disabled'])
        self.stop_button.state(['!disabled'])
        
        self.running_thread = Thread(target=self.run_autoclicker)
        self.running_thread.start()
    
    def stop_autoclicker(self):
        if self.running_thread and self.running_thread.is_alive():
            self.running_thread.join()
        
        self.start_button.state(['!disabled'])
        self.stop_button.state(['disabled'])

    def run_autoclicker(self):
        while self.is_enabled:
            time.sleep(5)
            
            # sjekk pixelverdien på mana
            rgb_value = get_pixel_mana()
            correct_value = (68, 68, 255)

            if rgb_value == correct_value:
                print("Casting Utevo lux!")
                pyautogui.press('F9')
                time.sleep(1)
                eatFood()
            else:
                print("Not enough mana!")

def get_pixel_mana():
    # Capture the screen and get the pixel color at the cursor position
    screenshot = ImageGrab.grab()
    pixel_color = screenshot.getpixel((1822, 301))

    # Return the RGB value of the pixel color
    return pixel_color

def eatFood():
    bilder = ['Souls-bot\sopp.PNG', 'Souls-bot\ham.PNG', 'Souls-bot\meat.PNG']
    
    for bilde in bilder:
        #try:
        location = pyautogui.locateOnScreen(bilde, confidence=0.8)
        if location is not None:
            # Hvis bildet ble funnet, kan du utføre ønskede handlinger
            pyautogui.moveTo(location)
            pyautogui.rightClick()
            pyautogui.moveTo(3333, 475)
        #except Exception as e:
            #print(f'Feil oppstod: {e}')

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
