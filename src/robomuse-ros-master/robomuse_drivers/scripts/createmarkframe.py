#!/usr/bin/env python  
import roslib
roslib.load_manifest('robomuse_drivers')
import numpy as np
import rospy
import tf
from pyquaternion import Quaternion

class mover:
    def __init__(self):
        self.x=0
        self.y=0
        self.z=0
        self.r=0
        self.p=0
        self.a=0
        self.w=1


if __name__ == '__main__':
    data = np.genfromtxt('/home/robomuse/catkin_ws/src/robomuse-ros-master/robomuse_drivers/marker.csv',dtype=None, delimiter=',')
    rospy.init_node('markerwrtmap')
    data = data.transpose()
    mv= mover()
    mv.x = np.mean(data[0])
    mv.y = np.mean(data[1])
    mv.z = np.mean(data[2])
    mv.rx = np.mean(data[3])
    mv.ry = np.mean(data[4])
    mv.rz = np.mean(data[5])
    mv.rw = np.mean(data[6])
    q = Quaternion(mv.rx,mv.ry,mv.rz,mv.rw)
    q = q.normalised
    print q
    mv.rx = q[0]
    mv.ry  = q[1]
    mv.rz = q[2]
    mv.rw = q[3]
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        br.sendTransform((mv.x, mv.y, mv.z),(mv.rx,mv.ry,mv.rz,mv.rw),rospy.Time.now(),"markerpos","map")
        rate.sleep()
