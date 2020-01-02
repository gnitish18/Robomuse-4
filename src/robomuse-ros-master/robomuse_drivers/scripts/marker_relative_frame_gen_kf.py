#!/usr/bin/env python
import roslib
roslib.load_manifest('aruco_ros')
import rospy
import math
import tf
import geometry_msgs.msg
import aruco_msgs.msg
from visualization_msgs.msg import Marker
from pyquaternion import Quaternion as pyqu
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
            if True:
                j = 0
                for flag in self.id_visible_flags:
                    try:
                        data1 = idarray()
                        if flag == 1:
                            p = self.posearray[j]
                            P = np.identity(7,dtype=float)
                            if self.flag1 == 0:
                                self.flag1 = 1
                                m = [p.position.x,p.position.y,p.position.z,p.orientation.x,p.orientation.y,p.orientation.z,p.orientation.w]
                                Kg = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
                                poseo = m
                                Pk = np.zeros((7,7))
                                V = np.zeros((7,7))
                            pose = np.array([p.position.x,p.position.y,p.position.z,p.orientation.x,p.orientation.y,p.orientation.z,p.orientation.w])
                            V = np.linalg.inv(P+Pk)
                            Kg = np.matmul(Pk,V)
                            diff = (pose - poseo)
                            posen = poseo + np.matmul(Kg,diff)
                            Pk = np.matmul(np.identity(pose.size)-np.matmul(Kg,(np.identity(pose.size))),Pk)
                            poseo = posen
                            ori = pyqu(poseo[3],poseo[4],poseo[5],poseo[6])
                            ori = ori.normalised
                            poseo = [poseo[0],poseo[1],poseo[2],ori[0],ori[1],ori[2],ori[3]]
                            self.br.sendTransform((poseo[0],poseo[1],poseo[2]),(poseo[3],poseo[4],poseo[5],poseo[6]),rospy.Time.now(),"relmarker_"+str(j),'camera_rgb_optical_frame')
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
        try:
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
        except:
            pass
        return 0


if __name__ == '__main__':
    rospy.init_node('aruco_frame_generator')
    rate = rospy.Rate(30)
    a = converter()
    a.repeater()
