import picamera
from subprocess import call

camera = picamera.PiCamera()

camera.capture('image.jpg')
call(["/home/pi/PicameraDetectApriltags/apriltags_demo", "/home/pi/PicameraDetectApriltags/image.jpg"])
