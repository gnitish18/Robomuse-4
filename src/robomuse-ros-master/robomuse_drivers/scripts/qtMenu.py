#!/usr/bin/env python

#pocketsphinx speech recognition engine with wxwidget application
#Library imports for Speech Recognition,wxwidget(GUI), ROS Node

import wx
import speech_recognition as sr
import os

from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

#imports for faceRecog
import numpy as np
import cv2

#import pyqt requirements
import sys
from PyQt4 import QtCore, QtGui, uic

#import pyttsx
import pyttsx

#importing ros requirements
import rospy
from geometry_msgs.msg import PoseStamped

pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=5)
rospy.init_node('menu', anonymous=True)

""" Location 1 - Room1 """
pose1 = PoseStamped()

pose1.header.frame_id = "map"

pose1.pose.position.x = 3.78
pose1.pose.position.y = 0.788
pose1.pose.position.z = 0.0

pose1.pose.orientation.x = 0.0
pose1.pose.orientation.y = 0.0
pose1.pose.orientation.z = 0.0
pose1.pose.orientation.w = 1.0

""" Location 2- Room2 """
pose2 = PoseStamped()

pose2.header.frame_id = "map"

pose2.pose.position.x =  0.815#1.01
pose2.pose.position.y =  -0.122#2.33
pose2.pose.position.z = 0.0

pose2.pose.orientation.x = 0.0
pose2.pose.orientation.y = 0.0
pose2.pose.orientation.z = 0.0
pose2.pose.orientation.w = 1.0

""" Location 3- Room3 """
pose3 = PoseStamped()

pose3.header.frame_id = "map"

pose3.pose.position.x = 1.01
pose3.pose.position.y = 2.33
pose3.pose.position.z = 0.0

pose3.pose.orientation.x = 0.0
pose3.pose.orientation.y = 0.0
pose3.pose.orientation.z = 0.0
pose3.pose.orientation.w = 1.0

#End of location Definition
#Definition for Speech Recognition Parameters

MODELDIR = "/usr/local/share/pocketsphinx/model"
DATADIR = "/usr/local/share/pocketsphinx"
MYDIR = "/home/subbu/Documents/TAR7358"

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MYDIR, '7358.lm'))
config.set_string('-dict', path.join(MYDIR, '7358.dic'))
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

import pyaudio

#End of Speech reCog parameters

qtCreatorFile = "/home/subbu/catkin_ws/src/robomuse-ros-master/robomuse_drivers/scripts/robomuse.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.uno.clicked.connect(self.func1)
        self.dos.clicked.connect(self.func2)
        self.tres.clicked.connect(self.func3)
        self.quat.clicked.connect(self.func4)
        self.showMaximized()
        engine = pyttsx.init()
        volume = engine.getProperty('rate')
        engine.setProperty('rate', 150)
        engine.say('Hello, Welcome to Advances in Robotics 2017. Where would you like to go?')
        engine.runAndWait()

    def func1(self):
        print "unos mamos"
        pub.publish(pose1)
    def func2(self):
        print "dos mamos"
        pub.publish(pose2)
    def func3(self):
        print "tres mamos"
        pub.publish(pose3)
    def func4(self):
        print "quat mamos"
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        stream.start_stream()

        in_speech_bf = False
        decoder.start_utt()

        while True:
            buf = stream.read(1024)
            if buf:
                decoder.process_raw(buf, False, False)
                if decoder.get_in_speech() != in_speech_bf:
                    in_speech_bf = decoder.get_in_speech()
                    if not in_speech_bf:
                        decoder.end_utt()
                        inOpt =  decoder.hyp().hypstr
                        print 'Result:',inOpt
                        if(inOpt=="LOCATION ONE"):
                            print "okay ... breaking"
                            pub.publish(pose1)
                            break
                        elif(inOpt=="LOCATION TWO"):
                            pub.publish(pose2)
                            break
                        elif(inOpt=="LOCATION THREE"):
                            pub.publish(pose3)
                            break
                        else:
                            print "Can you repeat option ?"
                            decoder.start_utt()
            else:
                break



if __name__ == "__main__":

    face_cascade = cv2.CascadeClassifier('/home/subbu/opencv-3.1.0/data/haarcascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    flag = 1
    while(True and flag):
        ret, img= cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            flag = 0
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]

        cv2.imshow('PLEASE STAND IN FRONT',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
