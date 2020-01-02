#!/usr/bin/env python
import roslib
roslib.load_manifest('aruco_ros')
import rospy
import math
import tf
import geometry_msgs.msg
import aruco_msgs.msg
from visualization_msgs.msg import Marker
from std_msgs.msg import Int32
from std_msgs.msg import UInt32MultiArray as idarray
import numpy as np

class generator():
    def __init__(self):
        self.listener = tf.TransformListener()
        self.br = tf.TransformBroadcaster()
        self.dictsub = rospy.Subscriber('/robomuse/marker_dictionary_map',idarray,self.dictcbk)
        self.vis_pub = rospy.Subscriber('/robomuse/marker_flags',idarray,self.flagcbk)
        self.id_dictionary = np.array([])
        self.id_visible_flags= np.array([])
        self.posearray = []
        self.flag1 = 0

    def dictcbk(self,msg):
        self.id_dictionary = msg.data
        self.id_dictionary = np.array(self.id_dictionary)
        return 0

    def flagcbk(self,msg):
        self.id_visible_flags = msg.data
        self.id_visible_flags = np.array(self.id_visible_flags)
        return 0

    def repeater(self):
        while not rospy.is_shutdown():
            j = 0
            poses = []
            for flag in self.id_visible_flags:
                try:
                    if flag == 1:
                        (trans,rot) = self.listener.lookupTransform("relmarker_"+str(j),'base_link', rospy.Time(0))
                        self.br.sendTransform(trans,rot,rospy.Time.now(),"corrected_pose"+str(j),"markerframe_"+str(j))
                        (trans,rot) = self.listener.lookupTransform('map',"corrected_pose"+str(j), rospy.Time(0))
                        poses.append([trans[0],trans[1],0,rot[0],rot[1],rot[2],rot[3]])
                    j = j + 1
                except(IndexError,tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                    j = j + 1
                    continue
            rate.sleep()
        return 0

if __name__ == '__main__':
    rospy.init_node('generate_corrected_pose')
    rate = rospy.Rate(30)
    a = generator()
    a.repeater()
