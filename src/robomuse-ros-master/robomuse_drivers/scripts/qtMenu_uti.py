#!/usr/bin/env python

#pocketsphinx speech recognition engine with wxwidget application
#Library imports for Speech Recognition,wxwidget(GUI), ROS Node

import wx
import os

from os import environ, path

#imports for faceRecog
import numpy as np
import cv2

#import pyqt requirements
import sys
import subprocess
from PyQt4 import QtCore, QtGui, uic

#importing ros requirements
import rospy
from geometry_msgs.msg import PoseStamped

rospy.init_node('menu', anonymous=True)

qtCreatorFile = "/home/nitish/catkin_ws/src/robomuse-ros-master/robomuse_drivers/scripts/robomuse_uti.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):

    def func1(self):
        subprocess.call("shellscripts/./aroundlhc.sh", shell=True)
    
    def func2(self):
        subprocess.call("shellscripts/./teletoauto.sh", shell=True)
    
    def func3(self):
        subprocess.call("shellscripts/./kill.sh", shell=True)
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.aut.clicked.connect(self.func1)
        self.tel.clicked.connect(self.func2)
        self.off.clicked.connect(self.func3)

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
