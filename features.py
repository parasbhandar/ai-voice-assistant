import os
from pipes import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
from engine.command import speak
from engine.config import ASSISTANT_NAME
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine
from urllib.parse import quote
import pygetwindow as gw
from engine.helper import extract_yt_term,remove_words
from hugchat import hugchat
con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
# Playing assiatnt sound function
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

# def whatsApp(mobile_no, message, flag, name):
#     if flag == 'message':
#         jarvis_message = "Message sent successfully to " + name
#     elif flag == 'call':
#         message = ''
#         jarvis_message = "Calling " + name
#     else:
#         message = ''
#         jarvis_message = "Starting video call with " + name

#     # Encode the message for URL
#     encoded_message = quote(message)
    
#     # Construct the WhatsApp URL
#     whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    
#     # Open WhatsApp with the constructed URL
#     full_command = f'start "" "{whatsapp_url}"'
#     subprocess.run(full_command, shell=True)

#     # Wait for WhatsApp to open
#     time.sleep(7)

#     # Simulate pressing "Enter" to send the message
#     pyautogui.press('enter')

#     # Speak the confirmation message
#     speak(jarvis_message)

# Update these coordinates after finding button positions
AUDIO_CALL_X, AUDIO_CALL_Y = 1829, 73  # Replace with real values
VIDEO_CALL_X, VIDEO_CALL_Y = 1769, 99  # Replace with real values

def activate_whatsapp():
    """Brings WhatsApp window to the foreground"""
    try:
        whatsapp_window = [win for win in gw.getWindowsWithTitle("WhatsApp") if win.visible]
        if whatsapp_window:
            whatsapp_window[0].activate()
            time.sleep(2)  # Ensure it gains focus
            return True
    except Exception as e:
        print("Could not focus WhatsApp:", e)
    return False

def whatsApp(mobile_no, message, flag, name):
    """Send message or make WhatsApp calls (audio/video)"""
    
    # Encode message for URL
    encoded_message = quote(message)
    
    # Open the WhatsApp chat
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    subprocess.run(f'start "" "{whatsapp_url}"', shell=True)

    # Wait for WhatsApp to open
    time.sleep(7)

    # Ensure WhatsApp is in focus
    if not activate_whatsapp():
        print("WhatsApp window not found! Ensure it's open.")
        return

    if flag == 'message':
        pyautogui.press('enter')  # Send message
        print(f"✅ Message sent to {name}")

    elif flag == 'call':
        print(f"📞 Calling {name}...")
        pyautogui.moveTo(AUDIO_CALL_X, AUDIO_CALL_Y)  # Move to audio call button
        time.sleep(1)
        pyautogui.click()  # Click the button

    elif flag == 'video':
        print(f"📹 Starting video call with {name}...")
        pyautogui.moveTo(VIDEO_CALL_X, VIDEO_CALL_Y)  # Move to video call button
        time.sleep(1)
        pyautogui.click()  # Click the button

    else:
        print("❌ Invalid command!")

# chat bot
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response