#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
import maskanddetect
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from geometry_msgs.msg import Twist
import numpy as np


left = Twist()

left.linear.x = 0
left.linear.y = 0
left.linear.z = 0

left.angular.x = 0
left.angular.y = 0
left.angular.z = -0.1

right = Twist()

right.linear.x = 0
right.linear.y = 0
right.linear.z = 0

right.angular.x = 0
right.angular.y = 0
right.angular.z = 0.1

stop = Twist()

stop.linear.x = 0
stop.linear.y = 0
stop.linear.z = 0

stop.angular.x = 0
stop.angular.y = 0
stop.angular.z = 0

straight = Twist()

straight.linear.x = 0.1
straight.linear.y = 0
straight.linear.z = 0

straight.angular.x = 0
straight.angular.y = 0
straight.angular.z = 0

pub = rospy.Publisher('/robomuse/cmd_vel', Twist, queue_size=10)


class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    cx,cy = maskanddetect.detect(cv_image)
    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)
    if(cx == 0 and cy == 0):
        pub.publish(stop)
    elif (cx>320):
        pub.publish(left)
    elif (cx<300):
        pub.publish(right)
    elif(cx>300 and cx<320):
        pub.publish(straight)



def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
