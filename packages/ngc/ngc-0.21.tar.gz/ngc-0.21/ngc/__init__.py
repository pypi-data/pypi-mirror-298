import os
import sys
import shutil
import re
import json
import csv
import urllib
import html
import requests
import threading
import glob
import tempfile
import pathlib

# **************************
# 文件管理相关
# **************************

traverse_dir_all = lambda path : pathlib.Path(path).rglob('*')
traverse_dir = lambda path : list(filter(lambda x: os.path.isfile(x), pathlib.Path(path).rglob('*')))
traverse_dir_quick = lambda path : glob.iglob(path+'/**',recursive=True)
'''Usage: /path_root/**/*.txt'''

def dirlist(path, ext="", containDir=False, depth=1,pureFilename=False):
    '''
    traverse folder
    '''
    if type(path) is list:
        return path
    allfiles=[]
    rsl=os.walk(path, topdown=True)
    for root, dirs, files in rsl:
        if depth<0 or root.replace(path,"").count("\\")<depth:
            for name in files:
                if name.endswith(ext):
                    if pureFilename:
                        allfiles.append(name)
                    else:
                        allfiles.append(os.path.join(root, name).replace("\\","/"))
            if containDir:
                for name in dirs:
                    if pureFilename:
                        allfiles.append(name)
                    else:
                        allfiles.append(os.path.join(root, name).replace("\\","/"))
    return allfiles

# makedir = os.makedirs
makedir = lambda path: os.makedirs(path) if not os.path.exists(path) else None
'''os make directory'''
getdir=lambda src:os.path.split(src)[0]
'''get dirname of file'''
getname = lambda src,incsuff=True:os.path.split(src)[1] if incsuff else os.path.splitext(os.path.split(src)[1])[0]
'''get filename'''
copyfile = lambda srcfile, dstfile,force=False:shutil.copyfile(srcfile,dstfile) if not os.path.exists(dstfile) or force else None
'''copy file'''
copydir = lambda srcdir,dstdir,force=False:list(makedir(y) if os.path.isdir(x) else copyfile(x,y,force) for [x,y] in dirstruct_copy(srcdir,dstdir))
'''copy directory'''
copy = lambda src,dst,force=False:copyfile(src,dst,force) if os.path.isfile(src) else copydir(src,dst,force)
'''copy file or directory'''
dirstruct_copy=lambda srcdir,dstdir: list([x,x.replace(srcdir,dstdir)] for x in dirlist(srcdir,containDir=1,depth=-1))
'''return the same path list replaced'''

fork_dir = lambda src,dst,*arg: shutil.copytree(src,dst,arg) if not os.path.exists(dst) else None
'''copy dir = copydir / new func'''
fork_file = shutil.copy
'''copy file = copyfile / new func'''

rename = os.rename
'''rename'''
PathAdd = lambda src,ex = "_new":os.path.join(os.path.split(src)[0] + ex, os.path.split(src)[1])

PathAdd = lambda src,ex = "_new", built = 1: (makedir(os.path.split(src)[0] + ex) if built else None) or os.path.join(os.path.split(src)[0] + ex, os.path.split(src)[1])
'''replace to directory-relative pathname'''
NameAdd = lambda src,ex = "_new":os.path.splitext(src)[0]+ex+os.path.splitext(src)[1]
'''replace to filename-relative pathname'''

def another(file_path):
    '''avoid same file for PathAdd, NameAdd'''
    import random
    dir_name = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    name, ext = os.path.splitext(file_name)
    if not ext: ext = '.dat'
    new_file_name = name + '_new' + ext
    new_file_path = os.path.join(dir_name, new_file_name)
    while os.path.exists(new_file_path):
        new_file_name = name + '_new' + str(random.randint(1,100)) + ext
        new_file_path = os.path.join(dir_name, new_file_name)
    return new_file_path


def calculate_deepest_folder(file_paths):
    """
    Calculate the deepest folder directory in which a group of file paths are located.
    计算一组文件路径共同所在的最深文件夹目录
    :param file_paths: 一个文件路径列表
    :return: 共同最深文件夹目录
    """
    # 检查输入参数
    if not isinstance(file_paths, list):
        raise TypeError('file_paths should be a list')
    if len(file_paths) == 0:
        raise ValueError('file_paths can not be empty')

    # 获取最深文件夹
    deepest_folder = os.path.dirname(file_paths[0])
    for path in file_paths[1:]:
        deepest_folder = os.path.commonpath([deepest_folder, path])
    return deepest_folder



# **************************
# 文件读写相关
# **************************

## file
filename_format = lambda x: re.sub('[\\\\/:\*\?"<>\|]','_',x)
'''format filename'''
readfile = lambda src,srccoding="utf-8" : open(src,"rb").read().decode(srccoding)
'''read text file content'''
writefile = lambda cnt,dst,dstcoding="utf-8" : open(dst,"wb").write(cnt.encode(dstcoding))
'''write text file content'''
readalllines = lambda src,srccoding="utf-8": open(src,'r',encoding=srccoding).read().splitlines()
'''read text file content to lines'''
writealllines = lambda lines,src,srccoding="utf-8": open(src,'w',encoding=srccoding).writelines([x+'\n' for x in lines])
'''write text lines to file'''
jsonload = lambda src,srccoding="utf-8" : json.load(open(src, "r", encoding=srccoding))
'''load json from file'''
jsondump = lambda dic,dst,srccoding='utf-8',sort=False : json.dump(dic, open(dst, "w", encoding=srccoding), ensure_ascii=False, sort_keys=sort, indent=4)
'''dump json to file'''
csvload = lambda src,srccoding='utf-8',dem=',',skipHead=False : list(csv.reader(open(src, "r", encoding=srccoding),delimiter=dem))[1 if skipHead else 0:]
'''load double list from csv file'''
csvdump = lambda dic,dst,srccoding='utf-8-sig',dem=',' : csv.writer(open(dst, 'w', encoding=srccoding),delimiter=dem,lineterminator='\n').writerows(dic)
'''dump double list to csv file'''
loadFileHex = lambda src:list(open(src,'rb').read())
'''load hex list from binary file'''
dumpFileHex = lambda iter,dst:open(dst,'wb').write(bytes(iter))
'''dump hex list to binary file'''


class temp():
    def __init__(self):
        self.f = tempfile.TemporaryFile(mode='w+t',encoding='u8')
    
    def write(self, text, mode='w'):
        """
        写入内容到临时文件中
        text: 要写入的内容，可以是字符串或字符串列表
        mode: 写入模式，可以是 'w'（覆写）、'a'（追加）或 'w+'（清空后重写）
        """
        if mode == 'a':
            self.f.seek(0, 2)  # 将文件指针移动到文件末尾
        elif mode == 'w+':
            self.f.seek(0)  # 将文件指针移动到文件开头
            self.f.truncate(0)  # 截断文件，清空文件中的内容
        elif mode == 'o':
            self.f.seek(0)  # 将文件指针移动到文件开头
        
        if isinstance(text, str):
            self.f.write(text)
        elif isinstance(text, list):
            self.f.writelines([line+'\n' for line in text])
        
        self.f.flush()  # 刷新文件缓冲区，确保内容被写入到临时文件中
        
    def read(self, n=-1):
        """
        读取临时文件中的内容
        n: 读取的字节数，默认为 -1，表示读取全部内容
        """
        pos = self.f.tell()  # 保存当前文件指针位置
        self.f.seek(0)  # 将文件指针移动到文件开头
        try:
            return self.f.read(n)
        finally:
            self.f.seek(pos)  # 恢复文件指针位置
    
    def readline(self):
        """
        从临时文件中读取一行内容
        """
        return self.f.readline()
    
    def readlines(self):
        """
        读取临时文件中的所有行，并返回一个包含所有行的列表
        """
        pos = self.f.tell()  # 保存当前文件指针位置
        self.f.seek(0)  # 将文件指针移动到文件开头
        try:
            return self.f.read().splitlines()
        finally:
            self.f.seek(pos)  # 恢复文件指针位置
            
    def __del__(self):
        self.f.close()

    def copy_to_file(self, filename):
        """
        将临时文件内容拷贝到目标文件中
        filename: 目标文件名
        """
        import shutil
        self.f.seek(0)  # 将文件指针移动到文件开头
        with open(filename, 'w', encoding='utf-8') as f:
            shutil.copyfileobj(self.f, f)

    def changemode(self, mode='w'):
        if mode == 'a':
            self.f.seek(0, 2)  # 将文件指针移动到文件末尾
        elif mode == 'w+':
            self.f.seek(0)  # 将文件指针移动到文件开头
            self.f.truncate(0)  # 截断文件，清空文件中的内容
        elif mode == 'o':
            self.f.seek(0)  # 将文件指针移动到文件开头



# **************************
# 运算相关
# **************************

## calculate
between = lambda x,a,b: x>=a and x<=b
'''whether a <= x <= b'''

def splits(mstr,marks):
    if type(mstr)==list:
        mgs = mstr
    else:
        mgs = [mstr]
    if type(marks)==str:
        marks=[marks]
    for mark in marks:
        ngs = []
        for x in mgs:
            ngs+=x.split(mark)
        mgs = ngs
    mgs = [x for x in mgs if x!='']
    return mgs


def matches(mstr,marks):
    if type(mstr)==list:
        mgs = mstr
    else:
        mgs = [mstr]
    if type(marks)==str:
        marks=[marks]
    for mark in marks:
        for mg in mgs:
            if re.match(mark,mg):
                return True
    return False


# **************************
# 字符串操作相关
# **************************

## string solve
# replaceAll = lambda x, replis: list(x:=x.replace(y[0],y[1]) for y in replis) and x
def replaceAll(x, replis):
    """
    批量替换字符串中的内容
    x: 待替换的字符串
    replis: 替换规则，为一个列表，列表中每个元素为一个元组，元组中包含两个字符串，
            第一个字符串表示待替换的内容，第二个字符串表示替换后的内容
    """
    for r in replis:
        x = x.replace(r[0], r[1])
    return x


'''replace item from double list'''
afterDecodeCP932 = lambda x, replis=[['〜','～'],['‖','∥'],['−','－']]: replaceAll(x,replis)
'''fix CP932 content read with python'''
beforeEncodeCP932 = lambda x, replis=[['·','・'],['～','〜'],['∥','‖'],['－','−']]: replaceAll(x,replis)
''''''
is_En = lambda char : char >= '\u0000' and char <= '\u007F'
'''is a char ascii'''
is_enline = lambda line : not sum(not is_En(ch) for ch in line)
'''is a string ascii'''
strQ2B = lambda ustring : ''.join(list((chr(ord(u)-0xFEE0) if between(ord(u),0x21+0xFEE0,0x7E+0xFEE0) else u) if u!='　' else ' ' for u in ustring))
'''convert full width to half width'''
strB2Q = lambda ustring : ''.join(list((chr(ord(u)+0xFEE0) if between(ord(u),0x21,0x7E) else u) if u!=' ' else '　' for u in ustring))
'''convert half width to full width'''



# **************************
# 数据结构相关
# **************************

## struct

prlis = lambda lis: list(print(x) for x in lis)
'''print item from list'''

mergeDict = lambda d1, d2:d1.copy().update(d2)
'''merge dict'''

cvtLis2Dic = lambda lis : dict(x for x in lis)
'''merge dict'''

cvtLis2Dic = lambda lis1,lis2 : dict([[x[0],x[1]] for x in list(zip(lis1,lis2))])
'''convert list to dict'''

zip2map=cvtLis2Dic

revertDic = lambda dic: dict([[v,k] for k, v in dic.items()])
'''revert dict item'''

flipLis = lambda lis: list(x.reverse() for x in lis)
'''revert double list'''

sortList = lambda lis,i=1,rev=False : sorted(lis, key=(lambda x: x[i]),reverse=rev) if type(lis) is list else lis
'''sort list with item'''

sortLisDict = lambda dic,rev=False : sorted(dic.items(), key=lambda d: d[1], reverse=rev) if type(dic) is dict else dic
'''sort dict with value'''

cvtCsv2Dic = lambda lines : dict(list([line[0],dict(list([lines[0][i+1],v] for i,v in enumerate(line[1:])))] for line in lines[1:]))
'''convert csv's double list to dict'''


def json_format(json_data,maxlen=10):
    """
    输入一个json，以一行maxlen个元素的形式的json输出
    :param json_data: json的数据
    :return: json的字符串
    """
    if isinstance(json_data, list):
        json_str = "["
        for i in range(len(json_data)):
            if i % maxlen == 0 and i != 0:
                json_str += "\n"
            json_str += '"{}"'.format(str(json_data[i]).replace('"','\\"')) + ","
        json_str = json_str[:-1] + "]"
    elif isinstance(json_data, dict):
        json_str = "{"
        for key, value in json_data.items():
            if json_str.count(",") % maxlen == 0 and json_str.count(",") != 0:
                json_str += "\n"
            json_str += '"' + str(key).replace('"','\\"') + '":"' + str(value).replace('"','\\"') + '",'
        json_str = json_str[:-1] + "}"
    else:
        raise TypeError("json格式错误")
    return json_str



def print_leaf_elements(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print_leaf_elements(value)
            else:
                print(key, ':', value)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                print_leaf_elements(item)
            else:
                print(item)

def match_leaf_elements(data,regex,result_list=[]):
    if isinstance(data, dict):
        for key, value in data.items():
            result_list = match_leaf_elements(value,regex,result_list)
            result_list = match_leaf_elements(key,regex,result_list)
    elif isinstance(data, list):
        for item in data:
            result_list = match_leaf_elements(item,regex,result_list)
    elif isinstance(data, str) and (rgx := re.match(regex,data)):
        result_list += [''.join(rgx.groups())]
    return result_list



def simplify_list(lst, skip_element_func = None):
    # 给出py，输入int元素的list，
    # 把每一段连续整数的简化成[start, end]，单个亦然，
    # skip_element_func作用是，在list中出现连续的整数，但是中间有一个元素被跳过的情况下，
    # 根据skip_element_func的判断结果来决定是否把被跳过的元素也算进去，
    # 从而简化list中的连续整数。
    # 输出[start, end]的list
    # 应用：查找并给出GBK编码范围
    lst = sorted(lst)
    result = []
    start = lst[0]
    end = lst[0]
    for i in range(1, len(lst)):
        if lst[i] - lst[i-1] == 1:
            end = lst[i]
        elif skip_element_func and lst[i] - lst[i-1] == 2 and skip_element_func(lst[i-1]+1):
            end = lst[i]
        else:
            result.append([start, end])
            start = lst[i]
            end = lst[i]
    result.append([start, end])
    return result


def int_to_hex(data):
    '''该函数的作用是将输入的json中int数据转换为十六进制'''
    if isinstance(data, dict):
        return {int_to_hex(key): int_to_hex(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [int_to_hex(elem) for elem in data]
    elif isinstance(data, int):
        return hex(data)
    else:
        return data



# **************************
# 文本操作相关
# **************************

def dectect_coding(src):
    import chardet
    f = open(src, "rb")
    coding = chardet.detect(f.read())["encoding"]
    f.close()
    return coding


def read_file_by_line_max_N(file_name, N, func):
    # 给我markdown格式的python3函数，
    # 输入文本文件，
    # 从首行开始读取，一次读取多行，
    # 确保一次读取的文本行拼接后的字符数量最多，但不超过N，
    # 且读取的每一行都要完整，然后作为参数调用func，
    # 直至读取到文件结束。
    with open(file_name, 'r', encoding='u8') as f:
        line = f.readline()
        lines = []
        total_len = 0
        while line:
            line_len = len(line)
            if total_len + line_len > N:
                func(''.join(lines))
                # func('-'*20)
                lines = []
                total_len = 0
            total_len += line_len
            lines.append(line)
            line = f.readline()
        if lines:
            func(''.join(lines))
            # func('-'*20)

def split_StrList_by_line_maxlen(lis, maxlen=3000):
    # 将一个字符串列表按照每行的最大长度进行分割，
    # 将分割出来的字符串列表存入新的列表中，
    # 并返回新的列表
    dstlis = [[]]
    for line in lis:
        if sum(list(len(x) for x in dstlis[-1])) + len(line) < maxlen:
            dstlis[-1].append(line)
        else:
            dstlis.append([line])
    return dstlis

# getline
def get_list_elements(lis,noret = None):
    '''
    yield line from lis
    '''
    for line in lis:
        yield line
    while True:
        yield noret

def insert_blank_lines(lisa, lisb):
    # 给我markdown格式的python3函数，
    # 输入字符串列表lisa和lisb，lisa中有空行，lisb没有空行，
    # 请在lisb中的lisa所有有空行的位置插入空行，输出lisb
    blank_indexes = []
    for index, line in enumerate(lisa):
        if line == '':
            blank_indexes.append(index)
    for blank_index in blank_indexes:
        lisb.insert(blank_index, '')
    return lisb


def extract_list(strSourceLis, regexList, regexExcepLis):
    # 给我markdown格式的py3代码，设计函数，
    # 检查strSourceLis的所有元素，
    # 其中与regexList中的正则表达式匹配的行
    # （最多只匹配一个正则表达式，且该行不能匹配到rgexExcepLis的所有表达式），
    # 提取这些行的捕获项拼接后的字符串（如无捕获则使用整行）返回列表
    # 或叫 regex_transform check_str_list
    result = []
    for line in strSourceLis:
        for regex in regexList:
            m = re.match(regex,line)
            if m:
                excepFlag = False
                for excep in regexExcepLis:
                    if re.search(excep,line):
                        excepFlag = True
                        break
                if not excepFlag:
                    result.append(''.join(m.groups()) if m.groups() else line)
                    break
    return result


def inpack_list(strSourceLis, regexList, strReplaceLis, regexExcepLis):
    '''给我markdown格式的py3代码，设计函数，
    检查strSourceLis的所有元素，
    其中与regexList中的正则表达式匹配的行
    （最多只匹配一个正则表达式，且该行不能匹配到rgexExcepLis的所有表达式），
    用strReplaceLis的字符串替换捕获项并更新到strSourceLis，
    返回更新后的strSourceLis
    或叫replace_str_by_regex regex_replace'''
    l=0
    for i in range(len(strSourceLis)):
        for j in range(len(regexList)):
            match = re.match(regexList[j], strSourceLis[i])
            if match:
                flag = 0
                for k in range(len(regexExcepLis)):
                    if re.match(regexExcepLis[k], strSourceLis[i]):
                        flag = 1
                        break
                if flag == 0:
                    gp = re.match(regexList[j], strSourceLis[i])
                    strSourceLis[i] = gp.group(1) + strReplaceLis[l] + gp.group(3)
                    # strSourceLis[i] = re.sub(regexList[j], strReplaceLis[l], strSourceLis[i])
                    l+=1
                    break
    return strSourceLis


#推荐单段式 ^.*'(.*)'.*
def extractTextsLines(src,pattern,srccode="utf-8",repl=None,isLine=True,exc=None):
    newlines=[]
    if isLine:
        if repl==None:
            repl=""
            for i in range(pattern.count('(')):repl+="\\"+str(i+1)
            repl=eval("r'"+repl+"'")
        for line in open(src,encoding=srccode).read().splitlines():
            if exc:
                gpt=re.match(exc,line)
            gps=re.match(pattern,line)
            if gps and (not exc or exc and not gpt):
                newlines.append(re.sub(pattern,repl,line))
    else:
        patternx = pattern
        newlines=re.findall(patternx,open(src,"r",encoding=srccode).read())
    return newlines

#推荐三段式 ^(.*')(.*)('.*)
def inpackTexts(src,dst,pattern,replLines,threeform=True,isLine=True,srccode="utf-8",dstcode="utf-8",exc=None):
    """ 根据正则表达式列表文本回填
    :param src: 源文件路径
    :param dst: 目标文件路径
    :param pattern: 正则表达式
    :param replLines: 替换文本列表
    :param threeform: 是否采用三元组形式
    :param isLine: 是否按行替换
    :param srccode: 源文件编码
    :param dstcode: 目标文件编码
    :param exc: 排除正则表达式
    :return: None """
    lines=open(src,encoding=srccode).read().splitlines()
    replline=get_list_elements(replLines)
    if isLine:
        for i in range(len(lines)):
            gps=re.match(pattern,lines[i])
            if exc:
                gpt=re.match(exc,lines[i])
            if gps and (not exc or exc and not gpt):
                if threeform:
                    lines[i]=gps.group(1)+next(replline)+gps.group(3)
                else:
                    lines[i]=re.sub(pattern,next(replline),lines[i])
    open(dst,'w',encoding=dstcode).writelines([lines[i] + '\n' if i<len(lines)-1 else lines[i] for i in range(len(lines))])






# **************************
# Web相关
# **************************

## web solve
url_encode = urllib.parse.quote
'''urllib.parse.quote'''
url_decode = urllib.parse.unquote
'''html.escape'''
html_encode = html.escape
'''html.escape'''
html_decode = html.unescape
'''html.unescape'''
downloadDic = lambda url,data={}: json.loads(requests.post(url,data).text)
'''get dict from url posted'''
download = lambda url,dst : open(dst, "wb").write(requests.get(url).content)
'''download file from url got'''



# 创建一个空的代理字典
no_proxies = {
    "http": None,
    "https": None,
}

# 保存原始的 requests.get 方法
original_get = requests.get

def new_get(url, **kwargs):
    if 'proxies' not in kwargs:
        kwargs['proxies'] = no_proxies
    return original_get(url, **kwargs)

# 覆写 requests.get 方法
requests.get = new_get



# 给我markdown格式的python3代码，提供函数，输入文件夹路径，挂载到localhost，制作一个本地服务器，可以通过url访问文件夹下的文件
def mount_server(path):
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    os.chdir(path)
    port = 8000
    httpd = HTTPServer(('', port), SimpleHTTPRequestHandler)
    print("Serving at port", port)
    httpd.serve_forever()

get_response_json = lambda response: json.loads(response.text)
'''get response's data in json'''

get_response_byte = lambda response: response.content
'''get response's data in bytes'''



# 为了使这段代码兼容 Python 3.6，你可以尝试以下修改：

# 使用 functools.partial 替换 lambda 函数。例如，将 getdir = lambda src:os.path.split(src)[0] 替换为 getdir = functools.partial(os.path.split, 1)。
# 使用 pathlib 模块替换手动拼接文件路径的方式。例如，将 os.path.join(os.path.split(src)[0] + ex, os.path.split(src)[1]) 替换为 Path(src).parent / (Path(src).name + ex)。
# 使用 with open 语句替换手动打开和关闭文件的方式。例如，将 open(src,'r',encoding=srccoding).read().splitlines() 替换为 with open(src, "r", encoding=srccoding) as f: f.read().splitlines()。
# 使用 f-strings 替换格式化字








# **************************
# 函数操作相关
# **************************

# fLoop = lambda func,argvs: list(x:=func(x,z) for z in argvs) and x
def fLoop(func, argvs):
    """
    对一个函数反复执行，并将结果存入列表中
    func: 待执行的函数
    argvs: 函数参数，为一个列表，列表中的每个元素都是一个函数参数
    """
    result = []
    for arg in argvs:
        result.append(func(*arg))
    return result
'''loop function with iterator'''

same = lambda x: x

run_in_thread_decorator = lambda f: lambda *args: threading.Thread(target=f, args=args).start()
'''开启另一个线程给函数，不阻塞'''

def get_print_output(func):
    '''获取函数print输出的装饰器'''
    import io
    def wrapper(*args, **kwargs):
        f = io.StringIO()
        sys.stdout = f
        func(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return f.getvalue()
    return wrapper

def donnot_print(func):
    '''不要输出的装饰器'''
    def inner(*args, **kwargs):
        sys.stdout = open(os.devnull, 'w')
        func(*args, **kwargs)
        sys.stdout = sys.__stdout__
    return inner

def just_try(func):
    '''不要输出的装饰器'''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print('run',str(func),'fail!')
    return inner


def get_current_function_file_dir():
    '''获取当前函数所在文件的路径'''
    import inspect
    a = inspect.currentframe().f_back.f_code.co_filename
    return os.path.dirname(a)


def module_exists(module_name):
    '''查看模块是否存在'''
    import importlib
    try:
        importlib.import_module(module_name)
    except ImportError:
        return False
    else:
        return True


def mod_checker(mod1=None,f1=None,mod2=lambda x: x,f2=None):
    '''模块存在检查或替换'''
    import importlib
    if module_exists(mod1):
        mod = importlib.import_module(mod1)
        if f1:
            return getattr(mod, f1)
        return mod
    if f2:
        mod = importlib.import_module(mod2)
        return getattr(mod, f2)
    return mod2

