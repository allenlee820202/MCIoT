# Detecting objects in the photo using AprilTags 

## Sources
  [April Tags C++ Library](http://people.csail.mit.edu/kaess/apriltags/)
  [Picamera Python library](https://www.raspberrypi.org/documentation/usage/camera/python/README.md)

## Dependencies
libopencv-dev

## Workflow

1. Picamera takes a picture
2. April tag detector detects April tags in the picture
3. Output object ID and its location (represented using pixel position)
 

## Usage

  ```shell
  python monitor.py
  ```
