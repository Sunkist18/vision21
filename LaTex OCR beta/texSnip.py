import pyautogui
from pynput.keyboard import Listener

import do
import util
from config import Config

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
        do.do_()

    if key == Config.terminate:  # Stop
        return False


while True:
    try:
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except:
        pass
