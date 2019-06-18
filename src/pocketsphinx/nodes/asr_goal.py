#!/usr/bin/env python

import rospy
import subprocess
from std_msgs.msg import String
from std_msgs.msg import Int64

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %d", data.data)
    if data == 1:
        print 'GOAL NOT REACHED'
        subprocess.call("espeak 'unable to reach goal'", shell=True)
        rospy.sleep(1)
        subprocess.call("espeak 'aborting'", shell=True)
    elif data == 3:
        print 'REACHED GOAL'
        subprocess.call("espeak 'reached goal'", shell=True)

def listener():
    rospy.init_node('asr_goal', anonymous=True)
    rospy.Subscriber('nav_base/goal', Int64, callback)
    rospy.spin()

if __name__ == '__main__':
    while(1):
        try:
            listener()
        except:
            pass
