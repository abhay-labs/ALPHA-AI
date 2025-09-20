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
import threading
import eel
import time
from engine.features import *
from engine.command import *
from engine.auth import recognize

def start():
    eel.init("www")

    print("🔒 Starting face authentication...")

    try:
        # Face authentication
        flag = recognize.AuthenticateFace()

        if flag:
            print("✅ Face authentication successful!")

            # Play assistant sound (optional thread)
            threading.Thread(target=playAssistantSound, daemon=True).start()

            # Open Edge browser only after successful authentication
            time.sleep(0.1)  # optional minimal delay
            try:
                os.system('start msedge.exe --app="http://localhost:8000/index.html"')
            except Exception as e:
                print("Could not open Edge:", e)

            # Start Eel server
            eel.start('index.html', mode=None, host='localhost', port=8000, block=True)

        else:
            print("❌ Face authentication failed. Project will not start.")

    except Exception as e:
        print("Error during authentication or startup:", e)
