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

import os
import re
from urllib.parse import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pvporcupine
import pyaudio
import pyautogui
import pyttsx3
from engine.command import speak
from engine.config import ASSISTANT_NAME

import pywhatkit as kit

from engine.helper import extract_yt_term, remove_words

import google.generativeai as genai

con = sqlite3.connect("Alpha.db")
cursor = con.cursor()

# playing assistant sound function

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\alphaopenaudio.mp3"
    playsound(music_dir)


def opencommand(query):
    query = query.lower()
    query = query.replace(ASSISTANT_NAME.lower(), "")
    query = query.replace("open", "")
    query = re.sub(r'\s+', ' ', query)  # ✅ multiple spaces ko ek space mein convert karo

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()   

            if len(results) != 0:
                speak("Opening"+query)
                os.startfile(results[0][0])

            elif len(results) == 0:
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening"+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening"+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("Some thing went wrong")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)



def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        # pre trained keywords
        porcupine=pvporcupine.create(keywords=["alexa"])
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)

        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keywords comes from mic
            keyword_index=porcupine.process(keyword)

            # checking first keyword detected for not
            if keyword_index>=0:
                print("hotword detection")

                # pressing shortcut key win+j
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



# Find Contacts
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
    




def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        alpha_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        alpha_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        alpha_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message)

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(alpha_message)
    




####  using gemini api key #######################################  niche kuch mat hatana  ##############

#### chat function

# --- Configuration ---
##     /////////////////////////////////////////// Put your Gemini API key /////////////////////////////////////////////////////////////////////////  # apni API key yahan daalo

# --- Initialize Model ---
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Initialize Text-to-Speech Engine ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# --- Chatbot Function ---
def chatBot(query):
    user_input = query.lower()

    # Generate response using the model
    response = model.generate_content(user_input)
    answer = response.text

    print("Alpha says:", answer)
    speak(answer)

    return answer



### speak function

# --- Configuration ---
#/////////////////////////////////////////////////   Put your Gemini API key    //////////////////////////////////////////////////  # apni API key yahan daalo

# --- Initialize Model ---
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Initialize Text-to-Speech Engine ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

# --- Speak Function with Display ---
def speak(text):
    """Speak the text and also display it on the web interface."""
    try:
        eel.DisplayMessage(text)()      # Display message in web interface
        eel.receiverText(text)()       # Optional: show text in another widget if needed
    except Exception as e:
        print("Eel error:", e)
    
    engine.say(text)
    engine.runAndWait()

# --- Chatbot Function ---
def chatBot(query):
    user_input = query.lower()

    # Generate response using the model
    response = model.generate_content(user_input)
    answer = response.text

    print("Alpha says:", answer)
    speak(answer)

    return answer




### Android automation

from engine.features import findContact, whatsApp

# Set your ADB path here
ADB_PATH = r"C:\platform-tools\adb.exe"  # <-- yaha adb.exe ka full path daalo

def makeCall(name, mobileNo):
    # Clean number
    mobileNo = ''.join(filter(lambda x: x.isdigit() or x=='+', mobileNo))
    speak(f"Calling {name}...")

    # Use full ADB path
    command = f'"{ADB_PATH}" shell am start -a android.intent.action.CALL -d tel:{mobileNo}'
    os.system(command)



# to send message

def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvent, adbInput
    # prepare message and number
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("Sending message...")

    # go back to home
    goback(4)
    time.sleep(1)
    keyEvent(3)  # home button

    # ---------------- Tap coordinates for Realme C31 ----------------
    # open SMS app (adjusted)
    tapEvent(87, 1426)  # bottom dock, left side (approx location of messaging icon)

    # start chat / new message
    tapEvent(623, 1444)  # bottom-right "new message" icon

    # search mobile number
    adbInput(mobileNo)

    # tap on contact (first search result)
    tapEvent(230, 417)  # middle of first contact result

    # tap on message input box
    tapEvent(231, 1485)

    # type message
    adbInput(message)

    # send button
    tapEvent(651, 923)
    speak("Message send succesfully to"+name)




def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvent, adbInput

    # Clean number: sirf digits
    mobileNo = ''.join(filter(lambda x: x.isdigit(), mobileNo))

    message = replace_spaces_with_percent_s(message)

    speak("Sending message...")

    goback(4)
    time.sleep(1)
    keyEvent(3)  # home button

    ############## sending message
    # open SMS app
    tapEvent(87, 1426)
    time.sleep(2)

    # start new message
    tapEvent(623, 1444)
    time.sleep(2)

    # tap on search bar
    search_x, search_y = 318, 275  # aap apne phone ke hisab se change karo
    tapEvent(search_x, search_y)
    time.sleep(2)

    print("Typing mobile number:", mobileNo)
    adbInput(mobileNo)
    time.sleep(2)

    # select first contact
    tapEvent(230, 417)
    time.sleep(2)

    # tap on input box
    tapEvent(231, 1485)
    time.sleep(1)

    # type message
    print("Typing message:", message)
    adbInput(message)
    time.sleep(1)

    # send button
    tapEvent(651, 923)
    time.sleep(1)

    speak("Message sent successfully to " + name)
    

