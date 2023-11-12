import pyautogui

# Definer regionen du vil søke i (venstre, topp, bredde, høyde)
region = (3424, 708, 176, 372)

# Filnavnet på bildet du vil søke etter
mushroom = "mushroom.PNG"

# Søk etter bildet innenfor den angitte regionen
pos = pyautogui.locateOnScreen('mushroom.png', region=region)

# Hvis bildet ble funnet, skriv ut koordinatene
if pos:
    x, y = pyautogui.center(pos)
    print(f"Bildet '{mushroom}' ble funnet på koordinater: ({x}, {y})")
else:
    print(f"Bildet '{mushroom}' ble ikke funnet i den angitte regionen.")
