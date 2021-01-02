import pickle
from tkinter.filedialog import asksaveasfilename, askopenfilename


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
