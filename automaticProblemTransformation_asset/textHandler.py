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
