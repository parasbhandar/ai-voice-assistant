import pyautogui
import time

print("Move your mouse to the Audio Call button and wait...")
time.sleep(5)  # Gives you time to move the mouse

x, y = pyautogui.position()
print(f"Audio Call Button Coordinates: ({x}, {y})")

print("Now move your mouse to the Video Call button and wait...")
time.sleep(5)

x, y = pyautogui.position()
print(f"Video Call Button Coordinates: ({x}, {y})")