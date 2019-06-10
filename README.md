# Robomuse-4
<h3> Autonomous Robot Platform of IIT Delhi </h3>
<h3> Running the robot</h3>
<h4> To start the robot this command has to be run in a terminal</h4>
<code>
roslaunch robomuse_drivers robomuse_depth_reg.launch
</code>
<h4>For creating a new map</h4>
<code>
roslaunch robomuse_drivers map_rtab.launch
</code>
<h4>For mapping along with markers run this with above</h4>
<code>
roslaunch aruco_ros marker_publisher.launch
</code>

<h4>For navigating on given map </h4>
<code>
roslaunch robomuse_drivers nav_rtab.launch \
</code>
<code>
roslaunch robomuse_drivers nav_move_base.launch
</code>
