tab="--tab"
foo=""

cmd="bash -c 'cd ~/Documents/aio\ rem/ && java -jar AioRemoteDesktop3.5.0.jar';bash"
foo=($tab -e "$cmd")         

gnome-terminal "${foo[@]}"
foo=""

cmd="bash -c 'roslaunch robomuse_drivers robomuse_depth_reg.launch';bash"
foo=($tab -e "$cmd")         

gnome-terminal "${foo[@]}"
foo=""

sleep 5

cmd="bash -c 'roslaunch robomuse_drivers map_rtab.launch';bash"
foo=($tab -e "$cmd")

gnome-terminal "${foo[@]}"

sleep 5

cmd="bash -c 'roslaunch robomuse_drivers map_move_base.launch';bash"
foo=($tab -e "$cmd")

gnome-terminal "${foo[@]}"

sleep 5

cmd="bash -c 'cd ';bash"
foo=($tab -e "$cmd")

gnome-terminal "${foo[@]}"

exit 0
