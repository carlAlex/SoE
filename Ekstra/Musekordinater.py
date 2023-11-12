import time
import pyautogui



def print_mouse_position_for_5_seconds():
    end_time = time.time() + 5  # Run for 5 seconds from the current time

    while time.time() < end_time:
        x, y = pyautogui.position()
        print(f"Mouse position: ({x}, {y})")
        time.sleep(6)  # Wait for 1 second before printing again

if __name__ == "__main__":
    while True:

        time.sleep(1)
        print_mouse_position_for_5_seconds()