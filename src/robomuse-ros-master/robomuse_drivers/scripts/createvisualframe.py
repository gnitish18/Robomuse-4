#!/usr/bin/env python  
import roslib
roslib.load_manifest('robomuse_drivers')
import rospy
import tf
from geometry_msgs.msg import Pose

def handle_robot_pose(msg):
    br = tf.TransformBroadcaster()
    pos = msg.position
    quat = msg.orientation
    br.sendTransform((pos.x, pos.y, pos.z),(quat.x,quat.y,quat.z,quat.w),rospy.Time.now(),"visualpos","markerpos")

def listener():
    rospy.init_node('create_visual_frame')
    rospy.Subscriber('/robomuse/visualcorrection',Pose,handle_robot_pose)
    rospy.spin()

if __name__ == '__main__':
    listener()
    
