import latex2mathml.converter
import pyperclip

path = 'C:/Users/user/Desktop/latex_cmw.mml'
if __name__ == '__main__':
    pyperclip.copy('')
    prev_clipboard = ''
    next_clipboard = ''
    while True:
        # try:
        next_clipboard = pyperclip.paste()
        if next_clipboard != prev_clipboard:
            latex = next_clipboard
            if '$' in latex:
                with open(path, 'w') as fp:
                    print(latex2mathml.converter.convert(latex.replace('$', '')))
                    fp.write(latex2mathml.converter.convert(latex.replace('$', '')))

        prev_clipboard = next_clipboard
        # except Exception as e:
        #     next_clipboard = ''
        #     print('next_clipboard : ' + next_clipboard)
        #     print('prev_clipboard : ' + prev_clipboard)
        #     print('Exception : ' + str(e))
