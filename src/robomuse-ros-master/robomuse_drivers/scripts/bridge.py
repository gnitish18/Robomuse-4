#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import numpy as np
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
i = 0

class image_converter:

  def __init__(self):
    self.bridge1 = CvBridge()
    self.bridge2 = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback1)
    self.cv_image = np.zeros((480,640,3))
    self.cv_maskcolor = np.zeros((480,640,3))
    self.one = 255*np.ones((480,640,3))

  def callback1(self,data):
    global i
    i =1
    try:
      self.cv_image = self.bridge1.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)



    cv2.imshow("Image window", self.cv_image)
    cv2.waitKey(3)




def main(args):
  global i
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    if i==1:
      print(ic.cv_image)
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main(sys.argv)