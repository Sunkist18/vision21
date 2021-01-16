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
        print(file_name, '\t\t', int(capture.get(cv2.CAP_PROP_POS_FRAMES)), '/',
              int(capture.get(cv2.CAP_PROP_FRAME_COUNT)))
        pre_frame = frame

finally:
    capture.release()
    cv2.destroyAllWindows()

    for j in frame_list:
        minute = int(j // 60)
        second = int(j % 60)
        frame_set.add('%02d:%02d' % (minute, second))

    with open(origin.replace('.mp4', '.txt'), 'w') as f:
        f.write(' 0번 / '.join(sorted(list(frame_set))) + ' 0번')
        f.close()

    os.rename(file_name, origin)
