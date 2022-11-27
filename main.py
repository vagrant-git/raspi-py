#! /usr/bin/env python
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import os
from playsound import playsound

from zebra_crossing import iscrossing

### 初始化设置 ###
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
channel1 = []  # 开关 channel
GPIO.setup(channel1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 按一次一个向上的冲激

ch_left = [], ch_right = []
channel2 = [ch_left, ch_right]
GPIO.setup(channel2, GPIO.OUT)

# GPIO.setup(channel3, GPIO.OUT)

### 按键状态检测 ###


def startup():
    '''wait_for_edge 60s'''
    channel1 = GPIO.wait_for_edge(
        channel1, GPIO.RISING, timeout=60000)  # timeout=60s
    if channel1 is None:
        print('Timeout')
    else:
        playsound("./sounds/welcome.wav")
        print('open successfully, start to recognize')


### 识别结束，按下按键手动关闭 ###
def cleanup():
    ''' 手动结束程序 '''
    shut = 0
    channel1 = GPIO.wait_for_edge(channel1, GPIO.RISING)  # timeout=5000 (ms)

    if channel1 is not None:
        playsound("./sounds/stop.wav")
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
    # camera.resolution = (1024, 768)
    # camera.start_preview()
    # Camera warm-up time
    sleep(1)
    camera.capture('a.jpg')


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
        while True:
            #
            # capture_5s()
            capture_one()

            # 红绿灯交互
            if traffic_light == 1:  # 绿灯
                playsound("./sounds/green.wav")
                viberation_ts(t=0.5)  # TODO 绿灯提醒
            elif traffic_light == 2:  # 红灯
                playsound("./sounds/red.wav")
                viberation_ts()  # 两侧同时震动3s
            elif traffic_light == 0:  # 没识别到
                playsound("./sounds/nonlight.wav")

            # 斑马线交互
            i = iscrossing("./a.jpg")
            if(i == 0):
                playsound("./sounds/nozebra.wav")
                print('未识别到斑马线，请移动位置重新识别')
            elif (i == 1):
                playsound("./sounds/rightmove.wav")
                viberation_ts(1, ch_right)
                print('接近斑马线左侧边缘，请靠右移动少许')
            elif (i == 2):
                playsound("./sounds/leftmove.wav")
                viberation_ts(1, ch_left)
                print('接近斑马线右侧边缘，请靠左移动少许')
            elif (i == 3):
                playsound("./sounds/leftrot.wav")
                viberation_ts(1, ch_left)
                print('斑马线在您左侧，请向左旋转少许')
            elif (i == 4):
                playsound("./sounds/rightrot.wav")
                viberation_ts(1, ch_right)
                print('斑马线在您右侧，请靠右旋转少许')
            elif(i == 5):
                playsound("./sounds/goodzebra.wav")
                print('斑马线在您正前方，请放心通行')

            if cleanup() == 1:
                GPIO.cleanup()
                break
