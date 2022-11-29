import cv2
import numpy as np
import os
kernel_Ero = np.ones((3, 1), np.uint8)
kernel_Dia = np.ones((5, 1), np.uint8)
'''
file_src="../../../pythonProject/image_processing/images"
img_name="banmaxian07.jpeg"
img_src=os.path.join(file_src,img_name)
img = cv2.imread(img_src)
# copy_img = img.copy()
'''
img = cv2.imread("./a.jpg")


def iscrossing(img):

    i = 0
    # 图像调整分辨率
    img = np.array(img)
    copy_img = cv2.resize(img, (768, 1024))
    # gray = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
    # 图像灰度化
    gray = cv2.cvtColor(copy_img, cv2.COLOR_BGR2GRAY)
    # 高斯滤波
    imgblur = cv2.GaussianBlur(gray, (5, 5), 10)
    # 阈值处理
    ret, thresh = cv2.threshold(imgblur, 200, 255, cv2.THRESH_BINARY)
    # 腐蚀
    img_Ero = cv2.erode(thresh, kernel_Ero, iterations=3)
    # 膨胀
    img_Dia = cv2.dilate(img_Ero, kernel_Dia, iterations=1)
    # cv2.imshow('img_Dia',img_Dia)
    # cv2.waitKey(0)
    # 轮廓检测
    contouts, h = cv2.findContours(
        img_Dia, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    rects = []
    point_xs = []
    point_ys = []
    widths = []
    heights = []
    angles = []
    for cnt in contouts:
        rect = cv2.minAreaRect(cnt)
        x, y = rect[0]
        w, h = rect[1]
        a = rect[2] if(w > h) else 90-rect[2]
        if ((w > 100 and (h > 10 and h < 80)) or ((w > 10 and w < 80) and h > 100) and y > 200):
            rects.append(rect)
            point_xs.append(x)
            point_ys.append(y)
            widths.append(w)
            heights.append(h)
            angles.append(a)

    # 去除角度相差很大的部分（斑马线平行性）
    angle_avg = np.average(angles)
    angles_copy = angles.copy()
    widths_copy = widths.copy()
    heights_copy = heights.copy()
    point_ys_copy = point_ys.copy()
    point_xs_copy = point_xs.copy()
    rects_copy = rects.copy()

    for angle in angles_copy:
        i = angles_copy.index(angle)
        # print(angle)
        if abs(angle-angle_avg) > 25:
            rects.remove(rects_copy[i])
            angles.remove(angle)
            widths.remove(widths_copy[i])
            heights.remove(heights_copy[i])
            point_xs.remove(point_xs_copy[i])
            point_ys.remove(point_ys_copy[i])

    widths_avg = np.average(widths)
    heights_avg = np.average(heights)
    angles_copy = angles.copy()
    widths_copy = widths.copy()
    heights_copy = heights.copy()
    point_ys_copy = point_ys.copy()
    point_xs_copy = point_xs.copy()
    rects_copy = rects.copy()
    # print(rects)
    for width in widths_copy:
        i = widths_copy.index(width)
        if abs((width-widths_avg)*(heights_copy[i]-heights_avg)) > 3600:
            rects.remove(rects_copy[i])
            angles.remove(angles_copy[i])
            widths.remove(widths_copy[i])
            heights.remove(heights_copy[i])
            point_xs.remove(point_xs_copy[i])
            point_ys.remove(point_ys_copy[i])

    i = len(angles)
    # print(angle_avg)
    width = np.average(widths)
    height = np.average(heights)
    angle_avg = np.average(angles)
    point_x = np.average(point_xs)
    point_y = np.average(point_ys)

    for rect in rects:
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        x, y = rect[0]
        w, h = rect[1]
        a = rect[2] if(w > h) else 90-rect[2]
        print('x=%d y=%d width=%d height=%d angle=%0.3f' % (x, y, w, h, a))
        outimg = cv2.drawContours(copy_img, [box], 0, (0, 0, 255), 2)

    # cv2.imshow('out',outimg)
    # cv2.waitKey(0)

    if(i < 3):
        return 0
    elif(point_x < 100):
        return 1
    elif(point_x > 500):
        return 2
    elif(width < height and angle_avg > 5):
        return 3
    elif(width > height and angle_avg > 5):
        return 4
    else:
        return 5


# print(iscrossing(img))
'''
i=iscrossing(copy_img)
if(i==0):
    print('这儿没有斑马线，请四周移动位置')
elif (i == 1):
    print('接近斑马线左侧边缘，请靠右移动少许')
elif (i == 2):
    print('接近斑马线右侧边缘，请靠左移动少许')
elif (i == 3):
    print('斑马线在您左侧，请靠左旋转少许')
elif (i == 4):
    print('斑马线在您右侧，请靠右旋转少许')
elif(i==5):
    print('这儿有斑马线，请等待通行')
    '''
