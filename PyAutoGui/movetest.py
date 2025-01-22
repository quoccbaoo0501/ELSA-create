
import pyautogui
import time 


pyautogui.mouseDown()
time.sleep(0.5)
    
pyautogui.moveTo(1000, 100)
pyautogui.mouseUp()

print(pyautogui.position())