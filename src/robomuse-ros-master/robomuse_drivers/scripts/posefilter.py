#!/usr/bin/env python  
import roslib
roslib.load_manifest('aruco_ros')
import rospy
import math
import tf
import geometry_msgs.msg
import aruco_msgs.msg
from visualization_msgs.msg import Marker
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from std_msgs.msg import Int32
from std_msgs.msg import UInt32MultiArray as idarray
import numpy as np

class generator():
    def __init__(self):
        self.listener = tf.TransformListener()
        self.br = tf.TransformBroadcaster()
        #self.dictsub = rospy.Subscriber('/robomuse/marker_dictionary_map',idarray,self.dictcbk)
        self.vis_pub = rospy.Subscriber('/robomuse/marker_flags',idarray,self.flagcbk)
        rospy.Subscriber('robomuse/odom',Odometry,self.odomcbk)
        self.id_dictionary = np.array([])
        self.id_visible_flags= np.array([])
        self.posearray = []
        self.ox =0
        self.oy =0
        self.otheta =0
        self.vx = 0
        self.vy = 0
        self.vtheta = 0
        self.flag1 = 0

    def flagcbk(self,msg):
        self.id_visible_flags = msg.data
        self.id_visible_flags = np.array(self.id_visible_flags)
        return 0
    
    def odomcbk(self,odom):
        self.oy = odom.pose.pose.position.y
        self.ox = odom.pose.pose.position.x
        orientation_q = odom.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
        self.otheta = yaw

    def repeater(self):
        while not rospy.is_shutdown():
            print 'hi'
            j = 0
            su = 0
            for flag in self.id_visible_flags:
                su = flag + su
            print su
            if su == 0:
                self.pose = [self.ox, self.oy, self.otheta]
            else:
                try:
                    (trans,rot) = self.listener.lookupTransform('map',"corrected_pose_absolute"+str(j), rospy.Time(0))
                    (roll, pitch, yaw) = euler_from_quaternion (rot)
                    self.vx = trans[0]
                    self.vy = trans[1]
                    self.vtheta = yaw
                    self.pose = [self.vx, self.vy, self.vtheta]
                except:
                    pass
            P = np.identity(3,dtype=float)
            if self.flag1 == 0:
                self.flag1 = 1
                m = np.array(self.pose)
                Kg = [0.0,0.0,0.0]
                poseo = m
                Pk = np.zeros((3,3))
                V = np.zeros((3,3))
            pose = np.array(self.pose)
            V = np.linalg.inv(P+Pk)
            Kg = np.matmul(Pk,V) 
            diff = (pose - poseo)
            posen = poseo + np.matmul(Kg,diff)
            Pk = np.matmul(np.identity(pose.size)-np.matmul(Kg,(np.identity(pose.size))),Pk)
            poseo = posen
            if su == 0:
                self.br.sendTransform((100,100,100),(0,0,0,1),rospy.Time.now(),"corrected_pose_filtered",'map')
            else:
                x = posen[0]
                y = posen[1]
                yaw = posen[2]
                print x,y,yaw
                [rx,ry,rz,rw] = quaternion_from_euler(0,0,yaw)
                self.br.sendTransform((x,y,0),(rx,ry,rz,rw),rospy.Time.now(),"corrected_pose_filtered",'map')
            rate.sleep()
        return 0


if __name__ == '__main__':
    rospy.init_node('filtered_pose')
    rate = rospy.Rate(30)
    a = generator() 
    a.repeater()
