#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from agv.srv import *

import time

class motorClient(object):
	def __init__(self):
		self.motorService = rospy.ServiceProxy('motor', Motor)

	def command(self, action):
		rospy.wait_for_service('motorService')
		try:
			self.motorService = rospy.ServiceProxy('motorService', Motor)
			res = self.motorService(action)
			print 'ack: '+res.ack
		except rospy.ServiceException , e:
			print "Service call failed: %s"%e
			
	def forward(self):
		self.command('forward')

	def backward(self):
		self.command('backward')

	def left(self):
		self.command('left')

	def right(self):
		self.command('right')

	def stop(self):
		self.command('stop')

if __name__ == '__main__':
	mClient = motorClient()



	mClient.forward()
	mClient.backward()
	mClient.left()
	mClient.right()
	mClient.stop()
