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
            dist = []
            for flag in self.id_visible_flags:
                try:
                    if flag == 1:
                        (trans,rot) = self.listener.lookupTransform('map',"corrected_pose"+str(j), rospy.Time(0))
                        dist.append(math.sqrt(trans[0]**2 + trans[1]**2 + trans[2]**2))
                        s = math.sqrt(rot[2]**2 + rot[3]**2)
                        poses.append([trans[0],trans[1],0,0,0,rot[2]/s,rot[3]/s])
                    else:
                        dist.append(100000.0)
                        poses.append([50,50,50,0,0,0,1])
                    j = j + 1
                except(IndexError,tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                    j = j + 1
                    continue
            if len(dist)>0:
                if self.id_visible_flags[dist.index(min(dist))]==1:
                    if not min(dist)>1000:
                        p =poses[dist.index(min(dist))]
                        self.br.sendTransform((p[0],p[1],0),(p[3],p[4],p[5],p[6]),rospy.Time.now(),"corrected_pose_absolute",'map')
                    else:
                        self.br.sendTransform((100,100,100),(0,0,0,1),rospy.Time.now(),"corrected_pose_absolute",'map')
                else:
                    self.br.sendTransform((100,100,100),(0,0,0,1),rospy.Time.now(),"corrected_pose_absolute",'map')
            rate.sleep()
        return 0


if __name__ == '__main__':
    rospy.init_node('choose_corrected_pose')
    rate = rospy.Rate(30)
    a = generator()
    a.repeater()
