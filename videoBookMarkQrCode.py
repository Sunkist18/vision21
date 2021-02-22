import glob
import os
import pyperclip

import qrcode


def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def doQR(link, box_k, dir_path):
    # dir_path = dir_path.replace(' ', '')
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=0,
    )
    os.makedirs('./' + dir_path, exist_ok=True)
    for t, name in box_k:
        qr.clear()
        qr.add_data(link + '&t=' + str(t))
        qr.make_image().save('./' + dir_path + '/' + name + '.png')


while True:
    result = []
    title = input('TITLE\t# ').split('.')[0]
    try:
        pyperclip.copy(title[title.index('일비'):].replace('_', ' '))
    except:
        pass
    youtu = input('_LINK\t# ')
    try:
        path = './' + title[title.index('일비'):].replace(' ', '').replace('_', '')
    except:
        path = './' + title
    delta = int(input('DELTA\t# '))
    print('INPUT LINES HERE --- EOF\t# 0')
    index = 0
    while True:
        a = input()
        if a == "0":
            index  = 0
            break
        str_time = a.split('.')[0]
        index += 1
        chap = str(index)
        time = get_sec(str_time)
        if str_time[:3] == '00:':
            str_time = str_time[3:]
        result.append([chap, time, str_time])
    os.makedirs('./' + path, exist_ok=True)
    open(path + '/문제스킵.txt', 'w', encoding='utf8').write(' / '.join([str(i[2]) + ' 문제%02d' % (int(i[0]) + delta) for i in result]))
    doQR(youtu, [[i[1], '문제 ' + str(delta + int(i[0]))] for i in result], path) 
    # combine two txt
    try:
        result = []
        for txt in glob.glob(path + r'/*.txt'):
            for var in open(txt, 'r').readline().split(' / '):
                result.append(var.split())
        result.sort(key=lambda x: (len(x[0]), x[0]))
        open(title + '.txt', 'w', encoding='utf8').write(' / '.join([x[0] + ' ' + x[1] for x in result]))
    except:
        pass