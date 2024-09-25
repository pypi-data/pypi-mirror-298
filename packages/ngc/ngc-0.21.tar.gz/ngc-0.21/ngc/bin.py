import os
import hashlib
import zlib
import re


# 二进制加密、压缩、读写

writeIntsToBytes = lambda lis,dst: open(dst,'wb').write(bytes(lis))
'''将给定的整数列表写入指定的字节文件中。'''
getHexString = lambda hex,encode: bytes.fromhex(hex(hex)[2:]).decode(encode)
'''将十六进制字符串转换成指定编码的字符串'''
fin_lambda = lambda dat,src:open(src,'wb+').write(bytes.fromhex(dat))
'''将传入的16进制数据（dat）转换成字节数据，并将其写入指定的文件（src）中'''
fout=lambda src: open(src, 'rb').read().hex()
'''将文件的内容转换成十六进制字符串'''

getStrMD5 = lambda str: hashlib.md5(str).hexdigest()
'''计算字符串的MD5值'''

def getFileMD5(file):
    '''计算文件的MD5值'''
    m = hashlib.md5()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(2**13), b''): m.update(chunk)
    return m.hexdigest()

def writeQt(mylist,dst):
    '''
    QDataStream写文件
    '''
    from PyQt5.QtCore import QDataStream, QIODevice, QFile
    buf=QFile(dst)
    buf.open(QIODevice.WriteOnly)
    dStream = QDataStream(buf)
    dStream.setVersion(QDataStream.Qt_4_5)
    for item in mylist:
        dStream.writeQVariant(item)
    buf.close()

def readQt(dst):
    '''
    QDataStream读文件
    '''
    from PyQt5.QtCore import QDataStream, QIODevice, QFile
    buf=QFile(dst)
    buf.open(QIODevice.ReadOnly)
    dStream = QDataStream(buf)
    dStream.setVersion(QDataStream.Qt_4_5)
    mylist = []
    while not dStream.atEnd():
        item = dStream.readQVariant()
        mylist.append(item)
    buf.close()
    return mylist


def zlib_decompress(src, dst, bytesize=1024 * 1024):
    '''
    zlib解压缩文件，level 越小越快
    '''
    src = open(src, 'rb')
    dst = open(dst, 'wb')
    decompress = zlib.decompressobj()
    data = src.read(bytesize)
    while data:
        dst.write(decompress.decompress(data))
        data = src.read(bytesize)
    dst.write(decompress.flush())

def zlib_compress(src, dst, level=1, bytesize=1024 * 1024):
    '''
    zlib压缩文件，level 越小越快
    '''
    src = open(src, 'rb')
    dst = open(dst, 'wb')
    compress = zlib.compressobj(level)
    data = src.read(bytesize)
    while data:
        dst.write(compress.compress(data))
        data = src.read(bytesize)
    dst.write(compress.flush())

def pack_iso(root_dir,dst,vol_ident=''):
    import pathlib
    '''打包iso'''
    import pycdlib
    iso = pycdlib.PyCdlib()
    iso.new(
        interchange_level=3, #  interchange_level=1,
        vol_ident=vol_ident, #  vol_ident='',
        joliet=True, #  joliet=None,
        rock_ridge='1.09',
        xa=True,
        )
    print('Start packing...')
    filelist=pathlib.Path(root_dir).rglob('*')
    for src in filelist:
        jpath=src.replace(root_dir,'')
        if os.path.isdir(src):
            iso.add_directory(joliet_path=jpath)
        elif os.path.isfile(src):
            iso.add_file(src,joliet_path=jpath)
    iso.write(dst)
    iso.close()
    print('Finished.')


# 提取可编码字符串

def extract_gbk_str(filename):
    '''定义一个函数，用于提取可以使用GBK编码提取的字符串'''
    # 判断文件是否存在
    if not os.path.exists(filename):
        return None
    # 打开文件
    with open(filename, 'rb') as f:
        # 读取文件内容
        content = f.read()
        # 通过正则表达式提取字符串
        gbk_str_list = re.findall(b'[\x80-\xff]+', content)
        # 将字节数组转换为字符串
        # gbk_str_list = [str(s, 'gbk') for s in gbk_str_list]
        new_gbk_str_list=[]
        for s in gbk_str_list:
            try:
                x=str(s, 'gbk')
                new_gbk_str_list.append(x+'\n')
            except:
                pass
        # 返回字符串列表
        return new_gbk_str_list

