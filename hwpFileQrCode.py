import os
import time

import pyperclip as clip
import qrcode


def doQR(link, box_k, path):
    path = path.replace(' ', '')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=0,
    )
    os.makedirs('./' + path, exist_ok=True)
    for t, name in box_k:
        qr.clear()
        qr.add_data(link + '&t=' + str(t))
        qr.make_image().save('./' + path + '/' + name + '.png')


def reformatHwp(hwp):
    result = []
    start = False
    index = 0
    for line in str(hwp).split('\n'):
        line = line.replace('\r', '')
        if line == '스킵시간':
            start = True
            continue
        if not start or line == '':
            continue
        if index == 0:
            name = line
        if index == 1:
            time1 = line
        if index == 2:
            time2 = line
            result.append([int(time1) * 60 + int(time2), name])
            index = -1
        index += 1
    return result


recent_value = ""
title = ''
box = []
youtube_link = ''


def refactor(time_i):
    div, mod = divmod(time_i, 60)
    return ((refactor(div)) if div >= 60 else ('%02d' % div)) + (':%02d' % mod)


def doTXT(box_k, path):
    path = path.replace(' ', '')
    os.makedirs('./' + path, exist_ok=True)
    txt_list = []
    for t, name in box_k:
        txt_list.append(refactor(t) + ' ' + name)
    txt = ' / '.join(txt_list)
    f = open('./' + path + '/' + path + '.txt', 'w')
    f.write(txt)


clip.copy('')
while True:
    try:
        tmp_value = clip.paste()
        if tmp_value != recent_value:
            recent_value = tmp_value
            if "스킵타이틀" in recent_value:
                box = reformatHwp(recent_value)
            if "youtube" in recent_value:
                youtube_link = recent_value
            if '개념' in recent_value:
                title = recent_value
            if title and box and youtube_link:
                print(title + ' progress . . .')
                doQR(youtube_link, box, title)
                doTXT(box, title)
                print(title + ' Done')
                title = ''
                box = []
                youtube_link = ''
        time.sleep(0.1)
    except Exception as e:
        print(str(e), '\n')
