#!/usr/bin/env python

import rospy
import geometry_msgs.msg
import random
import std_srvs.srv
import subprocess

GOAL_POSE = {'C1': [3.00, 0.00, 0.000],
             'S4': [0.00, 0.00, 0.000]}


class NavigationStressTest(object):
    def __init__(self):
        self.event_in = None
        self.nav_goal = None
        
        self.nav_pub = rospy.Publisher("/move_base_simple/goal", geometry_msgs.msg.PoseStamped,queue_size=2)
    
    def run(self):        
        while not rospy.is_shutdown():
            rospy.sleep(3)
            clear_costmap = rospy.ServiceProxy('/move_base/clear_costmaps', std_srvs.srv.Empty)
            rospy.sleep(3)
            self.publish_1stgoal()
            subprocess.call("sayhello.sh", shell=True)
            rospy.sleep(3)
	    self.publish_2ndgoal()
            subprocess.call("sayhello.sh", shell=True)
            

    def publish_1stgoal(self):
        goal = 'C1'
        pose = GOAL_POSE[goal]
        self.nav_goal = geometry_msgs.msg.PoseStamped()
        self.nav_goal.header.frame_id = 'map'
        self.nav_goal.pose.position.x = pose[0]
        self.nav_goal.pose.position.y = pose[1]
        self.nav_goal.pose.orientation.z = pose[2]
	self.nav_goal.pose.orientation.w = 1.0
        self.nav_pub.publish(self.nav_goal)
        rospy.loginfo("going to pose "+goal)
        self.nav_pub.wait()

    def publish_2ndgoal(self):
        goal = 'S4'
        pose = GOAL_POSE[goal]
        self.nav_goal = geometry_msgs.msg.PoseStamped()
        self.nav_goal.header.frame_id = 'map'
        self.nav_goal.pose.position.x = pose[0]
        self.nav_goal.pose.position.y = pose[1]
        self.nav_goal.pose.orientation.z = pose[2]
	self.nav_goal.pose.orientation.w = 1.0
        self.nav_pub.publish(self.nav_goal)
        rospy.loginfo("going to pose "+goal)
        self.nav_pub.wait()

def main():
    rospy.init_node("nav_goal_stresstest", anonymous=False)
    nav_stress_test = NavigationStressTest()
    nav_stress_test.run()

if __name__ == '__main__':
    main()


