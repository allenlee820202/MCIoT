#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

import rospy
from std_msgs.msg import String

DR = 16
DL = 19

def DRcallback(self):
	DR_status = GPIO.input(DR)
	DL_status = GPIO.input(DL)
	rospy.loginfo(DR_status)+" "+str(DL_status) 
	self.pub.publish( str(DR_status)+" "+str(DL_status) )

def DLcallback(self):
	DR_status = GPIO.input(DR)
	DL_status = GPIO.input(DL)
	rospy.loginfo(DR_status)+" "+str(DL_status) 
	self.pub.publish( str(DR_status)+" "+str(DL_status) )

class frontIR(object):
	def __init__(self, dr=16, dl=19):
		self.DR = dr
		self.DL = dl
				
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.DR, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.DL, GPIO.IN, GPIO.PUD_UP)
		
		self.pub = rospy.Publisher('frontIR', String, queue_size=10)
		rospy.init_node('frontIR', anonymous=True)


	def setCallback(self):
		GPIO.add_event_detect(self.DR, GPIO.BOTH, callback = DRcallback)
		GPIO.add_event_detect(self.DL, GPIO.BOTH, callback = DLcallback)

if __name__ == '__main__':
	frontIR()
	while(1):
		time.sleep(10)
