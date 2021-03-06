#!/usr/bin/env python
import csv
import os
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

class converter():
    def __init__(self):
        self.listener = tf.TransformListener()
        os.mkdir('poses')
        self.br = tf.TransformBroadcaster()
        self.arucsubp = rospy.Subscriber('/aruco_marker_publisher/markers_list',idarray,self.markerlistcbk)
        self.id_dictionary = np.array([])
        self.id_visible_flags= np.array([])
        self.posearray = []
        self.flag1 = 0

    def repeater(self):
        with open('poses\marker'+str(self.id_dictionary[j])+'.csv','rt')as f:
            data = csv.reader(f)
            for row in data:
                print(row)
        j = j + 1
                except(IndexError,tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                    continue
            rate.sleep()
        return 0

    def markerlistcbk(self,msg):
        #print('listcbk')
        visiblemarkers = np.array(msg.data)
        if not self.id_dictionary.size:
            self.id_dictionary = np.array(msg.data)
            self.id_visible_flags = np.ones(self.id_dictionary.size)
        else:
            self.id_visible_flags = np.zeros(self.id_dictionary.size)
            for idi in visiblemarkers:
                index = np.where(self.id_dictionary == idi)
                if index[0].size is not 0:
                    self.id_visible_flags[index] = 1
                else:
                    self.id_dictionary = np.append(self.id_dictionary,idi)
                    self.id_visible_flags = np.append(self.id_visible_flags,1)
        return 0

if __name__ == '__main__':
    rospy.init_node('aruco_csv_generator')
    rate = rospy.Rate(30)
    a = converter()
    a.repeater()