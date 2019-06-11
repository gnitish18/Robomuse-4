#!/usr/bin/env python
# license removed for brevity
from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import rospy
from geometry_msgs.msg import Pose
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import subprocess

goals= [Pose(),Pose(),Pose(),Pose(),Pose()]
i = 0

def cbk0(msg):
    global goals
    goals[0] = msg 
def cbk1(msg):
    global goals
    goals[1] = msg 
def cbk2(msg):
    global goals
    goals[2] = msg 
def cbk3(msg):
    global goals
    goals[3] = msg 
def cbk4(msg):
    global goals
    goals[4] = msg 

def movebase_client(n):
    global goals
    global number
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = goals[n].position.x
    goal.target_pose.pose.position.y = goals[n].position.y
    goal.target_pose.pose.orientation.w = goals[n].orientation.z
    goal.target_pose.pose.orientation.w = goals[n].orientation.w
    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    i = 0
    rospy.init_node('movebase_client_py')
    rospy.Subscriber('/robomuse/goal_0',Pose,cbk0)
    rospy.Subscriber('/robomuse/goal_1',Pose,cbk1)
    rospy.Subscriber('/robomuse/goal_2',Pose,cbk2)
    rospy.Subscriber('/robomuse/goal_3',Pose,cbk3)
    rospy.Subscriber('/robomuse/goal_4',Pose,cbk4)
    while(1):
        n = input()
        try:
            result = movebase_client(n)
            if result:
                rospy.loginfo("Goal execution done!")
                subprocess.call("./sayhello.sh", shell=True)
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")
        rospy.sleep(3)


