#!/usr/bin/python  
# coding=utf-8  
#本段代码实现树莓派智能小车的红外避障效果
#代码使用的树莓派GPIO是用的BOARD编码方式。 
import RPi.GPIO as GPIO
import sys
import socket
import socket
import time

time.sleep(20)
HOST = '192.168.137.1'
PORT = 8002
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORT))

print("try to connect distance server")
sock.send(b'request')
re_mes=sock.recv(1024).decode()
print(re_mes)



T_SensorRight = 17
T_SensorRight2 = 16
T_SensorLeft  = 18
T_SensorLeft2  = 19

PWMA   = 24
AIN1   = 21
AIN2   = 27

PWMB   = 22
BIN1   = 12
BIN2   = 4

def t_up(leftspeed, rightspeed,t_time):
        L_Motor.ChangeDutyCycle(leftspeed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(rightspeed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)
        
def t_stop(t_time):
        L_Motor.ChangeDutyCycle(0)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(0)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)
        
def t_down(leftspeed, rightspeed,t_time):
        L_Motor.ChangeDutyCycle(leftspeed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(rightspeed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

def t_left(leftspeed, rightspeed,t_time):
        L_Motor.ChangeDutyCycle(leftspeed)
        GPIO.output(AIN2,True)#AIN2
        GPIO.output(AIN1,False) #AIN1

        R_Motor.ChangeDutyCycle(rightspeed)
        GPIO.output(BIN2,False)#BIN2
        GPIO.output(BIN1,True) #BIN1
        time.sleep(t_time)

def t_right(leftspeed, rightspeed,t_time):
        L_Motor.ChangeDutyCycle(leftspeed)
        GPIO.output(AIN2,False)#AIN2
        GPIO.output(AIN1,True) #AIN1

        R_Motor.ChangeDutyCycle(rightspeed)
        GPIO.output(BIN2,True)#BIN2
        GPIO.output(BIN1,False) #BIN1
        time.sleep(t_time)

            
def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location

    GPIO.setup(T_SensorRight,GPIO.IN)
    GPIO.setup(T_SensorLeft,GPIO.IN)
    GPIO.setup(T_SensorRight2, GPIO.IN)
    GPIO.setup(T_SensorLeft2, GPIO.IN)
    GPIO.setup(AIN2,GPIO.OUT)
    GPIO.setup(AIN1,GPIO.OUT)
    GPIO.setup(PWMA,GPIO.OUT)

    GPIO.setup(BIN1,GPIO.OUT)
    GPIO.setup(BIN2,GPIO.OUT)
    GPIO.setup(PWMB,GPIO.OUT)
    
if __name__ == '__main__':
    setup()
    # keysacn()
    L_Motor= GPIO.PWM(PWMA,100)
    L_Motor.start(0)
    R_Motor = GPIO.PWM(PWMB,100)
    R_Motor.start(0)
    print('111')
    if re_mes == "welcome to server!":
        while 1:
            print("接收端：")

            sock.send(b"waiting")
            print("服务端：")
            re_mes = sock.recv(1024).decode()
            if re_mes == "close":
                break
            print(re_mes)
            print("")
            if re_mes =="start":
                try:
                    while True:
                        SR = GPIO.input(T_SensorRight)
                        SL = GPIO.input(T_SensorLeft)
                        BSR = GPIO.input(T_SensorRight2)
                        BSL = GPIO.input(T_SensorLeft2)
                        if SL == False and SR == False and BSL == False and BSR == False:
                            print("t_up")
                            t_up(25,25,0.01)

                        elif SL == True and SR ==False and BSL == False and BSR == False:
                            print("Left")
                            t_up(10,30,0.02)

                        elif SL==False and SR ==True and BSL == False and BSR == False:
                            print("Rhgit")
                            t_up(30,10,0.02)

                        elif SL==False and SR ==False and BSL ==  True and BSR == False:
                            print("BLeft")
                            t_left(30, 30, 0)

                        elif SL==False and SR ==False and BSL ==  False and BSR == True:
                            print("BRhgit")
                            t_right(30, 30, 0)
                        elif SL == True and SR == True and BSL == True and BSR == True:
                            print("end")
                            sock.send(b"end")
                            t_stop(0)
                            break
                        else:
                            t_stop(0)
                except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
                    t_stop(0)
                    GPIO.cleanup()
