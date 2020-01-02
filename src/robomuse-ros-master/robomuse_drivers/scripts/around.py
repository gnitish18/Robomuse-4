#!/usr/bin/env python
# license removed for brevity
from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *
import rospy
import std_msgs.msg
from geometry_msgs.msg import Pose
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import subprocess

goals = [Pose(), Pose(), Pose(), Pose(), Pose(), Pose()]
i = 0
n = -1


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


def cbk5(msg):
    global goals
    goals[5] = msg


xpos = [7.4, 13.0, 19.2, 24.8, 28.5, 30.5, 30.9, 31.2,
        29.9, 27.6, 24.5, 20.2, 16.1, 10.2, 4.2, -2.9]
ypos = [-5.7, -6.0, -5.2, -2.8, 2.9, 7.6, 9.6, 14.3,
        19.7, 24.4, 28.4, 31.6, 31.6, 31.4, 29.7, 24.4]
thetaz = [-0.10, 0.04, 0.10, 0.28, 0.5, 0.64, 0.63,
          0.67, 0.76, 0.82, 0.90, 0.97, 0.99, 0.99, 0.98, 0.88]
thetaw = [0.99, 0.99, 0.99, 0.96, 0.87, 0.77, 0.77, 0.74,
          0.64, 0.57, 0.42, 0.25, 0.06, -0.05, -0.17, -0.44]


def movebase_client(n):
    global goals
    if n > -1:
        client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        client.wait_for_server()
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = xpos[n]
        goal.target_pose.pose.position.y = ypos[n]
        goal.target_pose.pose.orientation.z = thetaz[n]
        goal.target_pose.pose.orientation.w = thetaw[n]
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
    rospy.Subscriber('/robomuse/goal_0', Pose, cbk0)
    rospy.Subscriber('/robomuse/goal_1', Pose, cbk1)
    rospy.Subscriber('/robomuse/goal_2', Pose, cbk2)
    rospy.Subscriber('/robomuse/goal_3', Pose, cbk3)
    rospy.Subscriber('/robomuse/goal_4', Pose, cbk4)
    rospy.Subscriber('/robomuse/goal_5', Pose, cbk5)
    for n in range(16):
        try:
            result = movebase_client(n)
            if result:
                rospy.loginfo("Goal execution done!")
                subprocess.call("./sayhello.sh", shell=True)
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")
        if n == 0:
            n = 5
        else:
            n = 0
        rospy.sleep(3)
