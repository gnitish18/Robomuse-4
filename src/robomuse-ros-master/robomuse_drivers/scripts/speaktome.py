import time

import speech_recognition as sr

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import subprocess

xpos = [3.00,0.00]
i = 0


def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response["transcription"]

def movebase_client():

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()
    global i
    global xpos
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = xpos[i]
    i = i+1
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()


if __name__ == "__main__":

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    print sr.Microphone.list_microphone_names()

    

    # show instructions and wait 3 seconds before starting the game
    time.sleep(3)
    while(True):
    	guess = recognize_speech_from_mic(recognizer, microphone)
	if guess == 'goal':
		break
	print guess
    print 'You said goal'
    try:
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
            subprocess.call("./sayhello.sh", shell=True)
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
    rospy.sleep(3)
    while(True):
    	guess = recognize_speech_from_mic(recognizer, microphone)
	if guess == 'go to start':
		break
	print guess
    print 'You said to go to start'
    try:
        rospy.init_node('movebase_client_py')
        result = movebase_client()
        if result:
            rospy.loginfo("Goal execution done!")
            subprocess.call("./sayhello.sh", shell=True)
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")


 

