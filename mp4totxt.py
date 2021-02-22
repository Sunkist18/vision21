import os
import sys
from random import randint

import cv2
import numpy as np

try:
    origin = sys.argv[1]
except IndexError:
    exit(112)

file_name = '\\'.join(origin.split('\\')[:-1]) + '\\' + str(randint(1, int(10e15)))
os.rename(origin, file_name)
capture = cv2.VideoCapture(file_name)
fps = capture.get(cv2.CAP_PROP_FPS)

pre_frame = None
frame_list = list()
frame_set = set()

start = False
tkatlq = False
mid = False
End = False

try:
    while True:
        if capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT):
            break

        ret, frame = capture.read()
        frame = frame[:, 0:960]
        if pre_frame is not None:
            diff_frame = cv2.absdiff(frame, pre_frame)
        else:
            diff_frame = frame
        sum_value = np.sum(diff_frame)
        if sum_value > 100000000:
            sec = int(capture.get(cv2.CAP_PROP_POS_FRAMES) // fps)
            if len(frame_list):
                if frame_list[-1] + 5 <= sec:
                    frame_list.append(sec)
            else:
                frame_list.append(sec)
        progress = int(capture.get(cv2.CAP_PROP_POS_FRAMES) / capture.get(cv2.CAP_PROP_FRAME_COUNT) * 100)
        if progress > 0 and not start:
            start = True
            print(origin, 'Started.')
        if progress > 30 and not tkatlq:
            tkatlq = True
            print(origin, 'Proceed 30%')
        if progress > 50 and not mid:
            mid = True
            print(origin, 'Proceed 50%')
        if progress > 90 and not End:
            End = True
            print(origin, 'Proceed 90%+')

        pre_frame = frame

finally:
    capture.release()
    cv2.destroyAllWindows()
    print(origin, 'Proceed Complete')
    for j in frame_list:
        hour = None
        minute = int(j // 60)
        if minute > 60:
            hour = minute // 60
            minute %= 60
        second = int(j % 60)
        if hour:
            frame_set.add('%02d:%02d:%02d' % (hour, minute, second))
        else:
            frame_set.add('%02d:%02d' % (minute, second))

    with open(origin.replace('.mp4', '.txt'), 'w') as f:
        f.write(' 0번 / '.join(sorted(list(frame_set))) + ' 0번')
        f.close()

    os.rename(file_name, origin)
