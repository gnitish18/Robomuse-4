gnome-terminal --tab -e "bash -c \"roslaunch robomuse_drivers robomuse_depth_reg.launch\"" \
--tab -e "bash -c \"shellscripts/./rtabmap_exploration.sh\"" \
--tab -e "bash -c \"shellscripts/./mbmap_exploration.sh\"" \
--tab -e "bash -c \"shellscripts/./markmap.sh\"" \
--tab -e "bash -c \"shellscripts/./manmap.sh\"" \
--tab -e "bash -c \"shellscripts/./explore.sh\"" \