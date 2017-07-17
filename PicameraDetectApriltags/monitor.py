import picamera
import subprocess 
import os
import time, threading

path_name = os.path.dirname(os.path.abspath(__file__))

class Monitor_t(object):
	camera = picamera.PiCamera()
	isStart = False

	def take_shot(self):
		image_name = 'image.jpg'
		command = path_name+"/apriltags_demo -d "+path_name+"/"+image_name

		self.camera.capture(image_name)
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out, err = process.communicate()
		errcode = process.returncode
		return out
		
	def processing_data(self, raw_data):
		print raw_data
		for line in raw_data:
			return line

	def daemon_thread_function(self):
		while(self.isStart):
			print self.processing_data( self.take_shot() )
			time.sleep(1)
		
	def start(self):
		self.isStart=True
		self.daemon_t = threading.Thread(target = self.daemon_thread_function, args = (), name = 'daemon')
		self.daemon_t.start()

	def stop(self):
		self.isStart=False
		self.daemon_t.join()
		
	def __init__(self):
		self.start()
		time.sleep(10)
		self.stop()
	
if __name__ == '__main__':
	Monitor_t()
