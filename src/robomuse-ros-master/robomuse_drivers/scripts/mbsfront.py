#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import subprocess

xpos = [4.00,0.00]
i = 0
def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    global i
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = xpos[i]
    i = i+1
    goal.target_pose.pose.orientation.z = 10000.0
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
            subprocess.call("./sayhello.sh", shell=True)
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
    rospy.sleep(3)
    try:
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
            subprocess.call("./sayhello.sh", shell=True)
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")


