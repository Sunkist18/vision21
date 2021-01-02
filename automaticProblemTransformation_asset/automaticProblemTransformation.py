import pickle
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename, askopenfilename

import clipboard


def saveAs(file):
    title = '문제집 저장'
    file_type = [('문제집 파일', '.min')]
    filename = asksaveasfilename(filetypes=file_type, title=title,
                                 initialfile='문제집.min')
    if not filename:
        return None
    with open(filename, 'wb') as f:
        pickle.dump(file, f)


def loadMin():
    asked_roots = askopenfilename(title='문제 열기', filetypes=(('문제집', '*.min'), ('모든 타입의 문제', '*.*')))

    if not asked_roots:
        return None
    with open(asked_roots, 'rb') as f:
        return pickle.load(f)


# var 에 변수들 넣기
from decimal import Decimal
from fractions import Fraction

var = {}
n_count = 0
exec_value = None
frac_nums = []
url = 'sample.txt'


def frac_true():
    for frac_num in frac_nums:
        print(frac_num)
        if len(frac_num) > 25:
            return False
    return True


def frac(num):
    frac_num = str(Fraction(format(Decimal.from_float(num), '.3')))
    pre_frac_num = frac_num
    for i in range(4, 17):
        frac_num = str(Fraction(format(Decimal.from_float(num), '.' + str(i))))
        pre_frac_num = pre_frac_num if len(pre_frac_num) < len(frac_num) else frac_num
    if '/' in frac_num:
        frac_nums.append('{' + frac_num.split('/')[0] + '} over {' + frac_num.split('/')[1] + '}')
        return '{' + frac_num.split('/')[0] + '} over {' + frac_num.split('/')[1] + '}'
    return frac_num


def txt_to_var(whole_text):
    """
    :param whole_text: \n을 포함한 문자열입니다
    :return: 문자열을 # 제외 + 모든 변수지정자에 변수들을 집어 넣습니다
    """
    global n_count
    line_result = ''
    for line in whole_text.split('\n'):
        if '#' in line or not line or line == '\n':
            continue
        for var_name in var:
            line = line.replace('&' + str(var_name), str(var[var_name]))
        n_count += line.count('</n>')
        line_result += line + '\n'
    return line_result


def per_to_txt(whole_text):
    line_result = ''
    for line in whole_text.split('\n'):
        if '#' in line or not line or line == '\n':
            continue
        while line.count('%'):
            eval_line = line.split('%')[-1].split(' ')[0]
            exec('global exec_value; exec_value = ' + eval_line)
            line = line.replace('%' + eval_line, str(exec_value))
        line_result += line + '\n'
    return line_result


def check_condition(condition_line):
    for line in condition_line.split('\n'):
        if '#' in line or not line or line == '\n':
            continue
        exec('global exec_value; exec_value = ' + line)
        if not exec_value:
            return False
    return True


def task():
    with open(url, 'r', encoding='UTF8') as fp:
        readfile = fp.read()

        # 파싱
        func = readfile.split('@function')[-1].split('@text')[0]
        text = readfile.split('@text')[-1].split('@answer')[0]
        answ = readfile.split('@answer')[-1].split('@condition')[0]
        cond = readfile.split('@condition')[-1].split('@global')[0]
        glob = readfile.split('@global')[-1]

        # 전처리 과정
        # 변수 넣기 / 필요한 함수 제작 / 모듈 불러오기
        exec('global var;' + func)

        # 파싱한 데이터 (text, answ) 에서 # 제거 및 변수 넣기
        text = txt_to_var(text)
        answ = txt_to_var(answ)
        cond = txt_to_var(cond)
        glob = txt_to_var(glob)

        text = per_to_txt(text)
        answ = per_to_txt(answ)
        cond = per_to_txt(cond)
        glob = per_to_txt(glob)

        result = text.replace('\n', ':ENTER:') + '<p>\n' + answ.replace('\n', ':ENTER:') + '<a>\n'

        fp.close()
        return [check_condition(cond), result]


def url_to_str(txt_url):
    global url
    url = txt_url
    while True:
        frac_nums = []
        condition_work, return_value = task()
        if condition_work:
            break
    return return_value


window = Tk()
window.title('APG - dandalf@o.cnu.ac.kr')
window.geometry('480x480+200+200')
window.resizable(True, True)

window.dir_roots = list()


def addRoot():
    asked_roots = filedialog.askopenfilenames(title='문제 열기', filetypes=(('텍스트 문제', '*.txt'), ('모든 타입의 문제', '*.*')))
    if not len(asked_roots):
        return
    for asked_root in asked_roots:
        dirStructure = {'dirRoot': asked_root,
                        'viewRoot': str(asked_root).split('/')[-1].replace('{', '').replace('}', '')}
        window.dir_roots.append(dirStructure)
        folder_list.insert(END, window.dir_roots[-1]['viewRoot'])


def delRoot(lists):
    cur = lists.curselection()
    lists.delete(cur[0])
    del window.dir_roots[cur[0]]


def shiftUp(lists):
    cur = lists.curselection()
    if not cur:
        return
    root = window.dir_roots[cur[0]]
    lists.delete(cur[0])
    lists.insert(cur[0] - 1, root['viewRoot'])
    window.dir_roots.pop(cur[0])
    window.dir_roots.insert(cur[0] - 1, root)
    lists.selection_set(cur[0] - 1)


def shiftDown(lists):
    cur = lists.curselection()
    if not cur:
        return
    root = window.dir_roots[cur[0]]
    lists.delete(cur[0])
    lists.insert(cur[0] + 1, root['viewRoot'])
    window.dir_roots.pop(cur[0])
    window.dir_roots.insert(cur[0] + 1, root)
    lists.selection_set(cur[0] + 1)


def loadPick(list_box):
    loadedData = loadMin()
    if not loadedData:
        return
    window.dir_roots = loadedData
    refresh(list_box)
    return


def refresh(list_box):
    list_box.delete(0, END)
    for dir_root in window.dir_roots:
        list_box.insert(END, dir_root['viewRoot'])


var_frame = Frame(window, padx=10, pady=10)
left_frame = LabelFrame(var_frame, text='| Shift + UP/DOWN | Delete |', padx=10, pady=10)
right_frame = Frame(window, padx=20, pady=20)
right_up_frame = Frame(right_frame, padx=5, pady=5)
right_add_frame = Frame(right_frame, padx=5, pady=0)
right_pre = Frame(right_add_frame)
right_down_frame = Frame(right_frame, padx=5, pady=10)

var_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)
left_frame.pack(side=LEFT, fill=BOTH, expand=TRUE)
right_frame.pack(side=RIGHT, fill=BOTH, expand=TRUE)
right_up_frame.pack(side=TOP, fill=BOTH, expand=FALSE)
right_add_frame.pack(side=TOP, fill=BOTH, expand=FALSE)
right_down_frame.pack(side=BOTTOM, fill=BOTH, expand=TRUE)
right_pre.pack(side=BOTTOM, expand=TRUE)

folder_list_scroll = Scrollbar(left_frame)
folder_list_scroll.pack(side=RIGHT, fill=Y)

folder_list = Listbox(left_frame, yscrollcommand=folder_list_scroll.set)
folder_list.bind('<Delete>', lambda event: delRoot(folder_list))
folder_list.bind('<Shift-Up>', lambda event: shiftUp(folder_list))
folder_list.bind('<Shift-Down>', lambda event: shiftDown(folder_list))
folder_list.pack(side=RIGHT, fill=BOTH, expand=TRUE)

add_button = Button(right_add_frame, text='Add Component', command=addRoot)
add_button.pack(side=RIGHT, fill=BOTH, expand=TRUE)

save_button = Button(right_up_frame, text='Save', command=lambda: saveAs(window.dir_roots))
save_button.pack(side=LEFT, fill=X, expand=TRUE)
load_button = Button(right_up_frame, text='Load', command=lambda: loadPick(folder_list))
load_button.pack(side=LEFT, fill=X, expand=TRUE)


# img = ImageTk.PhotoImage(ImageTk.Image.open('..\\image\\2번.png'))
# preview = Label(right_pre, image=img)
# preview.pack(side=BOTTOM, fill="y", expand=YES)


def doHandler():
    result = ''
    for root_url in window.dir_roots:
        result += url_to_str(root_url['dirRoot'])

    print('미주변경', result.count('<a>'))
    print('수식변경', result.count('</n>'))
    print('자동줄바꿈', 1)

    clipboard.copy(result)


start_button = Button(right_down_frame, text='Run', command=lambda: doHandler())
start_button.pack(side=BOTTOM, fill=X, expand=FALSE)

window.mainloop()
