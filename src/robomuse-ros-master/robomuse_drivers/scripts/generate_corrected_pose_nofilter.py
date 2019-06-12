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
                        poses.append([trans[0],trans[1],trans[2],rot[0],rot[1],rot[2],rot[3]])
                    j = j + 1
                except(IndexError,tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                    j = j + 1
                    continue
            summ = [0,0,0,0,0,0,0]
            j = 0
            for pose in poses:
                summ = [summ[0]+pose[0],summ[1]+pose[1],summ[2]+pose[2],summ[3]+pose[3],summ[4]+pose[4],summ[5]+pose[5],summ[6]+pose[6]]
                j += 1
            if not j == 0:
                avg = [summ[0]/j,summ[1]/j,summ[2]/j,summ[3]/j,summ[4]/j,summ[5]/j,summ[6]/j]
                if self.id_visible_flags.sum() > 0:
                    pf = [avg[0],avg[1],avg[2],pose[3],pose[4],pose[5],pose[6]]
                else:
                    pf = [avg[0],avg[1],50,pose[3],pose[4],pose[5],pose[6]]
                nor = math.sqrt(pf[5]**2 + pf[6]**2)
                self.br.sendTransform((pf[0],pf[1],0),(0,0,pf[5]/nor,pf[6]/nor),rospy.Time.now(),"corrected_pose_absolute","map")
            rate.sleep()
        return 0


if __name__ == '__main__':
    rospy.init_node('generate_corrected_pose')
    rate = rospy.Rate(30)
    a = generator()
    a.repeater()
