import pyttsx3
import speech_recognition as sr
import eel
import time
def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    engine.setProperty('rate', 174)     # setting up new voice rate
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


def takecommand():

    r=sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening...')
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source,10,6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        
    except Exception as e:
        return ""
    
    return query.lower()


@eel.expose
def allCommands(message=1):

    if message==1:
        query=takecommand()
        print(query)
        eel.senderText(query)
    else:
        query=message
        eel.senderText(query)
    try:

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
    
            contact_no, name = findContact(query)
            if contact_no != 0:

                if "send message" in query:
                    speak("What message to send?")
                    query = takecommand()  # Get the actual message text
                    flag = 'message'  # Set flag for sending a message
                elif "phone call" in query:
                    flag = 'call'  # Set flag for voice call
                    query = ''  # No text needed for calls
                else:
                    flag = 'video'  # Set flag for video call
                    query = ''  # No text needed for calls

                whatsApp(contact_no, query, flag, name)  # Pass the correct flag

        else:
            #print("not run")
            from engine.features import chatBot
            chatBot(query)

    except:
        print("error")
    eel.ShowHood()