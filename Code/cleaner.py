import RPi.GPIO as GPIO  
import time

motor1=19
motor2=26
trig=16
echo=20

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor1, GPIO.OUT) # 모터 1번 지정
GPIO.setup(motor2, GPIO.OUT) # 모터 2번 지정
GPIO.setup(trig,GPIO.OUT) # 초음파 전송 트리거 신호 핀 출력으로 지정
GPIO.setup(echo,GPIO.IN) # 반사되는 초음파 수신하는 핀 입력으로 지정

p1 = GPIO.PWM(motor1, 50)
p1.start(0)
p2 = GPIO.PWM(motor2, 50)
p2.start(0)


while True:
    try:
        GPIO.output(trig,False) 
        time.sleep(0.5)
        GPIO.output(trig,True) # 초음파 송신 트리거 발생
        time.sleep(0.00001) # 트리거 펄스 중단
        GPIO.output(trig,False)
        
        while GPIO.input(echo) == 0:  
            start = time.time() # echo에 초음파가 인식이 안될때 시간출력
        while GPIO.input(echo) == 1:
            end = time.time() # echo에 초음파가 인식이 될때 시간출력

        duration = end-start # 초음파 수신시간에서 전송시간을 빼서 총 도달시간 산정
        distance = duration*17000  # 음파의 초당 이동속도(340m)를 이용하여 거리계
        distance = round(distance,2)
        print('distance :', distance)
        if distance <= 5: # 초음파 센서와 거리가 5cm 이하일때
            p1.ChangeDutyCycle(2.5)
            p2.ChangeDutyCycle(2.5) # p1과 p2모터를 돌려줌으로써 세정제 자동 분출
            time.sleep(1)
            p1.ChangeDutyCycle(7.5)
            p2.ChangeDutyCycle(7.5) # 1초 뒤 p1과 p2모터를 원상태로 돌려줌
            
    except:
        GPIO.cleanup() 

GPIO.cleanup()
        
