import RPi.GPIO as GPIO
import time

DR = 16
DL = 19

def DRcallback(self):
	DR_status = GPIO.input(DR)
	DL_status = GPIO.input(DL)
	print str(DR_status)+" "+str(DL_status) 
	
def DLcallback(self):
	DR_status = GPIO.input(DR)
	DL_status = GPIO.input(DL)
	print str(DR_status)+" "+str(DL_status) 

class frontIR(object):

	def setCallback(self):
		GPIO.add_event_detect(self.DR, GPIO.BOTH, callback = DRcallback )
		GPIO.add_event_detect(self.DL, GPIO.BOTH, callback = DLcallback )

	def __init__(self, dr=16, dl=19):
		self.DR = dr
		self.DL = dl
				
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.DR, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.DL, GPIO.IN, GPIO.PUD_UP)

		self.setCallback()

if __name__ == '__main__':
	fIR = frontIR()
	while(1):
		time.sleep(10)
