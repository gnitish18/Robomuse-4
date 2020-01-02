gnome-terminal --tab -e "bash -c \"roslaunch robomuse_drivers robomuse_depth_reg.launch\"" \
--tab -e "bash -c \"shellscripts/./rtabmap.sh\"" \
--tab -e "bash -c \"shellscripts/./mbmap.sh\"" \
--tab -e "bash -c \"shellscripts/./markmap.sh\"" \
--tab -e "bash -c \"shellscripts/./manmap.sh\"" \