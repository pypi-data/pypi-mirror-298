import time
import os
import platform
import wmi
import win32clipboard
import win32con


# 获取剪切板
def getClipboardText(fmat='GBK'):
    import win32con
    import win32clipboard as w
    w.OpenClipboard()
    d = w.GetClipboardData(win32con.CF_TEXT)
    w.CloseClipboard()
    return d.decode(fmat)

# 设置剪切板
def setClipboardText(aString):
    import win32con
    import win32clipboard as w
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_TEXT, aString)
    w.CloseClipboard()

'''
修改文件时间，人工
'''
def modify_file_time(filePath, createTime=None, modifyTime=None, accessTime=None, offset=(0, 1, 2)):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param filePath: 文件路径名
    :param createTime: 创建时间
    :param modifyTime: 修改时间
    :param accessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    from win32file import CreateFile, SetFileTime, GetFileTime, CloseHandle
    from win32file import GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
    from pywintypes import Time
    def timeOffsetAndStruct(times, format, offset):
        return time.localtime(time.mktime(time.strptime(times, format)) + offset)
    try:
        format = "%Y-%m-%d %H:%M:%S"  # 时间格式
        cTime_t,aTime_t,mTime_t=createTime, accessTime, modifyTime
        if createTime:
            cTime_t = timeOffsetAndStruct(createTime, format, offset[0])
        if modifyTime:
            mTime_t = timeOffsetAndStruct(modifyTime, format, offset[1])
        if accessTime:
            aTime_t = timeOffsetAndStruct(accessTime, format, offset[2])
        fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        createTimes, accessTimes, modifyTimes = GetFileTime(fh)
        if cTime_t:
            createTimes = Time(time.mktime(cTime_t))
        if aTime_t:
            accessTimes = Time(time.mktime(aTime_t))
        if mTime_t:
            modifyTimes = Time(time.mktime(mTime_t))
        SetFileTime(fh, createTimes, accessTimes, modifyTimes)
        CloseHandle(fh)
        return 0
    except:
        return 1




def modify_file_time2(filepath, ctime, mtime, atime):
    os.utime(filepath, (mtime, atime))



def get_system_info1():
    c = wmi.WMI()
    for sys in c.Win32_ComputerSystem():
        print("CPU型号: %s" % sys.Name.split(' ')[0])
    for gpu in c.Win32_VideoController():
        print("显卡型号: %s" % gpu.Name)
    for mem in c.Win32_PhysicalMemory():
        print("内存型号: %s, 内存大小: %s" % (mem.Name, mem.Capacity))



# 给我markdown格式的python代码，提供函数，获取电脑型号、操作系统、处理器型号、主板型号、显卡型号、内存型号和大小、主硬盘型号和大小、显示器型号（我的操作系统是windows 10）

def get_computer_info():
    # # 获取电脑型号
    # computer_model = platform.node()
    # # 获取操作系统
    # system_name = platform.system()
    # # 获取处理器型号
    # processor_name = platform.processor()
    # 获取主板型号
    c = wmi.WMI()

    # --------
    print_msg = lambda msg: print(msg) if msg is not None else None

    # get computer model
    for sys in c.Win32_ComputerSystem():
        computer_model = sys.Model
    # get os version
    for os in c.Win32_OperatingSystem():
        os_version = os.Caption
    # get processor model
    for processor in c.Win32_Processor():
        processor_model = processor.Name
    
    motherboard_name = c.Win32_BaseBoard()[0].Product

    print_msg("电脑型号：{}".format(computer_model))
    print_msg("操作系统：{}".format(os_version))
    print_msg("处理器型号：{}".format(processor_model))
    print_msg("主板型号：{}".format(motherboard_name))
    
    # 获取集成显卡型号
    integrated_graphics_name = c.Win32_VideoController()[0].Name
    integrated_graphics_memory = c.Win32_VideoController()[0].AdapterRAM

    for i,videoController in enumerate(c.Win32_VideoController()):
        print_msg("显卡{}型号：{}".format(i+1,videoController.Caption))
        print_msg("显卡{}显存大小：{} GB".format(i+1,abs(videoController.AdapterRAM) / 1024 / 1024 / 1024))
    
    # 获取内存条型号和数量和大小
    memory_num = len(c.Win32_PhysicalMemory())
    memory_size = sum(int(x.Capacity) for x in c.Win32_PhysicalMemory())
    print_msg("内存条数量：{}".format(memory_num))
    for i,physicalMemory in enumerate(c.Win32_PhysicalMemory()):
        print_msg("内存条{}型号：{}".format(i+1,physicalMemory.Name))
        print_msg("内存条{}大小：{} GB".format(i+1,int(physicalMemory.Capacity) / 1024 / 1024 / 1024))

    # 获取主硬盘型号和大小
    disk_name = c.Win32_DiskDrive()[0].Model
    disk_size = c.Win32_DiskDrive()[0].Size

    for physical_disk in c.Win32_DiskDrive ():
        for partition in physical_disk.associators ("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators ("Win32_LogicalDiskToPartition"):
                if logical_disk.Caption == 'C:':
                    disk_name = physical_disk.Model
                    disk_size = physical_disk.Size

    print_msg("主硬盘型号：{}".format(disk_name))
    print_msg("主硬盘大小：{} GB".format(int(disk_size) / 1024 / 1024 / 1024))

    # 获取显示器型号
    monitor_name = c.Win32_DesktopMonitor()[0].Name
    monitor_model = c.Win32_DesktopMonitor()[0].Caption
    # 获取屏幕尺寸
    screen_size = c.Win32_DesktopMonitor()[0].ScreenHeight
    for item in c.Win32_DesktopMonitor():
        ScreenWidth = item.ScreenWidth
        ScreenHeight = item.ScreenHeight
    
    print_msg("显示器型号：{}".format(monitor_model))
    print_msg("屏幕尺寸：{}x{}".format(ScreenWidth,ScreenHeight))


    # 获取电池出厂设计容量
    for battery in c.Win32_Battery():
        design_capacity = battery.DesignCapacity

    # 获取电池损耗百分比
    for battery in c.Win32_Battery():
        battery_percentage = battery.EstimatedChargeRemaining
        
    # print_msg("电池出厂设计容量：{}".format(design_capacity))
    # print_msg("电池损耗：{}".format(battery_percentage))
    # return computer_model, system_name, processor_name, motherboard_name, integrated_graphics_name, dedicated_graphics_name, dedicated_graphics_memory, memory_type, memory_num, memory_size, disk_name, disk_size, monitor_name, screen_size
    # computer_model, system_name, processor_name, motherboard_name, integrated_graphics_name, dedicated_graphics_name, dedicated_graphics_memory, memory_type, memory_num, memory_size, disk_name, disk_size, monitor_name, screen_size = get_computer_info()





'''
显示器亮度
'''
# def changeBrightness(level=10):














# # 获取剪切板上的富文本
# win32clipboard.OpenClipboard()
# data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
# win32clipboard.CloseClipboard()

# # 输出剪切板上的富文本
# print(data)

# # 保存剪切板上的富文本
# with open('data/rich_text.txt', 'w', encoding='u8') as f:
#     f.write(data)








# # 导入pyperclip和python-docx库
# import pyperclip
# import docx

# # 从剪切板获取富文本
# rich_text = pyperclip.paste()

# # 将富文本保存为html文件
# with open('data/rich_text.html', 'w', encoding='u8') as f:
#     f.write(rich_text)

# # 将富文本保存为word文件
# document = docx.Document()
# document.add_paragraph(rich_text)
# document.save('data/rich_text.docx')












def kalkule():
    import tkinter as tk

    # 创建窗口
    window = tk.Tk()
    window.title('Calculator')
    window.geometry('300x200')

    # 创建文本框
    e1 = tk.Entry(window, width=30)
    e1.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    # 创建输出文本框
    t1 = tk.Text(window, width=30, height=2)
    t1.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    # 定义计算函数
    def calc():
        expression = e1.get()
        try:
            result = eval(expression)
            t1.delete(1.0, tk.END)
            t1.insert(tk.END, result)
        except Exception as e:
            t1.delete(1.0, tk.END)
            t1.insert(tk.END, 'Error')

    # 创建计算按钮
    b1 = tk.Button(window, text='Calculate', command=calc)
    b1.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    # 绑定回车键
    window.bind('<Return>', lambda event: calc())

    # 运行窗口
    window.mainloop()








# 给我markdown格式的python3函数，输入exe文件，提取图标文件输出保存

# def extract_icon_file(exe_file_path, icon_file_path):
#     """
#     提取exe文件中的图标文件并保存到指定位置

#     Parameters
#     ----------
#     exe_file_path: str
#         exe文件路径
#     icon_file_path: str
#         图标文件保存路径

#     Returns
#     -------
#     None
#     """
#     # 创建图标文件保存路径
#     if not os.path.exists(icon_file_path):
#         os.mkdir(icon_file_path)

#     # 提取exe文件中的图标文件
#     exe_file = open(exe_file_path, 'rb')
#     exe_file.seek(0x3c)
#     pe_offset = struct.unpack('<I', exe_file.read(4))[0]
#     exe_file.seek(pe_offset)
#     pe_signature = exe_file.read(4)
#     if pe_signature == b'PE\x00\x00':
#         exe_file.seek(pe_offset + 6)
#         num_of_resources = struct.unpack('<H', exe_file.read(2))[0]
#         exe_file.seek(pe_offset + 0x54)
#         resource_table_offset = struct.unpack('<I', exe_file.read(4))[0]
#         for i in range(num_of_resources):
#             exe_file.seek(resource_table_offset + 0x08 + i*0x08)
#             resource_type_offset = struct.unpack('<I', exe_file.read(4))[0]
#             exe_file.seek(resource_type_offset + 0x04)
#             resource_type_id = struct.unpack('<H', exe_file.read(2))[0]
#             if resource_type_id == 3:
#                 exe_file.seek(resource_type_offset + 0x10)
#                 resource_name_offset = struct.unpack('<I', exe_file.read(4))[0]
#                 exe_file.seek(resource_name_offset + 0x04)
#                 resource_name_id = struct.unpack('<H', exe_file.read(2))[0]
#                 exe_file.seek(resource_name_offset + 0x08)
#                 resource_name_offset = struct.unpack('<I', exe_file.read(4))[0]
#                 exe_file.seek(resource_name_offset)
#                 resource_name = exe_file.read(resource_name_id).decode('utf-16')
#                 exe_file.seek(resource_type_offset + 0x08)
#                 resource_offset = struct.unpack('<I', exe_file.read(4))[0]
#                 exe_file.seek(resource_offset + 0x08)
#                 offset_to_data = struct.unpack('<I', exe_file.read(4))[0]
#                 exe_file.seek(offset_to_data + 0x10)
#                 size_of_data = struct.unpack('<I', exe_file.read(4))[0]
#                 exe_file.seek(offset_to_data + 0x14)
#                 offset_to_data = struct.unpack('<I', exe_file.read(4))[0]
#                 exe_file.seek(offset_to_data)
#                 icon_data = exe_file.read(size_of_data)
#                 icon_file_name = resource_name + '.ico'
#                 icon_file_path = os.path.join(icon_file_path, icon_file_name)
#                 with open(icon_file_path, 'wb') as icon_file:
#                     icon_file.write(icon_data)
#     exe_file.close()









def file_type(file_path):
    """
    根据文件头判断并输出文件类型（类似file命令）
    
    Parameters:
    file_path: 文件路径
    
    Returns:
    文件类型
    """
    # 定义文件头与文件类型映射表
    file_type_dict = {
        b'\xFF\xD8\xFF\xE0': 'JPEG',
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'PNG',
        b'\x47\x49\x46\x38\x39\x61': 'GIF',
        b'\x42\x4D': 'BMP',
        b'\x25\x50\x44\x46': 'PDF',
        b'\xD0\xCF\x11\xE0': 'DOC',
        b'\x52\x61\x72\x20\x1A\x07\x00': 'RAR',
        b'\x50\x4B\x03\x04': 'ZIP',
        b'\x25\x21\x50\x53': 'PS',
        b'\x4D\x5A': 'EXE'
    }
    
    # 读取文件头
    with open(file_path, 'rb') as f:
        file_head = f.read(8)
    
    # 根据文件头判断文件类型
    file_type = 'Unknown'
    for head, type in file_type_dict.items():
        if file_head.startswith(head):
            file_type = type
            break
    return file_type




