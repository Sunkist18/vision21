import os
from glob import glob
from multiprocessing import Pool


def sync(filedir):
    try:
        os.system('python mp4totxt.py "' + filedir + '"')
    except:
        print('something is wrong')


if __name__ == '__main__':
    direct = input('direct : ')
    print(str(len(glob(direct + '\\' + '*.mp4'))) + ' videos founded.')
    input('Press Any key to continue')

    pool = Pool(processes=5)
    pool.map(sync, glob(direct + '\\' + '*.mp4'))
    pool.close()
    pool.join()
