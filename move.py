import pyautogui

res = pyautogui.locateOnScreen('images/nox_icon_on_taskbar.png', confidence=0.8)
print(res)