#!/usr/bin/env python
import csv
import os 
import roslib
roslib.load_manifest('aruco_ros')
import rospy
import math
import tf
import subprocess
from geometry_msgs.msg import Pose
import aruco_msgs.msg
from pyquaternion import Quaternion as pyqu
from visualization_msgs.msg import Marker
from std_msgs.msg import Int32
from std_msgs.msg import UInt32MultiArray as idarray
import numpy as np


class converter():
    def __init__(self):
        self.listener = tf.TransformListener()
        self.br = tf.TransformBroadcaster()
        self.dict_pub = rospy.Publisher('/robomuse/marker_dictionary_map',idarray,queue_size = 10)
        self.id_dictionary = np.array([])
        self.id_visible_flags= np.array([])
        param_name = rospy.search_param('folder_name')
        v = rospy.get_param(param_name)
        self.nst = v
        self.posearray = []
        self.goalarray = []
        self.goalpub = []
        self.flag1 = 0

    def repeater(self):
        subprocess.call("cd ~/catkin_ws/src/robomuse-ros-master/robomuse_drivers/markers && ls && echo 'select marker folder'", shell=True)
        j = 0
        for flag in range(1024):
                try:
                    test = 0            
                    with open('/home/srike27/catkin_ws/src/robomuse-ros-master/robomuse_drivers/markers/'+self.nst+'/marker'+str(flag)+'.csv',mode = 'r')as f:
                        data = csv.reader(f)
                        summ = [0,0,0,0,0,0,0]
                        k = 0
                        for row in data:
                            test = 1
                            for l in range(len(row)):
                                summ[l] = float(row[l]) + summ[l]
                            k = k + 1
                    if test == 1:
                        avg = [summ[0]/k,summ[1]/k,summ[2]/k,summ[3]/k,summ[4]/k,summ[5]/k,summ[6]/k]
                        ori = pyqu(avg[3],avg[4],avg[5],avg[6])
                        ori = ori.normalised
                        #print ori
                        avg = [avg[0],avg[1],avg[2],ori[0],ori[1],ori[2],ori[3]]
                        self.br.sendTransform((avg[0],avg[1],avg[2]),(avg[3],avg[4],avg[5],avg[6]),rospy.Time.now(),"markerframe_"+str(j),'map')
                        self.posearray.append([avg[0],avg[1],avg[2],avg[3],avg[4],avg[5],avg[6]])
                        self.id_dictionary = np.append(self.id_dictionary,flag)
                        j += 1
                        f.close()
                except(IndexError,tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, IOError):
                    continue
        ff = 0
        while not rospy.is_shutdown():
            j = 0
            for pose in self.posearray:
                trans = (pose[0],pose[1],pose[2])
                rot = (pose[3],pose[4],pose[5],pose[6])
                self.br.sendTransform((trans[0],trans[1],trans[2]),(rot[0],rot[1],rot[2],rot[3]),rospy.Time.now(),"markerframe_"+str(j),'map')
                ori = pyqu(0,0,rot[2],rot[3])
                ori = ori.normalised
                self.br.sendTransform((trans[0],trans[1],0),(ori[0],ori[1],ori[2],ori[3]),rospy.Time.now(),"markerframeground_"+str(j),'map')
                self.br.sendTransform( (0,1.5,0),(0,0,-0.707,0.707),rospy.Time.now(),"goal_"+str(j),"markerframeground_"+str(j))
                if ff == 0:
                    self.goalpub.append(rospy.Publisher('/robomuse/goal_'+str(j),Pose,queue_size = 10))
                try:
                    (posi,orii) = self.listener.lookupTransform('map','goal_'+str(j), rospy.Time(0))
                    pp = Pose()
                    pp.position.x = posi[0]
                    pp.position.y = posi[1]
                    pp.position.z = posi[2]
                    pp.orientation.x = orii[0]
                    pp.orientation.y = orii[1]
                    pp.orientation.z = orii[2]
                    pp.orientation.w = orii[3]
                    self.goalpub[j].publish(pp)
                except(tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                    pass
                n = idarray()
                n.data = self.id_dictionary
                self.dict_pub.publish(n)
                j += 1
            ff = 1
            rate.sleep()
        return 0


if __name__ == '__main__':
    rospy.init_node('aruco_csv_generator')
    rate = rospy.Rate(30)
    a = converter()
    a.repeater()