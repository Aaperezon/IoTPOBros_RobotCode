import requests
from gpiozero import RGBLED
from gpiozero import OutputDevice
import time
from AngleMeterAlpha import AngleMeterAlpha
from os import remove
from os import path
import json
import motorController
import PID
#CLASS VARIABLES
angleMeter = AngleMeterAlpha()
angleMeter.measure()
led = RGBLED(17,27,22)
statusLED = RGBLED(10,9,11)
#HOST TO CONNECT
ipHost = '192.168.1.103'
#JSON CONFIGURATION FOR PID
p = './Scripts/PID_Configuration.json'
#GLOBAL VARIABLES
id = 0
timeValue = 0
switchValue = 0
gyroX = 0.0
gyroY = 0.0
gyroZ = 0.0
anyChange = False

def Upload(url):
        try:
                r = requests.get(url,timeout=0.2)
        except OSError as e:
                print ('Connection error Upload '+url)
                pass

if path.exists(p):
	with open(p) as pid_config:
		pid_config = json.load(pid_config)
	P_Data = float(pid_config['P_Data'])
	I_Data = float(pid_config['I_Data'])
	D_Data = float(pid_config['D_Data'])
	Upload('http://'+ipHost+'/IoTPOBros_Interface/services/CreateRPI_Client.php/?gyroX='+str(gyroX)+'&gyroY='+str(gyroY)+'&gyroZ='+str(gyroZ)+'&P_Data='+str(P_Data)+'&I_Data='+str(I_Data)+'&D_Data='+str(I_Data))
else:
	P_Data = 0.0
	I_Data = 0.0
	D_Data = 0.0

pid = PID.PID(P_Data,I_Data,D_Data)
pid.SetPoint = 0.0


def Download():
	global anyChange,id,timeValue,switchValue,P_Data,I_Data,D_Data
	try:
		r = requests.get(url = 'http://'+ipHost+'/IoTPOBros_Interface/services/ReadClient_RPI.php',timeout=0.2)
		r = r.json()
		id_wildcard = r[0][0]
		timeValue_wildcard = r[0][1]
		switchValue_wildcard = r[0][2]
		P_Data_wildcard = r[0][3]
		I_Data_wildcard = r[0][4]
		D_Data_wildcard = r[0][5]

		P_Data_wildcard = float(P_Data_wildcard)
		I_Data_wildcard = float(I_Data_wildcard)
		D_Data_wildcard = float(D_Data_wildcard)

		if(switchValue_wildcard != switchValue or P_Data_wildcard != P_Data or I_Data_wildcard != I_Data or D_Data_wildcard != D_Data):
			id = id_wildcard
			timeValue = timeValue_wildcard
			switchValue = switchValue_wildcard
			P_Data = float(P_Data_wildcard)
			I_Data = float(I_Data_wildcard)
			D_Data = float(D_Data_wildcard)
			SavePID()
			anyChange = True
		statusLED.color = (0,1,0)
	except OSError  as e:
		print ('Connection error Download')
		GetPID()
		statusLED.color = (1,0,0)
		pass


def MPU6050():
	global anyChange, gyroX,gyroY,gyroZ
	gyroX_wildcard = angleMeter.get_kalman_pitch()
	gyroY_wildcard = 0
	gyroZ_wildcard = angleMeter.get_kalman_roll()
	if(gyroX_wildcard != gyroX or gyroY_wildcard != gyroY or gyroZ_wildcard != gyroZ):
		gyroX = gyroX_wildcard
		gyroY = gyroY_wildcard
		gyroZ = gyroZ_wildcard
		anyChange = True
        #print(angleMeter.get_kalman_roll(),",", angleMeter.get_complementary_roll(), ",",angleMeter.get_kalman_pitch(),",", angleMeter.get_complementary_pitch(),".")
        #print(angleMeter.get_int_roll(), angleMeter.get_int_pitch())

def GetPID():
	with open(p) as pid_config:
		pid_config = json.load(pid_config)
	P_Data = float(pid_config['P_Data'])
	I_Data = float(pid_config['I_Data'])
	D_Data = float(pid_config['D_Data'])
	print("PID obtenido de archivo local")
	PrintValues()


def SavePID():
	if path.exists(p):
		remove(p)
	data = {
		"P_Data" : P_Data,
		"I_Data" : I_Data,
		"D_Data" : D_Data
	}

	with open(p, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4)
	f.close()
	if path.exists(p):
		print ('Actualizado...')

def PrintValues():
	print ('timeValue:'+str(timeValue)+'gyroX= '+str(gyroX)+' gyroY= '+str(gyroY)+' gyroZ= '+str(gyroZ)+' switch= '+str(switchValue)+' P_Data= '+str(P_Data)+' I_Data= '+str(I_Data)+' D_Data= '+str(D_Data))
while True:
	Download()
	MPU6050()
	pid.update(-gyroX)
	sOut = pid.output
	motorController.LeftWheelSpeed(sOut)
	motorController.RightWheelSpeed(sOut)
	print (sOut)
	if(switchValue == '1'):
		led.color = (1,1,1)
	else:
		led.color = (0,0,0)


	if(anyChange == True):
		PrintValues()
		url = 'http://'+ipHost+'/IoTPOBros_Interface/services/CreateRPI_Client.php/?gyroX='+str(gyroX)+'&gyroY='+str(gyroY)+'&gyroZ='+str(gyroZ)+'&P_Data='+str(P_Data)+'&I_Data='+str(I_Data)+'&D_Data='+str(I_Data)
		Upload(url)
		pid.setKp(P_Data)
		pid.setKi(I_Data)
		pid.setKd(D_Data)
		anyChange = False
	time.sleep(.001)

