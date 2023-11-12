import pyautogui
from PIL import ImageGrab
import time

#def get_pixel_color_under_mouse():
#    # Get the
#    # current position of the mouse cursor
#    x, y = pyautogui.position()
#
#    # Capture the screen and get the pixel color at the cursor position
#    screenshot = ImageGrab.grab()
#    pixel_color = screenshot.getpixel((x, y))
#
#   # Return the RGB value of the pixel color
#    return pixel_color

def get_pixel_mana():
    # Capture the screen and get the pixel color at the cursor position
    screenshot = ImageGrab.grab()
    pixel_color = screenshot.getpixel((1822, 301))

    # Return the RGB value of the pixel color
    return pixel_color



#### DENNE FUNKER : TRY og except er en slags failsafe !!!!!!!####
#def eatFood():
#    try:
#        pyautogui.locateOnScreen('sopp.PNG', confidence=0.8)        
#        pyautogui.moveTo('sopp.PNG')        
#        pyautogui.rightClick()
#        pyautogui.moveTo(3333, 475)     
#    except:
#        Exception

def eatFood():
    bilder = ['sopp.PNG', 'ham.PNG', 'meat.PNG']
    
    for bilde in bilder:
        try:
            location = pyautogui.locateOnScreen(bilde, confidence=0.8)
            if location is not None:
                # Hvis bildet ble funnet, kan du utføre ønskede handlinger
                pyautogui.moveTo(location)
                pyautogui.rightClick()
                pyautogui.moveTo(3333, 475)
        except Exception as e:
            print(f'Feil oppstod: {e}')

#def print_mouse_position_for_5_seconds():
#    end_time = time.time() + 5  # Run for 5 seconds from the current time
#
#    while time.time() < end_time:
#        x, y = pyautogui.position()
#        print(f"Mouse position: ({x}, {y})")
#        time.sleep(1)  # Wait for 1 second before printing again

if __name__ == "__main__":
    while True:
        
        #input("Press Enter to capture pixel color...")
        #print_mouse_position_for_5_seconds()
        
        # vent 5 sekund
        time.sleep(5)
        
        # finn fargeverdi
        #input("Press Enter to capture pixel color...")
        #rgb_value = get_pixel_color_under_mouse()
        #print(rgb_value)

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
            
            
## Hvis man bruker funksjonen her, vil at høyreklikke hele tiden###


        #print(f"RGB Value: {rgb_value}")