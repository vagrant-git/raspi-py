#! /usr/bin/env python
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep

GPIO.setmode(GPIO.BOARD)
channel = []  # switch
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # 按一次一个向上的冲激


def startup():
    '''wait_for_edge 60s'''
    channel = GPIO.wait_for_edge(
        channel, GPIO_RISING, timeout=60000)  # timeout=5000 (ms)

    if channel is None:
        print('Timeout')
    else:
        print('open successfully, start to recognize')


def cleanup():
    ''' 手动结束程序 '''
    shut = 0
    channel = GPIO.wait_for_edge(channel, GPIO_RISING)  # timeout=5000 (ms)

    if channel is not None:
        print('shutted down')
        shut = 1
        return shut


def capture_one():
    ''' capture one picture'''
    camera = PiCamera()
    # camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    camera.capture('foo.jpg')


def capture_con():
    ''' capture per 5s'''
    camera = PiCamera()
    camera.start_preview()
    sleep(2)
    for filename in camera.capture_continuous('img{counter:03d}.jpg'):
        print('Captured %s' % filename)
        sleep(5)  # wait 5 seconds


if __name__ == '__main__':
    startup()
    while True:
        capture_one()
        # TODO recognition

        # traffic_light = deeplearning()
        # zebra_crossing = machine_learning()
        if detection_success == False:
            print('detect fail, please adjust the direction')
            sleep(2)
            continue

        if traffic_light == 1:
            print('gogogo')
            if zebra_crossing != = 1:  # 0 1 2
                print('go left / right')

        else:
            print('please wait')

        if cleanup() == 1:
            GPIO.cleanup()
            break
