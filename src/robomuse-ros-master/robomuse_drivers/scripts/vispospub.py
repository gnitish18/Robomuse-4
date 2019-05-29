#!/usr/bin/env python  
import roslib
roslib.load_manifest('robomuse_drivers')
import rospy
import math
import tf
import geometry_msgs
from std_msgs.msg import Int16
from pyquaternion import Quaternion as qn
import numpy as np

class filter():
    def __init__(self):
        rospy.init_node('filterer')
        self.listener = tf.TransformListener()
        self.br = tf.TransformBroadcaster()
        rospy.Subscriber('/robomuse/inLOS',Int16,self.callback)
        self.vispospub = rospy.Publisher('/robomuse/vispose', geometry_msgs.msg.Pose,queue_size=1)
        self.pose = geometry_msgs.msg.Pose()
        self.pos = [0,0,0]
        self.ori = [0,0,0,1]
        self.ok = 1
        self.times = 0
        self.first = 1
        self.message = 0
        self.count =0
        self.count2 =0


    def listen(self):
        rate = rospy.Rate(1.0)
        while not rospy.is_shutdown():
            try:
#                (t1,r1)=self.listener.lookupTransform('marker1_frame', 'map', rospy.Time(0))
#                (t2,r2)=self.listener.lookupTransform('markerpos', 'map', rospy.Time(0))
#                dist = (t1[0]-t2[0])*(t1[0]-t2[0])+(t1[1]-t2[1])*(t1[1]-t2[1])+(t1[2]-t2[2])*(t1[2]-t2[2])
#                dist = math.sqrt(dist)
#                if(dist<0.3):
#                    self.ok = 1
#                    self.times = 0
#                else:
#                    self.times = self.times + 1
#                    if(self.times>5000 and self.first == 1):
#                        self.ok=0
#                        self. first= 0
#                    if(self.times>50 and self.first == 0):
#                        self.ok=0
#                    
                (self.pos,self.ori) = self.listener.lookupTransform('visualpos', 'map', rospy.Time(0))
                self.br.sendTransform((self.pose.position.x, self.pose.position.y, self.pose.position.z),(self.pose.orientation.x,self.pose.orientation.y,self.pose.orientation.z,self.pose.orientation.w),rospy.Time.now(),"map","visualposnorm")
                self.vispospub.publish(self.pose)
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue
            if(self.message):
                self.count = self.count +1
                self.count2 = 1
            if self.count >= 200:
                self.count =0 
            rate.sleep()

    def callback(self,msg):

        if msg.data == 1 and self.ok == 1 and self.count==0:
            self.count = 1
            self.pose.position.x = self.pos[0]
            self.pose.position.y = self.pos[1]
            self.pose.position.z = 0
            self.ori[0] = 0
            self.ori[1] = 0
            q = qn(self.ori)
            q = q.normalised
            self.ori = q
            self.pose.orientation.x = self.ori[0]
            self.pose.orientation.y = self.ori[1]
            self.pose.orientation.z = self.ori[2]
            self.pose.orientation.w = self.ori[3]
        elif msg.data==0:
            self.count = 0
            self.message = msg.data
            self.pose.position.z = 100
            

if __name__ == '__main__':
    a = filter()
    a.listen()
    

    