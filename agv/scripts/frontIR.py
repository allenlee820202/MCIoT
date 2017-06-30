#!/usr/bin/env python

import rospy
from std_msgs.msg import String

import RPi.GPIO as GPIO
import time

class frontIR_t(object):
	def DRcallback(self, dr, dl, pub):	
		DR_status = GPIO.input(dr)
		DL_status = GPIO.input(dl)
		if not rospy.is_shutdown():	
			rospy.loginfo(str(DR_status)+" "+str(DL_status) )
			pub.publish( str(DR_status)+" "+str(DL_status) )
	
	def DLcallback(self, dr, dl, pub):
		DR_status = GPIO.input(dr)
		DL_status = GPIO.input(dl)
		if not rospy.is_shutdown():	
			rospy.loginfo(str(DR_status)+" "+str(DL_status) )
			pub.publish( str(DR_status)+" "+str(DL_status) )
	
	def setCallback(self, dr, dl, pub):
		GPIO.add_event_detect(self.DR, GPIO.BOTH, callback = lambda *a: self.DRcallback(dr, dl, pub))
		GPIO.add_event_detect(self.DL, GPIO.BOTH, callback = lambda *a: self.DLcallback(dr, dl, pub))

	def __init__(self, dr=16, dl=19):
		self.DR = dr
		self.DL = dl
				
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.DR, GPIO.IN, GPIO.PUD_UP)
		GPIO.setup(self.DL, GPIO.IN, GPIO.PUD_UP)

    		pub = rospy.Publisher('frontIR', String, queue_size=10)
    		rospy.init_node('frontIR', anonymous=True)

		self.setCallback(dr, dl, pub)


if __name__ == '__main__':
	frontIR_t()
	while(1):
		time.sleep(10)
