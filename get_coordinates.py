#program to get whatsapp button coordinates for audio calling and video calling
import pyautogui
import time

# Get Audio Call Button Coordinates
print("Move your mouse to the AUDIO CALL button in WhatsApp, then wait...")
time.sleep(5)  # Gives you time to move the mouse
audio_x, audio_y = pyautogui.position()
print(f"Audio Call Button Coordinates: ({audio_x}, {audio_y})")

# Get Video Call Button Coordinates
print("Now move your mouse to the VIDEO CALL button in WhatsApp, then wait...")
time.sleep(5)
video_x, video_y = pyautogui.position()
print(f"Video Call Button Coordinates: ({video_x}, {video_y})")