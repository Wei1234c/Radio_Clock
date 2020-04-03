# http://stanley2910.pixnet.net/blog/post/189515895-raspberry-pi-pwm-%E9%A0%BB%E7%8E%87

import RPi.GPIO as GPIO  # runs only on RPi
import time



def mark(message, delay_seconds = 2):
    print(message)
    time.sleep(delay_seconds)



# GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

CHANNEL = 4
FREQUENCY = 100
DUTY_CYCLE_PERCENTAGE = 50

GPIO.setup(CHANNEL, GPIO.OUT)

p = GPIO.PWM(CHANNEL, FREQUENCY)

mark('start')
p.start(DUTY_CYCLE_PERCENTAGE)

mark('ChangeDutyCycle(75)')
p.ChangeDutyCycle(10)

mark('ChangeFrequency(100)')
p.ChangeFrequency(1000)

mark('stop')
p.stop()

GPIO.cleanup()
