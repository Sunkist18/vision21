from glob import glob

print('[*] 일비 스킵 합치기 프로그램')
print('[!] 폴더당 2개의 스킵파일이 있어야 합니다')
filename = input('filename [default : 전체스킵] : ')
condition = input('condition [default : 일비] : ')

for path in list(filter(lambda x: ('.' not in x) and (condition in x), glob('*'))):
    f = open(path + '/' + filename + '.txt', 'w')
    box = []
    for text in list(glob(path + '/' + '*.txt')):
        if filename in text:
            continue
        box += list(open(text, 'r').readline().split(' / '))
    box.sort(key=lambda x: (len(x.split()[0]), x))
    f.write(' / '.join(box))
    f.close()
