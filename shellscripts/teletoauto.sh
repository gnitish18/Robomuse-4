gnome-terminal --tab -e "bash -c \"rosrun robomuse_drivers teletoauto.py\"" \
sleep 1 \
--tab -e "bash -c \"rosrun robomuse_drivers qtMenu_tele.py\""
