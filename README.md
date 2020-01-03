# Robomuse-4
<h2> Autonomous Robot Platform of IIT Delhi </h2>
<h3> Setting up the Robot in your laptop:</h3>
<p> Clone the repository and copy all the files of src into the src in your catkin workspace.</p>
<p> Copy the shellscripts folder and .sh files into your home directory.</p>
<p> Copy the the arduino libraries into your arduino folder in home directory.</p>
<h3> Operating the Robot: </h3>
<p> Plug in the usb cables and turn on the switch </p>
<p> Open the terminal window </p>
<h4> To create a map manually: </h4>
<p> Run <code>./map.sh</code></p>
<p> Open another terminal window and run <code>rosrun robomuse_drivers teleop.py</code> and maneuver the robot to create a map</p>
<p> To save the map, open another terminal window and run <code>rosrun map_server map_saver -f "mapname"</code>
<h4> To create a map automatically: </h4>
<p> Run <code>./robotstart.sh</code></p>
<p> Click <code>MAP</code> button in the GUI to start mapping</p>
<p> To save the map, open another terminal window and run <code>rosrun map_server map_saver -f "mapname"</code>
<h4> To navigate in a created map: </h4>
<p> Set the required map in "nav_move_base.launch" and markers in "nav_marker_publish.launch" files and run <code>./nav.sh</code></p>
<h4> To navigate for surveillance automatically: </h4>
<p> Set the required map in "nav_move_base.launch", markers in "nav_marker_publish.launch" files and the goal values in the corresponding python file</p>
<p> Run <code>./robotstart.sh</code></p>
<p> Click <code>START</code> button in the GUI</p>
<p> To move autonomously, press <code>AUTONOMOUS</code></p>
<p> To move manually, press <code>TELE-OPERATION</code></p>
<p> To close, press <code>TURNOFF</code></p>
