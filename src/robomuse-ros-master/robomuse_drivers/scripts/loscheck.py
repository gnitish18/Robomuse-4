#!/usr/bin/env python
import rospy
import tf
from geometry_msgs.msg import Pose
from std_msgs.msg import Int16

class loschecker:
    def __init__(self):
        rospy.init_node('create_visual_frame')
        self.rate = rospy.Rate(5.0)
        self.a = rospy.Publisher('/robomuse/inLOS',Int16,queue_size=5)

    def handle_marker_pose(self,msg):
        self.a.publish(1)

    def listener(self):
        rospy.Subscriber('/aruco_simple/pose',Pose,self.handle_marker_pose)
        while(True):
            self.a.publish(0)
            rospy.sleep(0.5)
    

if __name__ == '__main__':
    n = loschecker()
    n.listener()

    
