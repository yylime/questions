import random
import pdfplumber
import re
from collections import defaultdict


def load_pdf(path):
    outputs = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            outputs = outputs + page.extract_text()

    with open('output.txt', 'w+') as f:
        f.write(outputs)

# 模拟提取所有的题目
def txt2list(path):
    res = []
    with open(path, 'r') as f:
        datas = f.readlines()
    # 检测数字和点在里面
    pattern_subject = re.compile("\d+\.")
    pattern_select = re.compile("[A-F]\.")
    # 定义一个连接每一行的标志，是否属于标题or解析or选项
    f = None
    for line in datas:
        if pattern_subject.findall(line):
            res.append(defaultdict(str))
            # 提出后面的选项
            if pattern_select.findall(line):
                pre = pre = pattern_select.findall(line)[0]
                res[-1]['subject'] += line.split(pre)[0].strip('\n').strip(' ')
            else:
                res[-1]['subject'] += line.strip('\n').strip(' ')
            f = 'subject'
        # 有的题目选项A在同一行，稍作处理，有的C和D在同一行我们也要处理
        if pattern_select.findall(line):
            pre = pattern_select.findall(line)
            for i, ps in enumerate(pre):
                key = ps.split('.')[0]
                if i ==0 and len(line.strip('\n').strip(' ').split(ps)[0]) > 0:
                    res[-1]['subject'] += line.strip('\n').strip(' ').split(ps)[0]
                res[-1][key] = ps + line.split(ps)[-1].split('.')[0].rstrip('D.').strip('\n').strip(' ')
                f = ps
        elif "答案" in line:
            # res[-1]['answer'] = line.split('】')[0].split('【')[0].strip('\n').strip(' ').replace("|", "")
            words = re.findall("[A-Z]+", line)
            answer = "".join(words)
            res[-1]['answer'] = answer
            f = "answer" if "解析" not in line else 'explain'
        elif "解析" in line:
            res[-1]['explain'] = line.strip('\n').strip(' ')
            f = 'explain'
        elif not pattern_subject.findall(line):
            # 如果答案和解析超过了一行需要额外处理
            if f == 'subject' and (res[-1][f][-1] != '。' or res[-1][f][-1] != '）'):
                res[-1][f] += line.strip('\n').strip(' ')
            elif f == 'explain' and (len(res[-1][f]) == 0 or res[-1][f][-1] != '。'):
                res[-1][f] += line.strip('\n').strip(' ')
            elif f == 'answer' and (len(res[-1][f]) == 0 or res[-1][f][-1] != '。'):
                res[-1][f] += line.strip('\n').strip(' ')
            else:
                f = None
    return res

def shuati(subjects):
    select_subjects = []
    for sub in subjects:
        if 'A' in sub:
            select_subjects.append(sub)
    # 随机做题
    n = len(select_subjects)
    while True:
        idx = random.randint(0, n - 1)
        sub = select_subjects[idx]
        print(sub['subject'])

        if len(sub['answer']) > 1:
            print("多选题")

        for c in "ABCDEF":
            if c in sub:
                print(sub[c])
        ans = input("输入正确答案: ")

        if str.upper(ans) == str.upper(sub['answer']):
            print("Right")
        else:
            print("Wrong")
            print(sub['answer'])
        if 'explain' in sub:
            print(sub['explain'])
        end = input("Input any key to continue: ")
        if str.lower(end) == 'exit':
            break

if __name__ == "__main__":
    tiku = txt2list("output.txt")
    # print(tiku[150])
    shuati(tiku)
