#!/usr/bin/env python

import rospy
from std_msgs.msg import String

import RPi.GPIO as GPIO
import time

DR = 16
DL = 19

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DR, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(DL, GPIO.IN, GPIO.PUD_UP)

pub = rospy.Publisher('frontIR', String, queue_size=10)
rospy.init_node('frontIR', anonymous=True)

def DRcallback(DR):	
	DR_status = GPIO.input(DR)
	DL_status = GPIO.input(DL)
	if not rospy.is_shutdown():	
		rospy.loginfo(str(DR_status)+" "+str(DL_status) )
		pub.publish( str(DR_status)+" "+str(DL_status) )

def DLcallback(DL):
	DR_status = GPIO.input(DR)
	DL_status = GPIO.input(DL)
	if not rospy.is_shutdown():	
		rospy.loginfo(str(DR_status)+" "+str(DL_status) )
		pub.publish( str(DR_status)+" "+str(DL_status) )


GPIO.add_event_detect(DR, GPIO.BOTH, callback = DRcallback)
GPIO.add_event_detect(DL, GPIO.BOTH, callback = DLcallback)

if __name__ == '__main__':
	while(1):
		time.sleep(10)
