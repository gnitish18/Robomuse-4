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

class converter():
    def __init__(self):
        self.listener = tf.TransformListener()
        self.br = tf.TransformBroadcaster()
        self.arucsubm = rospy.Subscriber('/aruco_marker_publisher/markers',aruco_msgs.msg.MarkerArray,self.markerarraycbk)
        self.arucsubp = rospy.Subscriber('/aruco_marker_publisher/markers_list',idarray,self.markerlistcbk)
        self.dictsub = rospy.Subscriber('/robomuse/marker_dictionary_map',idarray,self.dictcbk)
        self.vis_pub = rospy.Publisher('/robomuse/marker_flags',idarray,queue_size = 10)
        self.id_dictionary = np.array([])
        self.id_visible_flags= np.array([])
        self.posearray = []
        self.flag1 = 0

    def repeater(self):
        while not rospy.is_shutdown():
            j = 0
            for flag in self.id_visible_flags:
                try:
                    data1 = idarray()
                    if flag == 1:
                        p = self.posearray[j]
                        self.br.sendTransform((p.position.x,p.position.y,p.position.z),(p.orientation.x,p.orientation.y,p.orientation.z,p.orientation.w),rospy.Time.now(),"relmarker_"+str(j),'camera_rgb_optical_frame')
                        data1.data = self.id_visible_flags
                    else:
                        data1.data = self.id_visible_flags
                    j = j + 1
                    self.vis_pub.publish(data1)
                except(IndexError):
                    continue
            rate.sleep()
        return 0

    def dictcbk(self, msg):
        self.id_dictionary = msg.data
        self.id_dictionary = np.array(self.id_dictionary)

    def markerarraycbk(self,msg):
        pos = geometry_msgs.msg.Pose()
        pos.orientation.w = 1
        try:
            no = len(self.posearray)
            if no==0:
                for i in self.id_dictionary:
                    self.posearray.append(pos)
            no = len(self.posearray)
            while len(self.id_dictionary) > no:
                self.posearray.append(pos)
                no = no + 1
            for i in range(len(msg.markers)):
                try:
                    index = np.where(self.id_dictionary == msg.markers[i].id)
                    if index[0].size is not 0:
                        #print index[0][0]
                        """xo = msg.markers[i].pose.pose.orientation.x*self.posearray[index[0][0]].orientation.x  #ensure same sign of quaternion in marker
                        yo = msg.markers[i].pose.pose.orientation.y*self.posearray[index[0][0]].orientation.y  #ensure same sign of quaternion in marker
                        zo = msg.markers[i].pose.pose.orientation.z*self.posearray[index[0][0]].orientation.z  #ensure same sign of quaternion in marker
                        wo = msg.markers[i].pose.pose.orientation.w*self.posearray[index[0][0]].orientation.w  #ensure same sign of quaternion in marker
                        if xo > 0 and yo>0 and zo>0 and wo>0:"""
                    	self.posearray[index[0][0]] = msg.markers[i].pose.pose
                    else:
                        self.posearray.append(msg.markers[i].pose.pose)
                    #print self.posearray[i],msg.markers[i].id
                except(IndexError):
                    continue
        except:
            pass
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
    rospy.init_node('aruco_frame_generator')
    rate = rospy.Rate(30)
    a = converter()
    a.repeater()
