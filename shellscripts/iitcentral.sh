gnome-terminal --tab -e "bash -c \"roscore\"" \
--tab -e "bash -c \"rosrun rqt_console rqt_console\"" \
--tab -e "bash -c \"sleep 4s;roslaunch robomuse_drivers actual_iit_central_robomuse_nav_test.launch\"" \

