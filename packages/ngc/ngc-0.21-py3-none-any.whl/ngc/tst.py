import os,sys,glob,zlib,pathlib
import ngc
import shutil

fork_dir = lambda src,dst,*arg: shutil.copytree(src,dst,arg) if not os.path.exists(dst) else None

import os
import shutil
import random


def traverse_dir(dir_path, postfix=None, include_dir=False, level=None, only_filename=False):
    """
    遍历文件夹
    :param dir_path: 文件夹路径
    :param postfix: 文件后缀名，可以是字符串或者列表，默认为None，表示不按照后缀名过滤
    :param include_dir: 结果是否包含文件夹，默认False，不包含
    :param level: 遍历层数，None表示全部层数，默认为None
    :param only_filename: 是否只显示文件名，默认False，表示显示完整路径
    :return: 文件/文件夹列表
    """
    if not os.path.exists(dir_path):
        return []
    # 定义结果列表
    result_list = []
    # 获取文件夹下所有文件/文件夹
    dir_list = os.listdir(dir_path)
    # 遍历文件夹/文件夹
    for file_name in dir_list:
        # 获取完整路径
        file_path = os.path.join(dir_path, file_name)
        # 如果是文件夹
        if os.path.isdir(file_path):
            # 如果需要包含文件夹
            if include_dir:
                # 是否只显示文件名
                if only_filename:
                    result_list.append(file_name)
                else:
                    result_list.append(file_path)
            # 如果需要遍历子文件夹
            if level is None or level > 0:
                # 遍历子文件夹
                result_list += traverse_dir(file_path, postfix, include_dir, level - 1 if level else None, only_filename)
        # 如果是文件
        elif os.path.isfile(file_path):
            # 如果指定了文件后缀
            if postfix:
                # 如果是字符串
                if isinstance(postfix, str):
                    # 如果文件后缀名匹配
                    if file_name.endswith(postfix):
                        # 是否只显示文件名
                        if only_filename:
                            result_list.append(file_name)
                        else:
                            result_list.append(file_path)
                # 如果是列表
                elif isinstance(postfix, list):
                    # 如果文件后缀名匹配
                    if file_name.endswith(tuple(postfix)):
                        # 是否只显示文件名
                        if only_filename:
                            result_list.append(file_name)
                        else:
                            result_list.append(file_path)
            # 如果没有指定文件后缀
            else:
                # 是否只显示文件名
                if only_filename:
                    result_list.append(file_name)
                else:
                    result_list.append(file_path)
    # 返回结果列表
    return result_list
    





import importlib
import inspect

def export_func(func, py_file):
    """
    导出函数func的完整代码和包依赖，输出到独立的py文件中
    :param func: 函数
    :param py_file: 输出py文件
    :return: None
    """
    # 获取函数定义所在模块
    module_name = func.__module__
    module_obj = importlib.import_module(module_name)

    # 获取函数定义
    source_code = inspect.getsource(func)

    # 获取函数所依赖的模块
    module_dependencies = set(module_obj.__dict__.keys())
    module_dependencies.remove('__builtins__')
    module_dependencies = [module for module in module_dependencies if not module.startswith('_')]

    # 导出函数定义和依赖模块
    with open(py_file, 'w') as f:
        for module in module_dependencies:
            f.write(f'import {module}\n')
        f.write(source_code)

def func(i=0):
    import os,sys
    print(i)


import inspect
import os

def expf(func, file_name):
    """
    将一个函数的完整代码和依赖的模块导出到独立的py文件中
    :param file_name: 导出的py文件的文件名
    """

    # 获取func函数的完整代码和依赖的模块
    code = inspect.getsource(func)
    modules = inspect.getmodule(func)

    # 将func函数的完整代码和依赖的模块写入到py文件中
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('import {}\n\n'.format(modules.__name__))
        f.write(code)




from ngc import dirlist

# 将func函数导出到独立的py文件中
# func('func.py')
# export_func(dirlist,'func.py')
# expf(dirlist,'func.py')

def donnot_print(func): 
    def inner(*args, **kwargs): 
        import sys 
        sys.stdout = open(os.devnull, 'w') 
        func(*args, **kwargs) 
        sys.stdout = sys.__stdout__ 
    return inner

@donnot_print
def func():
    global i
    print(123)
    i+=1

if __name__=='__main__':
    i=0
    print(i)
    func()
    print(i)

