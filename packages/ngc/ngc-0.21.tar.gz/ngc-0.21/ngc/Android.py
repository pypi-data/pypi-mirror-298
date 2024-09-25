import os
import re


def getAppInfoDics():
    '''get Android's apps info'''
    cmd = 'adb shell pm list packages -f'
    res = os.popen(cmd).read()
    if 'error' in res:
       return '请先选择设备'
    else:
       info_list = re.compile(r'(/.*/base\.apk)=(.*)').findall(res, re.M)
    return info_list

def pullAllApks(savedir):
    import ngc
    '''pull Android's all apps'''
    dic=getAppInfoDics()
    for it in ngc.mod_checker('tqdm','tqdm')(dic):
        savepath = os.path.join(savedir, it[1]+'.apk')
        os.system('adb pull '+it[0]+' "'+savepath+'"')

# 手机端开启adb tcp连接端口
# :/$su
# :/$setprop service.adb.tcp.port 5555
# :/$stop adbd
# :/$start adbd
# :/$ifconfig
# adb connect phone_ipaddress:portnumber
