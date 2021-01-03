import os

import qrcode


def isSkipVailed(string):
    return_value = []
    try:
        for part in string.split('/'):
            time, num = part.split()[0], ' '.join(part.split()[1:])
            if len(time.split(':')) == 2:
                time = int(time.split(':')[0]) * 60 + int(time.split(':')[1])
            if len(time.split(':')) == 3:
                time = int(time.split(':')[0]) * 60 * 60 + int(time.split(':')[1]) * 60 + int(time.split(':')[2])
            return_value.append([num, str(time)])
    except Exception as e:
        print('인식할 수 없는 스킵 문자열이 있습니다')
        print(e)
        print(string)
    return return_value


if __name__ == '__main__':
    print('1. 유튜브 링크를 복사해서 붙여 넣으세요 (공유하기)')
    print('2. 메인 제목을 붙여 넣으세요')
    print('3. 스킵 문자열을 붙여넣으세요')
    while True:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=0,
        )
        qr.clear()
        print()
        youtube_link = input('Youtube Link\t: ')
        path = input('Youtube Title\t: ')
        skip_str = input('Youtube Skip\t: ')
        skip_str = isSkipVailed(skip_str)
        if not skip_str:
            continue
        try:
            os.mkdir(path)
        except:
            pass
        for title, t in skip_str:
            qr.clear()
            qr.add_data(youtube_link + '?t=' + t)
            qr.make_image().save(path + '/' + title + '.png')
        print('[QRCODE] Work complete with', len(skip_str), 'files.')
