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
        print self.nst
        self.posearray = []
        self.goalarray = []
        self.goalpub = []
        self.flag1 = 0

    def repeater(self):
        #subprocess.call("cd ~/catkin_ws/src/robomuse-ros-master/robomuse_drivers/markers && ls && echo 'select marker folder'", shell=True)
        j = 0
        for flag in range(1024):
                try:    
                    with open('/home/srike27/catkin_ws/src/robomuse-ros-master/robomuse_drivers/markers/'+'20_06_2019_14_06_08'+'/marker'+str(flag)+'.csv',mode = 'r')as f:
                        data = csv.reader(f)
                        values = []
                        k = 0
                        for row in data:
                            val = np.array([0.0,0.0,0.0,0.0,0.0,0.0,0.0])
                            for l in range(len(row)):
                                val[l] = float(row[l])
                            val = np.array(val)
                            values.append(val)
                            k = k + 1
                        f.close()
                        #print values

                        valueso = np.array(values)
                        P = np.cov(valueso.T)
                        m = np.mean(valueso,axis=0)
                        Kg = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                        Pk = np.zeros((7,7))
                        V = np.zeros((7,7))
                        poseo = m
                        for pose in values:
                            V = np.linalg.inv(P+Pk)
                            Kg = np.matmul(Pk,V)
                            diff = (pose - poseo)
                            posen = poseo + np.matmul(Kg,diff)
                            Pk = np.matmul((np.identity(pose.size)-P),P)
                            poseo = posen
                        print poseo,m 
                except(IndexError,tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException, IOError):
                    continue
        return 0


if __name__ == '__main__':
    rospy.init_node('aruco_csv_generator')
    rate = rospy.Rate(30)
    a = converter()
    a.repeater()