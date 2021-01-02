from tkinter import *
from tkinter import filedialog

import clipboard

import automaticProblemTransformation_asset.saveLoader as saveLoader
import automaticProblemTransformation_asset.textHandler as textHandler

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
    loadedData = saveLoader.loadMin()
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

save_button = Button(right_up_frame, text='Save', command=lambda: saveLoader.saveAs(window.dir_roots))
save_button.pack(side=LEFT, fill=X, expand=TRUE)
load_button = Button(right_up_frame, text='Load', command=lambda: loadPick(folder_list))
load_button.pack(side=LEFT, fill=X, expand=TRUE)

# img = ImageTk.PhotoImage(ImageTk.Image.open('..\\image\\2번.png'))
# preview = Label(right_pre, image=img)
# preview.pack(side=BOTTOM, fill="y", expand=YES)


def doHandler():
    result = ''
    for root_url in window.dir_roots:
        result += textHandler.url_to_str(root_url['dirRoot'])

    print('미주변경', result.count('<a>'))
    print('수식변경', result.count('</n>'))
    print('자동줄바꿈', 1)

    clipboard.copy(result)


start_button = Button(right_down_frame, text='Run', command=lambda: doHandler())
start_button.pack(side=BOTTOM, fill=X, expand=FALSE)

window.mainloop()
