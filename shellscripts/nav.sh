gnome-terminal --tab -e "bash -c \"roslaunch robomuse_drivers robomuse_depth_reg.launch\"" \
--tab -e "bash -c \"./rtabnav.sh\"" \
--tab -e "bash -c \"./mbnav.sh\"" \
--tab -e "bash -c \"./sur.sh\"" \
--tab -e "bash -c \"./aruc.sh\"" \
--tab -e "bash -c \"./markerloca.sh\"" \
#--tab -e "bash -c \"./voice.sh\"" \
--tab -e "bash -c \"rostopic echo /robomuse/odom\"" \
