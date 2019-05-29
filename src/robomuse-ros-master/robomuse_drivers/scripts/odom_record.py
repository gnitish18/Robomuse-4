#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import matplotlib.pyplot as plt
from csv import writer

x_pose = []
y_pose = []
z_ang = []
x_vel =[]
z_velang = []

def callback(odom):
    x_pose.append(-odom.pose.pose.position.y)
    y_pose.append(odom.pose.pose.position.x)
    orientation_q = odom.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    print yaw*180/3.14
    z_ang.append(yaw)
    x_vel.append(odom.twist.twist.linear.x)
    z_velang.append(odom.twist.twist.angular.z)

def at_closing():
    print "closing !!!!"
    print sum(x_vel) / float(len(x_vel))
    print sum(z_velang) / float(len(z_velang))
    print "closed ????"
    with open('odom_data.csv', 'wb') as f:
        wtr = writer(f, delimiter= ' ')
        wtr.writerows(zip(x_pose,y_pose,z_ang,x_vel,z_velang))
    f.close()
    plt.plot(x_pose,y_pose)
    plt.axis([-1, 1, -1, 5])
    plt.show()

    
def odom_listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('odom_listener', anonymous=True)

    rospy.Subscriber("/robomuse/odom", Odometry, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

    rospy.on_shutdown(at_closing)

if __name__ == '__main__':
    odom_listener()