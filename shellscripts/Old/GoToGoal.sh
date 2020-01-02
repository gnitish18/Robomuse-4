#!/bin/bash

roslaunch robomuse_drivers robomuse_depth_reg.launch
roslaunch robomuse_drivers nav_rtab.launch
roslaunch robomuse_drivers nav_move_base.launch
rosrun robomuse_drivers gotogoal.py