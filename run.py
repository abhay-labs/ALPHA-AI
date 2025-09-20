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

# To run alpha
import multiprocessing
import subprocess


def startAlpha():
    # code for process 1
    print("Process 1 is running.")
    from main import start
    start()

# To run hotword
def listenHotword():
    # code for process 2
    print("process 2 is running.")
    from engine.features import hotword
    hotword()


# start for both process
if __name__=='__main__':
    p1 = multiprocessing.Process(target=startAlpha)
    p2 = multiprocessing.Process(target=listenHotword)
    p1.start()
    subprocess.call([r'device.bat'])
    p2.start()
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("System stop")






