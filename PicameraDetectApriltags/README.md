# Detecting objects in the photo using AprilTags 

## Sources
  [April Tags C++ Library](http://people.csail.mit.edu/kaess/apriltags/)
  [Picamera Python library](https://www.raspberrypi.org/documentation/usage/camera/python/README.md)

## Dependencies
libopencv-dev

## Environment setup

1. Picamera is located on the ceiling or the wall, which can take shots of the marks and AGVs
2. There are several “marks” which is deployed by the user. The location of the mark is predefined by the user
3. All objects to be located also have AprilTags on it

## Workflow

1. Picamera takes a picture. Each picture must contain at least three marks to successfully detects the location of an object. 
2. April tag detector detects April tags in the picture
3. Transform the pixel coordination of objects into user-defined coordination by linear algebra calculation (change of basis)

## Usage

  ```shell
  python monitor.py
  ```
