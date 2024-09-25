import requests
import html
import json
import re
import os


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service  # 新增
from selenium.webdriver.common.by import By

# HOST添加屏蔽chrome更新
# 127.0.0.1 update.googleapis.com

def get_url_xpath_content(url,xpath1):
    from lxml import etree
    #请求头和目标网址
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
    }
    #获取和解析网页
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    try:
        dom = etree.HTML(r.text).xpath(xpath1)[0]
        return html.unescape(etree.tostring(dom,encoding='utf-8').decode('utf-8'))
    except: return ''

def get_Chrome_Header(src):
    if os.path.isfile(src):
        element = open(src,encoding='u8').readlines()
    else:
        element = src.splitlines()
    
    headers = {}
    for e in element:
        pos = re.search(':', e)
        if pos is not None:
            fir, sec = pos.regs[0]
            key, value = e[:fir], e[sec:]
            headers[key] = value.lstrip()
    return headers

def get_Chrome_Payload(src):
    if os.path.isfile(src):
        element = open(src,encoding='u8').readlines()
    else:
        element = src.splitlines()
    
    nl=[]
    for line in element:
        print(line)
        if line.endswith(': '):
            nl.append(line)
        else:
            nl[-1]+=line
    element=nl
    Payload = {}
    for e in element:
        pos = re.search(':', e)
        if pos is not None:
            fir, sec = pos.regs[0]
            key, value = e[:fir], e[sec:]
            Payload[key] = value.lstrip()
    return Payload



def start_browser():
    os.system('start chrome.exe --remote-debugging-port=9999 --user-data-dir="D:\\test"')

def init_driver():
    # 设置Chrome浏览器的选项
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
    driver = webdriver.Chrome(options=chrome_options)
    return driver
