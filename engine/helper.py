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
import time


def extract_yt_term(command):
    # Patterns try karte hain in order of priority
    patterns = [
        r'play\s+(.*?)\s+on\s+youtube',  # play ... on youtube
        r'play\s+(.*?)\s+youtube',       # play ... youtube
        r'youtube\s+(.*)',                # youtube ... 
        r'play\s+(.*)',                   # play ... 
        r'(.*)\s+youtube'                 # ... youtube at the end
    ]
    
    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            return match.group(1).strip()  
    return None



def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string



# Set your ADB path here
ADB_PATH = r"C:\platform-tools\adb.exe"

# key events like receive call, stop call, go back
def keyEvent(key_code):
    command = f'"{ADB_PATH}" shell input keyevent {key_code}'
    os.system(command)
    time.sleep(1)

# tap event used to tap anywhere on screen
def tapEvent(x, y):
    command = f'"{ADB_PATH}" shell input tap {x} {y}'
    os.system(command)
    time.sleep(1)

# Input event is used to insert text
def adbInput(message):
    command = f'"{ADB_PATH}" shell input text "{message}"'
    os.system(command)
    time.sleep(1)

# to go complete back
def goback(key_code):
    for i in range(6):
        keyEvent(key_code)

# replace spaces with %s for message typing
def replace_spaces_with_percent_s(input_string):
    return input_string.strip().replace(' ', '%s')


