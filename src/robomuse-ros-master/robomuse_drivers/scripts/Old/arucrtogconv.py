#!/usr/bin/env python
import roslib
roslib.load_manifest('robomuse_drivers')
import rospy
import math
import tf
import geometry_msgs
import aruco_mapping.msg
from visualization_msgs.msg import Marker
from std_msgs.msg import Int32
import numpy as np

class converter():
    def __init__(self):
        self.listener = tf.TransformListener()
        self.br = tf.TransformBroadcaster()
        self.arucsubm = rospy.Subscriber('aruco_markers',Marker,self.callback)
        self.arucsubp = rospy.Subscriber('aruco_poses',aruco_mapping.msg.ArucoMarker,self.arucbk)
        self.idn = -1
        self.flag = 0
        self.pose = geometry_msgs.msg.Pose()
        self.pos = [0,0,0]
        self.ori = [0,0,0,1]
        self.idlist = []

    def repeater(self):
        while not rospy.is_shutdown():
            j = 0
            for i in self.idlist:
                if i == self.idn:
                    self.index = j
                    break
                else:
                    j = j+1
            try:
                if self.flag == 1:
                    (self.pos,self.ori) = self.listener.lookupTransform('markerframe_'+str(j),'camera_'+str(j), rospy.Time(0))
                    self.br.sendTransform((self.pos[0], self.pos[1], self.pos[2]),(self.ori[0],self.ori[1],self.ori[2],self.ori[3]),rospy.Time.now(),"globalmarker_"+str(j),'camera_rgb_optical_frame')
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            rate.sleep()
        return 0

    def arucbk(self,msg):
        self.idlist = msg.marker_ids
        print 'hey'
        if msg.marker_visibile == True:
            self.flag = 1
        else:
            self.flag = 0
        return 0

    def callback(self,msg):
        self.idn = msg.id
        return 0

if __name__ == '__main__':
    rospy.init_node('aruco_rel_to_global')
    rate = rospy.Rate(30)
    a = converter()
    a.repeater()
