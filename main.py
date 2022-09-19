import pyautogui
import random
import time
while True:
    try:
        print("move mouse")
        pyautogui.moveTo(1000+random.randint(0,100), 100+random.randint(0,100), duration=0.25)
        time.sleep(200)
    except:
        pass