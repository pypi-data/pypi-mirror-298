import numpy as np
import cv2
import os
from PIL import Image, ImageOps

# http://c.biancheng.net/pillow/

# 作用：将indir里面的jpg逐个显示，用户照着四边形四点选取的方法逐个点击漫画框线边角，输出一个个的图片

'''
公共变量区
'''
pic_n = 0
pic_cnt = 0
# corner
z1 = [0, 0]
z2 = [0, 0]
z3 = [0, 0]
z4 = [0, 0]
zs = [z1, z2, z3, z4]






# **************************
# 图像相关
# **************************



'''
in,out,text,x,y,width
一次性使用方法 ImgText(src,dst , text, x, y, 1080, 50).draw_text()
'''
class ImgText:

    # font = ImageFont.truetype("msyh.ttc", 50) # 字体文件、字体大小
    def __init__(self, infile,outfile,text,x,y,width=1080,fontsize=50):
        from PIL import ImageFont
        self.infile = infile
        self.outfile = outfile
        self.x = x
        self.y = y
        self.font = ImageFont.truetype("msyh.ttc", fontsize)

        # 预设宽度 可以修改成你需要的图片宽度
        self.width = width # 文字的放置宽度
        # 文本
        self.text = text
        # 段落 , 行数, 行高
        self.duanluo, self.note_height, self.line_height = self.split_text()
        self.draw_text()

    def get_duanluo(self, text):
        from PIL import ImageDraw
        txt = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)
        # 所有文字的段落
        duanluo = ""
        # 宽度总和
        sum_width = 0
        # 几行
        line_count = 1
        # 行高
        line_height = 0
        for char in text:
            width, height = draw.textsize(char, self.font)
            sum_width += width
            if sum_width > self.width:  # 超过预设宽度就修改段落 以及当前行数
                line_count += 1
                sum_width = 0
                duanluo += '\n'
            duanluo += char
            line_height = max(height, line_height)
        if not duanluo.endswith('\n'):
            duanluo += '\n'
        return duanluo, line_height, line_count

    def split_text(self):
        # 按规定宽度分组
        max_line_height, total_lines = 0, 0
        allText = []
        for text in self.text.split('\n'):
            duanluo, line_height, line_count = self.get_duanluo(text)
            max_line_height = max(line_height, max_line_height)
            total_lines += line_count
            allText.append((duanluo, line_count))
        line_height = max_line_height
        total_height = total_lines * line_height
        return allText, total_height, line_height

    def draw_text(self):
        from PIL import ImageDraw
        """
        绘图以及文字
        :return:
        """
        infile = self.infile
        outfile = self.outfile
        note_img = Image.open(infile) #.convert("RGBA")
        draw = ImageDraw.Draw(note_img)
        # 左上角开始
        x = self.x # 文字左上角的放置坐标
        y = self.y # 文字左上角的放置坐标
        for duanluo, line_count in self.duanluo:
            draw.text((x, y), duanluo, fill=(255, 255, 255), font=self.font) # fill是颜色
            y += self.line_height * line_count
        note_img.save(outfile)

'''
大裁剪，cutyes=0则只是放大到容器大小 =1规则化，通用
'''
def ScaleImageWithPadding(infile, wanlen, wanwidth, dst=None, cutyes=1, fill_color=(0, 0, 0), *arg):
    # if dst and os.path.exists(dst):
    #     return False
    if dst and os.path.exists(os.path.split(dst)[0]) == 0:
        os.makedirs(os.path.split(dst)[0])
    img = Image.open(infile)
    lenmore = True
    imgsize = img.size
    relength = wanlen
    rewidth = wanwidth
    if (imgsize[0] / imgsize[1] < wanlen / wanwidth):
        # print(imgsize)
        lenmore = True
        relength = int(imgsize[0] * wanwidth / imgsize[1])
        out = img.resize((relength, wanwidth), Image.LANCZOS)  # 抗毛刺 Image.ANTIALIAS
    else:
        # print(imgsize)
        lenmore = False
        rewidth = int(imgsize[1] * wanlen / imgsize[0])
        out = img.resize((wanlen, rewidth), Image.LANCZOS)

    if cutyes == 1:
        # 裁剪
        if lenmore:
            left = int(relength / 2 - wanlen / 2)
            cropped = out.crop((left, 0, left + wanlen, wanwidth))
        else:
            right = int(rewidth / 2 - wanwidth / 2)
            cropped = out.crop((0, right, wanlen, right + wanwidth))
        

        # 填充
        delta_w = wanlen - cropped.size[0]
        delta_h = wanwidth - cropped.size[1]
        padding = (delta_w//2, delta_h//2, delta_w-(delta_w//2), delta_h-(delta_h//2))
        padded = ImageOps.expand(cropped, padding, fill=fill_color)

        if dst:
            # cropped.save(dst,*arg)
            padded.save(dst, *arg)
            return
        return cropped
    if dst:
        # out.save(dst,*arg)
        padded.save(dst, *arg)
        return
    # return out
    return padded


'''
小裁剪，cutyes=0则只是放大到容器大小 =1规则化，不通用
'''
def ScaleImageWithCropping(infile,wanlen,wanwidth,dst=None,srcdir="",dstdir="",cutyes=1,**kwargs):
    # if dst and os.path.exists(dst):
    #     return False
    if dst and os.path.exists(os.path.split(dst)[0]) == 0:
        os.makedirs(os.path.split(dst)[0])

    img = Image.open(infile)
    # img.show()
    # grayimg = img.convert('L')
    # grayimg.save(outfile)
    lenmore = True
    imgsize = img.size
    relength = wanlen
    rewidth = wanwidth
    if (imgsize[0] / imgsize[1] > wanlen / wanwidth):
        # print(imgsize)
        lenmore = True
        relength = int(imgsize[0] * wanwidth / imgsize[1])
        # print("len more" + str(relength))
        out = img.resize((relength, wanwidth), Image.LANCZOS)  # 抗毛刺
    else:
        # print(imgsize)
        lenmore = False
        rewidth = int(imgsize[1] * wanlen / imgsize[0])
        out = img.resize((wanlen, rewidth), Image.LANCZOS)
    if cutyes == 1:
        # 裁剪 : 左上x，左上y，右下x，右下y
        if lenmore:
            left = int(relength / 2 - wanlen / 2)
            cropped = out.crop((left, 0, left + wanlen, wanwidth))
        else:
            right = int(rewidth / 2 - wanwidth / 2)
            cropped = out.crop((0, right, wanlen, right + wanwidth))
        if dst:
            cropped.save(dst,**kwargs)
            return
        return cropped
    if dst:
        out.save(dst,**kwargs)
        return
    return out


def ZoomImage(src,wdth=0,hght=0):
    img = Image.open(src)
    imgsize = img.size
    if wdth!=0:
        x,y = wdth, imgsize[1]/imgsize[0]*wdth
    elif hght!=0:
        x,y = imgsize[0]/imgsize[1]*hght,hght
    else:
        x,y=imgsize[0],imgsize[1]
    x,y=int(x),int(y)
    img=img.resize((x, y), Image.ANTIALIAS)
    img.save(src)


def image_cat(lis,dst,xnum=None,size=None):
    if not xnum:
        xnum=int((len(lis)-1)**0.5)+1
    ynum=int(len(lis)/xnum)
    if xnum*ynum<len(lis): ynum+=1
    if not size:size=Image.open(lis[0]).size
    rgbaImg = Image.new('RGBA', (xnum * size[0], ynum * size[1])) #创建一个新图
    ix = iy = 0
    print(xnum,ynum)
    for it in lis:
        print(it)
        it = ScaleImageWithPadding(it,size[0],size[1])
        rgbaImg.paste(it, (ix * size[0], iy * size[1]))
        ix = (ix+1)%xnum
        if ix == 0:iy = (iy+1)%ynum
    try:
        rgbaImg.save(dst)
    except:
        rgbImg=rgbaImg.convert("RGB")
        rgbImg.save(dst)

# 漫画手动切割
def MangaPiece(infile, srcdir="", dstdir=""):
    def solve(zs):
        global pic_n
        
        if srcdir == "" or dstdir == "" or srcdir == dstdir:
            outfile = infile
            outfile = os.path.split(outfile)[0] + \
                      "/" + os.path.split(outfile)[1].replace(".", "-" + str(pic_n) + ".").replace("jpg", "png")
        else:
            outfile = os.path.split(infile)[0].replace(srcdir, dstdir) +\
                      "/" + os.path.split(infile)[1].replace(".", "-" + str(pic_n) + ".").replace("jpg", "png")
        if os.path.exists(outfile):
            return False
        if os.path.exists(os.path.split(outfile)[0]) == 0:
            os.makedirs(os.path.split(outfile)[0])
        print(outfile)
        b = np.array(zs, dtype=np.int32)

        roi_t = []
        for i in range(4):
            roi_t.append(b[i])
        roi_t = np.asarray(roi_t)
        roi_t = np.expand_dims(roi_t, axis=0)
        im = np.zeros(image.shape[:2], dtype="uint8")

        # 生成切割后的底色为黑，四边形为白色的图片
        cv2.polylines(im, roi_t, 1, 255)
        cv2.fillPoly(im, roi_t, 255)

        mask = im
        # masked是黑底白四边形与原图片与运算后的图片也就是背景黑的切割后的cv2图片
        masked = cv2.bitwise_and(image, image, mask=mask)

        # # 底色透明化的切割，出问题：产生透明点，而且色调有变化。不建议使用
        # array = np.zeros((masked.shape[0], masked.shape[1], 4), np.uint8)
        # array[:, :, 0:3] = masked
        # array[:, :, 3] = 0
        # array[:, :, 3][np.where(array[:, :, 0] > 2)] = 255
        # array[:, :, 3][np.where(array[:, :, 1] > 2)] = 255
        # array[:, :, 3][np.where(array[:, :, 2] > 2)] = 255
        # print(array.max())
        # image_1 = Image.fromarray(array)

        # 补充部分：四边形的最小外接矩形

        x1 = min(zs[0][0], zs[1][0], zs[2][0], zs[3][0])
        y1 = min(zs[0][1], zs[1][1], zs[2][1], zs[3][1])
        x2 = max(zs[0][0], zs[1][0], zs[2][0], zs[3][0])
        y2 = max(zs[0][1], zs[1][1], zs[2][1], zs[3][1])

        # # 透明化的生成image_1的矩形生成保存。
        # cropped = image_1.crop((x1, y1, x2, y2))
        # cropped.save(outdir+"/"+os.path.split(filename)[1].replace(".","-"+str(n)+".").replace("jpg","png"), "PNG")
        # n = n + 1

        # 黑区化的
        image_1 = Image.fromarray(masked)

        # 切割
        masked = masked[y1:y2, x1:x2]

        # 保存
        cv2.imwrite(outfile,masked)

        # 序号自增
        pic_n = pic_n + 1

    # 点击四次之后调用四边形切割函数
    def judgeSolve(x, y):
        global z1, z2, z3, z4, zs, pic_cnt
        pic_cnt = (pic_cnt + 1)
        if pic_cnt == 1:
            z1 = [x, y]
        elif pic_cnt == 2:
            z2 = [x, y]
        elif pic_cnt == 3:
            z3 = [x, y]
        else:
            z4 = [x, y]
            zs = [z1, z2, z3, z4]
            solve(zs)
        pic_cnt = pic_cnt % 4


    # 鼠标左键单击响应事件
    def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            judgeSolve(x, y)
            # print(xy)
            print(x)
            print(y)

    image = cv2.imread(infile)
    img = image

    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    # cv2.destroyAllWindow()

# 漫画切割中间函数
def MangaPieceFormat(infile,outfile, srcdir="", dstdir="",zs=None):
    global pic_n
    if srcdir == "" or dstdir == "" or srcdir == dstdir:
        outfile = infile
        outfile = os.path.split(outfile)[0] + \
                  "/" + os.path.split(outfile)[1].replace(".", "-" + str(pic_n) + ".").replace("jpg", "png")
    else:
        outfile = os.path.split(infile)[0].replace(srcdir, dstdir) + \
                  "/" + os.path.split(infile)[1].replace(".", "-" + str(pic_n) + ".").replace("jpg", "png")
    if os.path.exists(outfile):
        return False
    if os.path.exists(os.path.split(outfile)[0]) == 0:
        os.makedirs(os.path.split(outfile)[0])

    if zs == None:
        zs = [[0, 0], [0, 0], [0, 0], [0, 0]]
    # def solve(zs):
    image = cv2.imread(infile)
    img = image
    # solve(zs)
    # global n
    b = np.array(zs, dtype=np.int32)

    roi_t = []
    for i in range(4):
        roi_t.append(b[i])
    roi_t = np.asarray(roi_t)
    roi_t = np.expand_dims(roi_t, axis=0)
    im = np.zeros(image.shape[:2], dtype="uint8")

    # 生成切割后的底色为黑，四边形为白色的图片
    cv2.polylines(im, roi_t, 1, 255)
    cv2.fillPoly(im, roi_t, 255)

    mask = im
    # masked是黑底白四边形与原图片与运算后的图片也就是背景黑的切割后的cv2图片
    masked = cv2.bitwise_and(image, image, mask=mask)

    # # 底色透明化的切割，出问题：产生透明点，而且色调有变化。不建议使用
    # array = np.zeros((masked.shape[0], masked.shape[1], 4), np.uint8)
    # array[:, :, 0:3] = masked
    # array[:, :, 3] = 0
    # array[:, :, 3][np.where(array[:, :, 0] > 2)] = 255
    # array[:, :, 3][np.where(array[:, :, 1] > 2)] = 255
    # array[:, :, 3][np.where(array[:, :, 2] > 2)] = 255
    # print(array.max())
    # image_1 = Image.fromarray(array)

    # 补充部分：四边形的最小外接矩形

    x1 = min(zs[0][0], zs[1][0], zs[2][0], zs[3][0])
    y1 = min(zs[0][1], zs[1][1], zs[2][1], zs[3][1])
    x2 = max(zs[0][0], zs[1][0], zs[2][0], zs[3][0])
    y2 = max(zs[0][1], zs[1][1], zs[2][1], zs[3][1])

    # # 透明化的生成image_1的矩形生成保存。
    # cropped = image_1.crop((x1, y1, x2, y2))
    # cropped.save(outdir+"/"+os.path.split(filename)[1].replace(".","-"+str(n)+".").replace("jpg","png"), "PNG")
    # n = n + 1

    # 黑区化的
    image_1 = Image.fromarray(masked)

    # 切割
    masked = masked[y1:y2, x1:x2]

    # 保存
    cv2.imwrite(outfile, masked)

    # 序号自增
    pic_n = pic_n + 1


'''判断图片是黑=0是白=128； num=True返回色值'''
def whetherImageDark(src,num = False,lineway = 30):
    from scipy import stats
    img = np.array(Image.open(src))  # 读取图片
    uL = stats.mode(img[lineway])[0][0]
    u = uL
    if str(type(uL)) == "<class 'numpy.ndarray'>":
        if len(set(uL)) != 1:
            print("fake "+str(uL)+src)
            u = min(x for x in uL)
        else:
            u = uL[0]
    if num == True:
        return u
    if u < 128:
        return True
    else:
        return False



'''反正图片颜色，覆盖'''
def reverseImageColor(src,dst=None):
    from PIL import Image
    import PIL.ImageOps
    # 读入图片
    image = Image.open(src)
    image = image.convert('L')
    inverted_image = PIL.ImageOps.invert(image)
    if dst == None:
        inverted_image.save(src)
    else:
        inverted_image.save(dst)



def img_simpleConcat(img,dst='test.jpg',axis=1):
    im1=np.array(Image.open(img[0]))
    for im in img[1:]:
        print(im)
        im=np.array(Image.open(im))
        im1=np.concatenate((im1,im),axis)
    Image.fromarray(im1).save(dst)


'''饼图'''
def makePatDraw(label,values):
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
    plt.figure(figsize=(6, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
    # label=['第一','第二','第三']#定义饼图的标签，标签是列表
    # explode=[0.01,0.01,0.01]#设定各项距离圆心n个半径
    # plt.pie(values[-1,3:6],explode=explode,labels=label,autopct='%1.1f%%')#绘制饼图
    # values=[4,7,9]
    explode = list(0.01 for i in range(0,len(label)))
    plt.pie(values, explode=explode, labels=label, autopct='%1.1f%%')  # 绘制饼图
    plt.title('占比统计')  # 绘制标题
    plt.savefig('./饼图')  # 保存图片
    # plt.show()
    return
















def compressImages(src,dst,multi=0,x=0,y=0):
    sImg = Image.open(src)
    w, h = sImg.size
    if x!=0 and y!=0:
        dImg = sImg.resize((x, y), Image.ANTIALIAS)
        dImg.save(dst)
    elif multi!=0:
        dImg = sImg.resize((int(w*multi), int(h*multi)), Image.ANTIALIAS)
        dImg.save(dst)


def pil_image_similarity(filepath1, filepath2):
    from PIL import Image
    import math
    import operator
    from functools import reduce

    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)

#    image1 = get_thumbnail(img1)
#    image2 = get_thumbnail(img2)

    h1 = image1.histogram()
    h2 = image2.histogram()

    rms = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    return rms











# 计算图片相似度
def is_imgs_similar(img1, img2):
    import functools
    # 计算Hash
    def phash(img):
        img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
        avg = functools.reduce(lambda x, y: x + y, img.getdata()) / 64.
        return functools.reduce(
            lambda x, y: x | (y[1] << y[0]),
            enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())),
            0
        )
    # 计算汉明距离
    def hamming_distance(a, b):
        return bin(a ^ b).count('1')
    xsim=hamming_distance(phash(img1), phash(img2))
    print('xsim',xsim)
    return True if xsim <= 5 else False



def detect_and_crop_polygon_image(image):
    # 导入库
    import cv2
    # 读取图片
    img = cv2.imread(image)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 检测多边形边框线
    edges = cv2.Canny(gray, 50, 150, apertureSize = 3)
    # 检测多边形
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    # print(lines)

    # 遍历每一个框图
    for line in lines:
        print(line)
        x1, y1, x2, y2 = line[0]
        # 根据框图的坐标，裁剪图片
        crop_img = img[y1:y2, x1:x2]
        # 保存到文件夹
        # cv2.imshow('image',crop_img)

def detect_polygon_and_save(img):
    # 将图片转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 使用Canny算法检测边缘
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # 寻找多边形轮廓
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 遍历轮廓
    for cnt in contours:
        # 检测多边形边框
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
        # 如果是4边形
        if len(approx) == 4:
            # 获取多边形边框的4个坐标点
            x, y, w, h = cv2.boundingRect(cnt)
            # 沿着框线裁剪每一个框图
            new_img = img[y:y + h, x:x + w]
            # 保存到文件夹中
            cv2.imwrite('new_img.jpg', new_img)


def save_image_from_clipboard(dst):
    import win32clipboard
    import io
    
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
    win32clipboard.CloseClipboard()
    # bmp_head=b'BM60*\x00\x00\x00\x00\x006\x00\x00\x00'
    bmp_head=b'BM\x00\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00'
    # bmp_head=b'\x42\x4d\x36\x00\x00\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00'

    img = Image.open(io.BytesIO(bmp_head+data))
    img.save(dst)



def copy_image_to_clipboard(img_path: str):
    '''输入文件名，执行后，将图片复制到剪切板'''
    import io
    import win32clipboard
    image = Image.open(img_path)
    output = io.BytesIO()
    image.save(output, 'BMP')
    data = output.getvalue()[14:]
    print(output.getvalue()[:14])
    print(hex(len(data)+14))
    
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def scale_resize_image(img_path, size, dst):
    """
    输入图像路径和目标尺寸，将图像保持比例缩放到目标尺寸刚好能容纳的大小，多余部分透明化，保存图像。
    :param img_path: 图像路径
    :param size: 目标尺寸
    """
    from PIL import Image
    image = Image.open(img_path)
    # 缩放图像到目标尺寸
    image.thumbnail(size)
    # 获取缩放后的图像尺寸
    width, height = image.size
    # 创建一个目标尺寸的图像，并用白色填充
    target_img = Image.new('RGBA', size, (255, 255, 255, 0))
    # 将缩放后的图像放入到目标图像的中间
    target_img.paste(image, (int((size[0] - width) / 2), int((size[1] - height) / 2)))
    # 保存图像
    target_img.save(dst)












# **************************
# 视频相关
# **************************

# def record_video():

def record_video_camera(video_name):
    import cv2
    import keyboard

    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_name, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    while True:
        ret, frame = cap.read()
        out.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if keyboard.is_pressed('F2'):
            break
    out.release()
    cap.release()
    cv2.destroyAllWindows()



#批量截取MP4两个时间之间的图片，-r 1 按一秒一截取，-r 24一秒24帧
def CutVideoToImg(startstr,endstr,file,output_dir):
    def func(flag1, flag2):
        cmd = f'ffmpeg -ss {str(flag1)}:{str(flag2)}: -i "{file}" -f image2 -r 2 -t 00:01 "{output_dir}/{str(flag1)}：{str(flag2)}%3d.jpg"'
        os.system(cmd)
        print(flag1, flag2)
    start1 = int(startstr.split(":")[0])
    start2 = int(startstr.split(":")[1])
    end1 = int(endstr.split(":")[0])
    end2 = int(endstr.split(":")[1])
    print(start1, start2, end1, end2)
    flag1 = 0
    flag2 = 0
    while start1 <= end1:
        if start1 == end1:
            if start2 == end2:
                exit()
            else:
                while start2 < end2:
                    func(start1, start2)
                    start2 += 1
        else:
            if start2 == 60:
                start2 = 0
                start1 += 1
                func(start1, start2)
            else:
                while start2 < 60:
                    func(start1, start2)
                    start2 += 1


def SplitSoundFromVideo(inVideoFile):
    os.system("ffmpeg -i \"" + inVideoFile + "\" -f mp3 " + inVideoFile + ".mp3")


def Mp3ToSteam(inmp3):
    from pydub import AudioSegment
    song = AudioSegment.from_mp3(inmp3)
    return song

def Mp3SaveToFile(out,outfile):
    out.export(outfile, format="mp3")



#批量截取MP4两个时间之间的图片，-r 1 按一秒一截取，-r 24一秒24帧
def CutVideoToImg(startstr,endstr,file):
    def func(flag1, flag2):
        os.system("ffmpeg -ss " + str(flag1) + ':' + str(
            flag2) + " -i \"" + file + "\" -f image2 -r 2 -t 00:01 G:/PythonIO/moveImg/" + str(flag1) + '：' + str(
            flag2) + "%3d.jpg")
        print(flag1, flag2)
    start1 = int(startstr.split(":")[0])
    start2 = int(startstr.split(":")[1])
    end1 = int(endstr.split(":")[0])
    end2 = int(endstr.split(":")[1])
    print(start1, start2, end1, end2)
    flag1 = 0
    flag2 = 0
    while start1 <= end1:
        if start1 == end1:
            if start2 == end2:
                exit()
            else:
                while start2 < end2:
                    func(start1, start2)
                    start2 += 1
        else:
            if start2 == 60:
                start2 = 0
                start1 += 1
                func(start1, start2)
            else:
                while start2 < 60:
                    func(start1, start2)
                    start2 += 1


def SplitSoundFromVideo(inVideoFile):
    os.system("ffmpeg -i \"" + inVideoFile + "\" -f mp3 " + inVideoFile + ".mp3")

