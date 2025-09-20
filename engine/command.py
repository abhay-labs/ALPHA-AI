# =====================================================
#  Project : ALPHA (Smart AI Assistant)
#  Author  : Abhay Jaiswal
#  Year    : 2025
#  Copyright (c) 2025 Abhay Jaiswal
#  All Rights Reserved.
#  Unauthorized copying or use is strictly prohibited.
#  Repo    : https://github.com/kingabhay2005/ALPHA
#  Unique Token : ALPHA-SEC-2025-ABJ-UNQ-9173X
# =====================================================


import pyttsx3
import speech_recognition as sr
import eel
import time

# Initialize pyttsx3 once
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 175)

# Global flag to track if mic is pressed
first_listen = False

def speak(text):
    text = str(text)
    """Speak the text and display it on the web interface."""
    try:
        eel.DisplayMessage(text)()
    except:
        pass
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    """Take voice input from user."""
    global first_listen
    first_listen = True
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...')
        try:
            eel.DisplayMessage('Listening...')()
        except:
            pass

        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=7, phrase_time_limit=12)
            print('Recognizing...')
            eel.DisplayMessage('Recognizing...')()
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            eel.DisplayMessage(query)()
            time.sleep(1)

            if first_listen:
                first_listen = False

            return query.lower()

        except sr.UnknownValueError:
            print("Could not understand audio")
            eel.DisplayMessage("Could not understand audio")()
            return ""

        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            eel.DisplayMessage(f"Could not request results; {e}")()
            return ""

        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            eel.DisplayMessage("Listening timed out...")()
            return ""

        except Exception as e:
            print(f"Some error occurred: {e}")
            eel.DisplayMessage(f"Error: {e}")()
            return ""

@eel.expose
def allCommands(message=None):
    """Handle all commands from user."""
    try:
        if not message or message == 1:
            query = takecommand()
            eel.senderText(query)
        else:
            query = message.lower()
            eel.senderText(query)

        print(f"Command received: {query}")

        if "open" in query:
            from engine.features import opencommand
            opencommand(query)

        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage

            # Find contact
            contact_no, name = findContact(query)

            if contact_no:  # check if contact is found
                speak("Which mode you want to use: WhatsApp or Mobile?")
                preference = takecommand().lower()
                print(preference)

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query:
                        speak("What message do you want to send?")
                        message = takecommand()
                        sendMessage(message, contact_no, name)  
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("Please try again. I didn't understand your request.")

                elif "whatsapp" in preference:
                    if "send message" in query:
                        speak("What message do you want to send?")
                        message = takecommand()
                    elif "phone call" in query:
                        message = "call"
                    else:
                        message = "video call"

                    whatsApp(contact_no, query, message, name)



        else:
            from engine.features import chatBot
            chatBot(query)

    except Exception as e:
        print(f"Error in allCommands: {e}")
    finally:
        time.sleep(1)
        try:
            eel.ShowHood()()
        except:
            pass

if __name__ == "__main__":
    eel.init('web')
    eel.start('index.html', size=(600, 400), block=False)
