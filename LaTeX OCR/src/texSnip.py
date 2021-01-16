import pyautogui
from pynput.keyboard import Listener

import util
from config import Config
from minu import path

pressed = set()


def on_press(key):
    keyStr = str(key).replace("'", "")
    print(keyStr + " press") if Config.VERBOSE else ""
    pressed.add(keyStr)


def on_release(key):
    oldPressed = pressed.copy()
    keyStr = str(key).replace("'", "")
    print(keyStr + " release") if Config.VERBOSE else ""
    try:
        pressed.remove(keyStr)
    except:
        pass

    if keyStr in Config.combo and all([c in oldPressed for c in Config.combo]):
        pressed.clear()
        util.run()

    if keyStr in Config.hwp_combo and all([c in oldPressed for c in Config.hwp_combo]):
        pressed.clear()
        pyautogui.keyUp('alt')
        pyautogui.keyDown('ctrl')
        pyautogui.press('n')
        pyautogui.press('m')
        pyautogui.keyUp('ctrl')
        pyautogui.sleep(.5)

        pyautogui.keyDown('alt')
        pyautogui.press('m')
        pyautogui.keyUp('alt')
        pyautogui.sleep(.5)

        pyautogui.write(path.replace('/', '\\'))
        pyautogui.press('enter')
        pyautogui.sleep(.5)

    if key == Config.terminate:  # Stop
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
