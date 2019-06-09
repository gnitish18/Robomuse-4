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

goals = [[1.56,-1.54,0,0,0,-0.31,0.95],[2,0.34,0,0,0,0.34,0.97],[0.8,-2.67,0,0,0,-0.34,1],[-0.59,-1,0,0,0,1,1]]
i = 0
def movebase_client(n):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = goals[n][0]
    goal.target_pose.pose.position.y = goals[n][1]
    goal.target_pose.pose.orientation.w = goals[n][5]
    goal.target_pose.pose.orientation.w = goals[n][6]

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    i = 0
    while(1):
        n = input()
        try:
            rospy.init_node('movebase_client_py')
            result = movebase_client(n)
            if result:
                rospy.loginfo("Goal execution done!")
                subprocess.call("./sayhello.sh", shell=True)
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")
        rospy.sleep(3)


