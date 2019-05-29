sleep 10
cd helperScripts
espeak 'Robo Muse initialized'
while :
do
	echo "Press [CTRL+C] to stop.."
	espeak 'Please tell me where to go'
	python lm_test.py
	sleep 1
done


