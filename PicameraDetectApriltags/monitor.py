import picamera
import subprocess 
import os
import time, threading
import json
import ast
import numpy as np

path_name = os.path.dirname(os.path.abspath(__file__))

class Monitor_t(object):
	camera = picamera.PiCamera()
	isStart = False
	config = ""		# user specified coordinations of marks loaded from config.json
	mark = {}		# pixel coordinations of marks
	obj = {}		# pixel coordinations of objects

	def take_shot(self):
		image_name = 'image.jpg'
		command = path_name+"/apriltags_demo -d "+path_name+"/"+image_name

		self.camera.capture(image_name)
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = process.communicate()
		errcode = process.returncode
		return out
		
	def processing_image(self, raw_data):
		if raw_data.split('\n')[1].split(' ')[0] != '0':
			for line in raw_data.split('\n')[2:-1]:
				tid = line.split(' ')[3]
				x = line.split(' ')[6].split('(')[1]
				y = line.split(' ')[7]
				#print tid, x, y
				if tid in self.config.keys():
					self.mark[tid] = (float(x), float(y))
				else:
					self.obj[tid] = (float(x), float(y))
				
		else:
			print 'nothing detected'

	def getPids(self):
		if len( self.mark ) < 3:
			print "Not enough mark detected"
			return ''
		else:
			pids = []
			for tid, o in self.config.iteritems():
				pids.append(tid)
			return pids

	def calculating_coordinations(self):
		# initialization phase
		# in user specified coordinations of marks
		pids = self.getPids()
		if pids=='' :
			return
		m0 = self.config[pids[0]]
		m1 = self.config[pids[1]]
		m2 = self.config[pids[2]]
		w1 = np.subtract(m1,m0).tolist()
		w2 = np.subtract(m2,m0).tolist()
		# in pixel coordination
		# print self.mark["0"]
		t0 = self.mark[pids[0]] # choose origin point
		t1 = self.mark[pids[1]] # choose origin point
		t2 = self.mark[pids[2]] # choose origin point
		v1 = np.subtract(t1, t0).tolist()
		v2 = np.subtract(t2, t0).tolist()
		# print v1, v2
		A = np.asmatrix([[v1[0], v1[1]], [v2[0], v2[1]]]).T
		# print A
		# calculation phase
		ret = {}
		for tid, o in self.obj.iteritems():
			b = np.subtract(np.asarray(o), t0).T
			r = np.linalg.solve(A,b)
			# print b
			# print r
			# print w1, w2
			y = r[0]*np.asarray(w1) + r[1]*np.asarray(w2)
			y[0] = y[0]+m0[0]
			y[1] = y[1]+m0[1]
			
			ret[tid] = y
		return ret
				


	def daemon_thread_function(self):
		while(self.isStart):
			self.processing_image( self.take_shot() )
			print self.calculating_coordinations()
			time.sleep(1)
		
	def start(self):
		self.isStart=True
		self.daemon_t = threading.Thread(target = self.daemon_thread_function, args = (), name = 'daemon')
		self.daemon_t.start()

	def stop(self):
		self.isStart=False
		self.daemon_t.join()
		
	def __init__(self):
		with open('config.json', 'r') as f:
			self.config = ast.literal_eval( json.load(f) )
			
		for key, value in self.config.iteritems():
			self.config[key] = ast.literal_eval(value)	# parse value from string type to tuple type
			# print key, self.config[key]

if __name__ == '__main__':
	monitor = Monitor_t()
	monitor.start()
	time.sleep(60)
	monitor.stop()
