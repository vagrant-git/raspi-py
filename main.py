#! /usr/bin/env python
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import os

from playsound import playsound

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
        channel1, GPIO.RISING, timeout=60000)  # timeout=5000 (ms)
    playsound("welcome.wav")
    if channel1 is None:
        print('Timeout')
    else:
        print('open successfully, start to recognize')


### 识别结束，按下按键手动关闭 ###
def cleanup():
    ''' 手动结束程序 '''
    shut = 0
    channel1 = GPIO.wait_for_edge(channel1, GPIO.RISING)  # timeout=5000 (ms)

    if channel1 is not None:
        playsound("stop.wav")
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


def zebra_crossing():
    '''斑马线识别'''
    if left == 1:
        return 1
    elif right == 1:
        return 2
    else:
        return 0


if __name__ == '__main__':
    while True:
        startup()
        while True:
            capture_5s()
            # 红绿灯交互
            if traffic_light == 1:  # 绿灯
                playsound("green.wav")
                viberation_ts(t=0.5)  # TODO 绿灯提醒
            elif traffic_light == 2:  # 红灯
                playsound("red.wav")
                viberation_ts()  # 两侧同时震动3s
            elif traffic_light == 0:  # 没识别到
                playsound("nonlight.wav")

            # 斑马线交互
            if zebra_crossing == 1:
                playsound("left.wav")
                viberation_ts(1, ch_right)
            elif zebra_crossing == 2:
                playsound("right.wav")
                viberation_ts(1, ch_left)

            if cleanup() == 1:
                GPIO.cleanup()
                break