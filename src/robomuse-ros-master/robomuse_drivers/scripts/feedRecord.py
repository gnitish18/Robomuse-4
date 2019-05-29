#!/usr/bin/env python
import roslib
from time import sleep
import sys
import cv2
import rospy
import os
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Int8

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/robomuse/rm4videos/vid1.avi',fourcc, 20.0, (640,480))

def callback(data):
  if(data.data):
    out.release()
    os.system("rosnode kill image_converter")

class image_converter:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_color",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
      #frame = cv2.flip(cv_image,0)

      # write the flipped frame
      out.write(cv_image)
    except CvBridgeError as e:
      print(e)

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(1)
      
    # os.system("rm /home/robomuse/input/recordedFeed.avi")
def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=False)
  rospy.Subscriber("startencryption", Int8, callback)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down yipppeee")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
