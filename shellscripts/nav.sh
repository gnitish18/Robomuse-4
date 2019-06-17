gnome-terminal --tab -e "bash -c \"roslaunch robomuse_drivers robomuse_depth_reg.launch\"" \
--tab -e "bash -c \"./rtabnav.sh\"" \
--tab -e "bash -c \"./mbnav.sh\"" \
--tab -e "bash -c \"./sur.sh\"" \