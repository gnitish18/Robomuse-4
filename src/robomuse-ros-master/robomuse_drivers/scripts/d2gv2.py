#!/usr/bin/env python
import roslib
roslib.load_manifest('robomuse_drivers')
import sys 
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
i  = 0
avg1 = np.ones((480,640))
avg2 = np.ones((480,640))

class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("grayscaledepth_raw",Image, queue_size=10)
    self.mask_pub = rospy.Publisher("nearmask",Image, queue_size=10)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/depth_registered/image",Image,self.callback)
    self.img_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback1)
    self.desired_shape = (640,480)
    self.thresh = 240
    self.var = 0
    self.kernel = np.ones((5,5),np.uint8)
    self.cv_image = np.zeros((480,640,3))


  def deflicker(self):
    global i
    global avg1
    global avg2
    if i==10:
        avg1 = self.depthimg
        i = 0
    cv2.accumulateWeighted(self.depthimg,avg1,0.3)

    return avg1

  def callback1(self,data):
    global i
    i =1
    try:
      self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)



    #cv2.imshow("Image window", self.cv_image)
    cv2.waitKey(3)

  

  def callback(self,msg_depth): 
    try:
      global i
      global avg1 
      global avg2
      cv_image = self.bridge.imgmsg_to_cv2(msg_depth, "32FC1")    
      cv_image_array = np.array(cv_image, dtype = np.dtype('f8'))
      cv_image_norm = cv2.normalize(cv_image_array, cv_image_array, 0, 1, cv2.NORM_MINMAX)
      cv_image_resized = cv2.resize(cv_image_norm, self.desired_shape, interpolation = cv2.INTER_CUBIC)
      self.depthimg = cv_image_resized
      self.depthimg = cv2.GaussianBlur(self.depthimg,(5,5),0)
      self.depthimg = self.deflicker()
      self.depthimg = 256*self.depthimg
      self.depthimg = np.uint8(self.depthimg)
      self.depthimg = cv2.bitwise_not(self.depthimg)
      _,mask255 = cv2.threshold(self.depthimg,254,255,cv2.THRESH_BINARY)
      mask255= cv2.bitwise_not(mask255)
      cv2.bitwise_and(self.depthimg,mask255,self.depthimg)
      cv2.bitwise_and(self.depthimg,mask255)
      self.thresh=np.max(self.depthimg)
      maximg = self.thresh*np.ones(np.shape(self.depthimg))
      self.var = np.mean(maximg - self.depthimg)
      self.thresh = self.thresh - self.var/5
      _,mask = cv2.threshold(self.depthimg,self.thresh,255,cv2.THRESH_BINARY)
      mask = cv2.dilate(mask,self.kernel,iterations = 5)
      mask = cv2.erode(mask,self.kernel,iterations = 3)
      #cv2.imshow('hello',self.depthimg)
      #cv2.imshow('mask',mask)
      i = i +1
      cv2.waitKey(1)
    except CvBridgeError as e:
      print(e)
    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.depthimg, "mono8"))
      self.mask_pub.publish(self.bridge.cv2_to_imgmsg(mask, "mono8"))
    except CvBridgeError as e:
      print(e)


def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  cv2.imshow("Image window", ic.cv_image)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"

if __name__ == '__main__':
    main(sys.argv)
