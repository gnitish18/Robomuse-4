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
        self.arucsubpose = rospy.Subscriber('/robomuse/camwrtmark0'+str(j),Pose,self.callback)
        self.arucsubid = rospy.Subscriber('/robomuse/arucoidmarker0'+str(j),aruco_mapping.msg.ArucoMarker,self.arucbk)
        self.idn = -1
        self.n = 0
        self.flag = 0
        self.happened = 0
        self.pose = geometry_msgs.msg.Pose()
        self.pos = [0,0,0]
        self.ori = [0,0,0,1]
        self.visible = [0,0,0,0,0,0]
        self.idlist = []

    def repeater(self):
        while not rospy.is_shutdown():
            j = 0
            if self.happened == 1:
                for i in self.idlist:
                    if i == self.idn:
                        self.index = j
                        break
                    else:
                        j = j+1
                try:
                    if self.visible[j]==1:
                        (self.pos,self.ori) = self.listener.lookupTransform('markerframe_'+str(j),'camera_'+str(j), rospy.Time(0))
                        self.br.sendTransform((self.pos[0], self.pos[1], self.pos[2]),(self.ori[0],self.ori[1],self.ori[2],self.ori[3]),rospy.Time.now(),"globalmarker_"+str(j),'camera_rgb_optical_frame')
                except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                    continue
            rate.sleep()
        return 0




if __name__ == '__main__':
    rospy.init_node('aruco_rel_to_global')
    rate = rospy.Rate(30)
    a = converter()
    a.repeater()