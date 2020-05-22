import RPi.GPIO as GPIO
import time

motor1=17
motor2=18

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor1, GPIO.OUT)
GPIO.setup(motor2, GPIO.OUT)

p1 = GPIO.PWM(motor1, 50)
p2 = GPIO.PWM(motor2, 50)

p1.start(0)
p2.start(0)

p1.ChangeDutyCycle(2.5)
p2.ChangeDutyCycle(2.5)

time.sleep(2)

p1.ChangeDutyCycle(7.5)
p2.ChangeDutyCycle(7.5)

GPIO.cleanup()
