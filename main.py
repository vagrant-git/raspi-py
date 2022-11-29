#! /usr/bin/env python
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import os
import cv2


### 初始化设置 ###
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

channel1 = 11  # 开关 channel
GPIO.setup(channel1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 按一次一个向上的冲激

ch_left = 13
ch_right = 15
channel2 = [ch_left, ch_right]

GPIO.setup(channel2, GPIO.OUT)

### 按键状态检测 ###

soundsdir = "/home/wordpi/Desktop/raspi-py/sounds/"


def startup():
    '''wait_for_edge 60s'''
    # start = GPIO.wait_for_edge(11, GPIO.RISING, timeout=60000)  # timeout=60s
    start = 1
    if start is None:
        print('Timeout')
    else:
        os.system("mplayer " + soundsdir + "welcome.mp3")
        print('open successfully, start to recognize')


### 识别结束，按下按键手动关闭 ###
def cleanup():
    ''' 手动结束程序 '''
    shut = 0
    close = GPIO.wait_for_edge(channel1, GPIO.RISING)  # timeout=5000 (ms)

    if close is not None:
        os.system("mplayer " + soundsdir + "stop.mp3")

        print('shutted down')
        shut = 1
    return shut


def capture_5s():
    '''拍摄5秒 每秒2张 '''
    with PiCamera() as camera:
        i = 1
        while True:
            camera.capture("./jpgs/jpg"+str(i)+".jpg")
            sleep(0.5)
            i = i+1
            if i > 10:  # get shutdown message
                print("capture ended")
                camera.close()
                break


def capture_one():
    ''' capture one picture'''
    camera = PiCamera()
    camera.resolution = (1024, 768)
    # camera.start_preview()
    # Camera warm-up time
    sleep(1)
    camera.capture('a.jpg')
    camera.close()


def viberation_ts(t=3, channel=channel2):
    '''channel high default = 3s ,channel2 '''
    GPIO.output(channel, GPIO.HIGH)
    sleep(t)


def traffic_light():
    '''红绿灯识别'''
    if green == 1:
        return 1
    elif red == 1:
        return 2
    else:
        return 0


if __name__ == '__main__':
    while True:
        startup()
        from zebra_crossing import iscrossing
        while True:
            #
            # capture_5s()
            capture_one()
            print("next recognition!!!")
            '''
            # 红绿灯交互
            if traffic_light == 1:  # 绿灯
                os.system("mplayer " + soundsdir+ "green.mp3")
                viberation_ts(t=0.5)  # TODO 绿灯提醒
            elif traffic_light == 2:  # 红灯
                os.system("mplayer " + soundsdir+ "red.mp3")
                viberation_ts()  # 两侧同时震动3s
            elif traffic_light == 0:  # 没识别到
                os.system("mplayer " + soundsdir+ "nonlight.mp3")
            '''
            # 斑马线交互
            img = cv2.imread("./a.jpg")
            i = iscrossing(img)
            print(i)
            if(i == 0):
                os.system("mplayer " + soundsdir + "nozebra.mp3")
                print('未识别到斑马线，请移动位置重新识别')
            elif (i == 1):
                os.system("mplayer " + soundsdir + "rightmove.mp3")
                viberation_ts(1, ch_right)
                print('接近斑马线左侧边缘，请靠右移动少许')
            elif (i == 2):
                os.system("mplayer " + soundsdir + "leftmove.mp3")
                viberation_ts(1, ch_left)
                print('接近斑马线右侧边缘，请靠左移动少许')
            elif (i == 3):
                os.system("mplayer " + soundsdir + "leftrot.mp3")
                viberation_ts(1, ch_left)
                print('斑马线在您左侧，请向左旋转少许')
            elif (i == 4):
                os.system("mplayer " + soundsdir + "rightrot.mp3")
                viberation_ts(1, ch_right)
                print('斑马线在您右侧，请靠右旋转少许')
            elif(i == 5):
                os.system("mplayer " + soundsdir + "goodzebra.mp3")
                print('斑马线在您正前方，请放心通行')

            '''
            if cleanup() == 1:
                GPIO.cleanup()
                break
            '''
