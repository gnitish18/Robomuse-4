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
                    with open('/home/nitish/catkin_ws/src/robomuse-ros-master/robomuse_drivers/markers/'+self.nst+'/marker'+str(flag)+'.csv',mode = 'r')as f:
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
                            Pk = np.matmul(np.identity(pose.size)-np.matmul(Kg,(np.identity(pose.size))),Pk)
                            poseo = posen
                        ori = pyqu(poseo[3],poseo[4],poseo[5],poseo[6])
                        ori = ori.normalised
                        poseo = [poseo[0],poseo[1],poseo[2],ori[0],ori[1],ori[2],ori[3]]
                        self.br.sendTransform((poseo[0],poseo[1],poseo[2]),(poseo[3],poseo[4],poseo[5],poseo[6]),rospy.Time.now(),"markerframe_"+str(j),'map')
                        self.posearray.append(poseo)
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
                self.br.sendTransform( (0,1.8,0),(0,0,-0.707,0.707),rospy.Time.now(),"goal_"+str(j),"markerframeground_"+str(j))
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
