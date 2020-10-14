import RPi.GPIO as GPIO 

#CONTROLLER FOR LEFT WHEEL
in1 = 23
in2 = 24
ena = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p1=GPIO.PWM(ena,1000)

#CONTROLLER FOR RIGHT WHEEL
in3 = 8
in4 = 7
enb = 1
temp2=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2=GPIO.PWM(enb,1000)


p1.start(0)
p2.start(0)

def LeftWheelSpeed(s):
	if(s<0):
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.HIGH)
	elif(s>0):
		GPIO.output(in1,GPIO.HIGH)
		GPIO.output(in2,GPIO.LOW)
	s = abs(s)
	if(s>100):
		s=100
	elif(s<0):
		s=0
	p1.ChangeDutyCycle(s)
def RightWheelSpeed(s):
	if(s<0):
		GPIO.output(in3,GPIO.HIGH)
		GPIO.output(in4,GPIO.LOW)
	elif(s>0):
		GPIO.output(in3,GPIO.LOW)
		GPIO.output(in4,GPIO.HIGH)
	s = abs(s)
	if(s>100):
		s=100
	elif(s<0):
		s=0
	p2.ChangeDutyCycle(s)
