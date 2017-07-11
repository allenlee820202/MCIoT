import picamera
import subprocess 
import os

image_name = 'image.jpg'
path_name = os.path.dirname(os.path.abspath(__file__))

command = path_name+"/apriltags_demo -d "+path_name+"/"+image_name

camera = picamera.PiCamera()

camera.capture(image_name)
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

out, err = process.communicate()
errcode = process.returncode

print out

print err
