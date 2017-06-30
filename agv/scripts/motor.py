#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from agv.srv import *

import RPi.GPIO as GPIO
import time

class Motor_t(object):
	
	def __init__(self,in1=12,in2=13,ena=6,in3=20,in4=21,enb=26):
		self.IN1 = in1
		self.IN2 = in2
		self.IN3 = in3
		self.IN4 = in4
		self.ENA = ena
		self.ENB = enb

		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.IN1,GPIO.OUT)
		GPIO.setup(self.IN2,GPIO.OUT)
		GPIO.setup(self.IN3,GPIO.OUT)
		GPIO.setup(self.IN4,GPIO.OUT)
		GPIO.setup(self.ENA,GPIO.OUT)
		GPIO.setup(self.ENB,GPIO.OUT)
		self.forward()
		self.PWMA = GPIO.PWM(self.ENA,500)
		self.PWMB = GPIO.PWM(self.ENB,500)
		self.PWMA.start(50)
		self.PWMB.start(50)

	def forward(self):
		GPIO.output(self.IN1,GPIO.HIGH)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.HIGH)

	def stop(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.LOW)

	def backward(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.HIGH)
		GPIO.output(self.IN3,GPIO.HIGH)
		GPIO.output(self.IN4,GPIO.LOW)
	def left(self):
		GPIO.output(self.IN1,GPIO.LOW)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.HIGH)
	def right(self):
		GPIO.output(self.IN1,GPIO.HIGH)
		GPIO.output(self.IN2,GPIO.LOW)
		GPIO.output(self.IN3,GPIO.LOW)
		GPIO.output(self.IN4,GPIO.LOW)

	def setPWMA(self,value):
		self.PWMA.ChangeDutyCycle(value)
	def setPWMB(self,value):
		self.PWMB.ChangeDutyCycle(value)

	def setMotor(self, left, right):
		if((right >= 0) and (right <= 100)):
			GPIO.output(self.IN1,GPIO.HIGH)
			GPIO.output(self.IN2,GPIO.LOW)
			self.PWMA.ChangeDutyCycle(right)
		elif((right < 0) and (right >= -100)):
			GPIO.output(self.IN1,GPIO.LOW)
			GPIO.output(self.IN2,GPIO.HIGH)
			self.PWMA.ChangeDutyCycle(0 - right)
		if((left >= 0) and (left <= 100)):
			GPIO.output(self.IN3,GPIO.HIGH)
			GPIO.output(self.IN4,GPIO.LOW)
			self.PWMB.ChangeDutyCycle(left)
		elif((left < 0) and (left >= -100)):
			GPIO.output(self.IN3,GPIO.LOW)
			GPIO.output(self.IN4,GPIO.HIGH)
			self.PWMB.ChangeDutyCycle(0 - left)

Ab = Motor_t()
def motorControlCallback(req):
	if(req.action == 'forward'):
		Ab.forward()
		rospy.loginfo(rospy.get_caller_id() + ': forward')
		return MotorResponse('forward')
		#res.ack = 'forward'
		#return res
	elif(req.action == 'left'):
		Ab.left()
		rospy.loginfo(rospy.get_caller_id() + ': left')
		res = MotorResponse()
		res.ack = 'left'
		return res
	elif(req.action == 'right'):
		Ab.right()
		rospy.loginfo(rospy.get_caller_id() + ': right')
		res = MotorResponse()
		res.ack = 'right'
		return res
	elif(req.action == 'backward'):
		rospy.loginfo(rospy.get_caller_id() + ': backward')
		Ab.backward()
		time.sleep(0.2)
		Ab.left()
		time.sleep(0.2)
		Ab.stop()
		res = MotorResponse()
		res.ack = 'backward'
		return res
	elif(req.action == 'stop'):
		Ab.stop()
		rospy.loginfo(rospy.get_caller_id() + ': stop')
		res = MotorResponse()
		res.ack = 'stop'
		return res
	else:
		res = MotorResponse()
		res.ack = 'error: no such action: '+req.action
		return res
		

def motorController():	
	rospy.init_node('motorServer')
	rospy.Service( 'motorService', Motor, motorControlCallback )
	rospy.spin()

if __name__ == '__main__':
	motorController()

