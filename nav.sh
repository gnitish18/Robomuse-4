gnome-terminal --tab -e "bash -c \"roslaunch robomuse_drivers robomuse_depth_reg.launch\"" \
--tab -e "bash -c \"shellscripts/./rtabnav.sh\"" \
--tab -e "bash -c \"shellscripts/./mbnav.sh\"" \
--tab -e "bash -c \"shellscripts/./marknav.sh\"" \
--tab -e "bash -c \"rosrun image_view image_view image:='/camera/rgb/image_raw'\"" \