echo 'Existing maps'
cd ~/catkin_ws/src/robomuse-ros-master/robomuse_drivers/maps/
ls
echo 'Enter name of map'
read MAPNAME
rosrun map_server map_saver -f $MAPNAME
cd ~/