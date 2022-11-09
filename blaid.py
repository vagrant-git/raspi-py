#! /usr/bin/env python
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
channel1 = []  # switch channel
GPIO.setup(channel1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 按一次一个向上的冲激

channel2 = []  # viberation channel
ch_left = [], ch_right = []
GPIO.setup(channel2, GPIO.OUT)


def startup():
    '''wait_for_edge 60s'''
    channel1 = GPIO.wait_for_edge(
        channel1, GPIO.RISING, timeout=60000)  # timeout=5000 (ms)

    if channel1 is None:
        print('Timeout')
    else:
        print('open successfully, start to recognize')


def cleanup():
    ''' 手动结束程序 '''
    shut = 0
    channel1 = GPIO.wait_for_edge(channel1, GPIO_RISING)  # timeout=5000 (ms)

    if channel1 is not None:
        print('shutted down')
        shut = 1
        return shut


def capture_one():
    ''' capture one picture'''
    camera = PiCamera()
    # camera.resolution = (1024, 768)
    # camera.start_preview()
    # Camera warm-up time
    sleep(1)
    camera.capture('p.jpg')


def capture_con():
    ''' capture per 5s'''
    camera = PiCamera()
    camera.start_preview()
    sleep(2)
    for filename in camera.capture_continuous('img{counter:03d}.jpg'):
        print('Captured %s' % filename)
        sleep(5)  # wait 5 seconds


def capture_continuous():
    with PiCamera() as camera:
        i = 1
        while True:
            sleep(1)
            camera.capture("./jpgs/jpg"+str(i)+".jpg")
            i = i+1
            if i > 5:  # get shutdown message
                print("capture ended")
                camera.close()
                break


def viberation_3s(t=3, channel=[channel2]):
    '''channel high default = 3s ,channel12 '''
    GPIO.output(channel, GPIO.HIGH)
    sleep(t)


if __name__ == '__main__':
    startup()
    while True:
        capture_one()
        # TODO recognition

        # traffic_light = deeplearning()
        # zebra_crossing = machine_learning()
        if detection_success == False:
            print('detect fail, please adjust the direction')
            viberation_3s()
            sleep(1)
            continue

        if traffic_light == 1:
            print('gogogo')
            if zebra_crossing != 1:  # 0 1 2
                viberation_3s(t=3, channel=ch_left)
                viberation_3s(t=3, channel=ch_right)
                print('go left / right')

        else:
            viberation_3s()
            print('please wait')

        if cleanup() == 1:
            GPIO.cleanup()
            break
