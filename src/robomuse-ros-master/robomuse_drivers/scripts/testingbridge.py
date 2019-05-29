#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
import detect
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

cv_image = cv2.imread("/home/subbu/Documents/Computer_Vision/RGB_image.png",1)
cx = 0
cy = 0

class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)

  def callback(self,data):
      global cv_image
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")

def main(args):

  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)

  while(1):

      global cv_image
      global cx
      global cy
      cx,cy = detect.detect(cv_image)
      try:
          print (cx,cy)
      except KeyboardInterrupt:
          print("Shutting down")
  try:
      rospy.spin()
  except KeyboardInterrupt:
      print("Shutting down")
      cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
