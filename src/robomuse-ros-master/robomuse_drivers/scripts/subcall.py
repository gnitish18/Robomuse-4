#!/usr/bin/env python  
import roslib
roslib.load_manifest('robomuse_drivers')
import actionlib_msgs.msg
from nav_msgs.msg import Odometry
import rospy
import os
import subprocess
gstatus = -1
vstatus = -1
def gcbk(msg):
        global gstatus
        gstatus = msg.statuslist[0].status

def vcbk(msg):
        global vstatus
        t = (msg.twist.twist.linear.x)**2+(msg.twist.twist.linear.y)**2+(msg.twist.twist.angular.z)**2
        if t == 0:
                vstatus = 1
        else:
                vstatus = 0

def repeater():
        global gstatus
        rospy.Subscriber('/movebase/status',actionlib_msgs.msg.GoalStatusArray,gcbk)
        rospy.Subscriber('/robomuse/odom',Odometry,vcbk)
        while(not rospy.is_shutdown()):
                if gstatus == 3 or vstatus == 1:
                        subprocess.call("cd ~/catkin_ws/src/robomuse-ros-master/robomuse_drivers/scripts && ./clearcostmap.sh", shell=True)
                        rospy.sleep(2)
                rate.sleep()


if __name__ == '__main__':
        rospy.init_node('subprocess_caller')
        rate = rospy.Rate(1)
        rospy.sleep(10)
        repeater()