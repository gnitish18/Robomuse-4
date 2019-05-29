#!/usr/bin/env python
import rospy
from std_msgs.msg import Int8
import os
from time import sleep

flag = 1

def callback(data):
    if(data.data):
        sleep(2)
        flag = 0
        os.system("python /home/robomuse/Encryption/encryptdir.py encrypt")
rospy.init_node('encryptNode', anonymous=False)

rospy.Subscriber("startencryption", Int8, callback)

rospy.spin()
   



