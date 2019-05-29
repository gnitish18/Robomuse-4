#!/usr/bin/env python
import math
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
    self.desired_shape = (640,480)
    self.thresh = 240
    self.var = 0
    self.kernel = np.ones((5,5),np.uint8)

  def func(self,x,a,b,c):
    return a*x*x + b*x + c


  def deflicker(self):
    global i
    global avg1
    global avg2
    if i==10:
        avg1 = self.depthimg
        i = 0
    cv2.accumulateWeighted(self.depthimg,avg1,0.3)

    return avg1

  def findcentroid(self):

    M = cv2.moments(self.mask)
    self.xcent = int(M["m10"]/M["m00"])
    self.ycent = int(M["m01"]/M["m00"])
    #_, contours, _ = cv2.findContours(self.mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #c = 255*np.ones(np.shape(self.depthimg))
    #try:
    #  c = max(contours, key = cv2.contourArea)
    #except:
    #  pass
    #if cv2.contourArea(c) > 150:
    #  (xcirc , ycirc) , radius = cv2.minEnclosingCircle(c)
    #  center = (int(xcirc) , int(ycirc))
    #  radius = int(radius)
    #  print np.shape(contours)
    #  self.xcent = int(xcirc)
    #  self.ycent = int(ycirc)
    #else:
    #  self.xcent = 0
    #  self.ycent = 0

    return self.xcent,self.ycent

  def findang(self):
    x = abs(self.xcent - 320)
    sign = -(self.xcent - 320)/x
    self.angle = sign*math.atan(x*0.00169)
    return self.angle

  def finddist(self):
    self.maxx,self.maxy = np.unravel_index(self.orgimg.argmax(),self.depthimg.shape)
    p = self.orgimg[self.maxx,self.maxy]
    print p
    self.r = self.func(p, 0.000164,-0.0836,11.264)
    return self.r
    return 0

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
      self.orgimg = np.uint8(256*self.depthimg)
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
      _,self.mask = cv2.threshold(self.depthimg,self.thresh,255,cv2.THRESH_BINARY)
      self.mask = cv2.dilate(self.mask,self.kernel,iterations = 5)
      self.mask = cv2.erode(self.mask,self.kernel,iterations = 3)
      self.findcentroid()
      self.findang()
      self.finddist()
      cv2.bitwise_and(self.depthimg,self.mask)
      cv2.imshow('hello',self.depthimg)
      cv2.imshow('mask',self.mask)
      i = i +1
      cv2.waitKey(1)
    except CvBridgeError as e:
      print(e)
    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.depthimg, "mono8"))
      self.mask_pub.publish(self.bridge.cv2_to_imgmsg(self.mask, "mono8"))
    except CvBridgeError as e:
      print(e)


def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"

if __name__ == '__main__':
    main(sys.argv)
