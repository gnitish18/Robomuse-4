gnome-terminal --tab -e "bash -c \"cd ~/Documents/aio\ rem/ && java -jar AioRemoteDesktop3.5.0.jar\"" \
--tab -e "bash -c \"roslaunch robomuse_drivers robomuse_depth_reg.launch\"" \
--tab -e "bash -c \"./telcall.sh\"" \
--tab -e "bash -c \"./odomsee.sh\"" \

