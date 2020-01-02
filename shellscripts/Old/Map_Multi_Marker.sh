#!/bin/bash

#roslaunch robomuse_drivers robomuse_depth_reg.launch
#roslaunch robomuse_drivers map_rtab.launch
#roslaunch aruco_ros marker_publisher.launch
#rosrun robomuse_drivers teleop.py

gnome-terminal --tab -e "bash -c \"roslaunch robomuse_drivers robomuse_depth_reg.launch\"" \
--tab -e "bash -c \"./map_rtab.sh\"" \
--tab -e "bash -c \"./marker_publisher.sh\"" \
--tab -e "bash -c \"./teleop.sh\"" \
#--tab -e "bash -c \"./aruc.sh\"" \
#--tab -e "bash -c \"./markerloca.sh\"" \
#--tab -e "bash -c \"./voice.sh\"" \
#--tab -e "bash -c \"rostopic echo /robomuse/odom\"" \