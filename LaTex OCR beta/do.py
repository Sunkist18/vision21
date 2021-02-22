import latex2mathml.converter
import pyautogui
import pyperclip

import balloons

path = 'C:/Users/user/Desktop/latex_cmw.mml'


def ctrl(key, interval=0.1):
    pyautogui.keyDown('ctrl')
    pyautogui.sleep(interval)
    pyautogui.press(key)
    pyautogui.sleep(interval)
    pyautogui.keyUp('ctrl')
    pyautogui.sleep(interval)


def do(string):
    global text, math
    string = str(string)
    balloons.balloon_tip('Success', string)
    box = string.split('$')
    text = [box[i] for i in range(0, len(box), 2)]
    math = [box[i] for i in range(1, len(box), 2)]
    print(box)


def do_():
    global text
    for i in range(0, len(text)):
        if text[i] != '\n':
            if len(text[i]) >= 1:
                if text[i][0] == ' ':
                    text[i] = text[i][1:]
            pyperclip.copy(text[i])
            ctrl('v')
        else:
            pyautogui.press('enter')
        try:
            print(math[i])
            fp = open(path, 'w')
            fp.write(latex2mathml.converter.convert(math[i]))
            fp.close()

            pyautogui.keyDown('ctrl')
            pyautogui.press('n')
            pyautogui.press('m')
            pyautogui.keyUp('ctrl')
            pyautogui.sleep(.1)

            pyautogui.keyDown('alt')
            pyautogui.press('m')
            pyautogui.keyUp('alt')
            pyautogui.sleep(.1)

            pyperclip.copy(path.replace('/', '\\'))
            ctrl('v')
            pyautogui.press('enter')
            pyautogui.sleep(.1)

            # 처리
            ctrl('a')
            ctrl('c')
            pyautogui.sleep(.3)
            tt = pyperclip.paste().replace('RIGHT >', '>').replace('LEFT >', '>').replace('RIGHT <', '<').replace(
                'LEFT <', '<').replace(',', ',~').replace('∴', '~~THEREFORE~') + '`'
            pyperclip.copy(tt)

            pyautogui.sleep(.3)
            ctrl('v')

            pyautogui.keyDown('shift')
            pyautogui.press('esc')
            pyautogui.keyUp('shift')
            pyautogui.sleep(.1)

        except IndexError:
            pass
