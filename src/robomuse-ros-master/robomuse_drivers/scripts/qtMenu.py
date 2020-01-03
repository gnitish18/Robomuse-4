#!/usr/bin/env python

#pocketsphinx speech recognition engine with wxwidget application
#Library imports for Speech Recognition,wxwidget(GUI), ROS Node

import wx
import os
import glob

from os import environ, path

#imports for faceRecog
import numpy as np
import cv2

#import pyqt requirements
import sys
from PyQt4 import QtCore, QtGui, uic

#importing ros requirements
import rospy
import subprocess
from geometry_msgs.msg import PoseStamped

rospy.init_node('menu', anonymous=True)

#End of location Definition
#Definition for Speech Recognition Parameters

#End of Speech reCog parameters

"""for file in glob.iglob('robomuse.ui', recursive=True):
    qtCreatorFile = file
    print(qtCreatorFile)
"""
qtCreatorFile = "/home/nitish/catkin_ws/src/robomuse-ros-master/robomuse_drivers/scripts/robomuse.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):

    def func1(self):
        subprocess.call("shellscripts/./nav.sh", shell=True)

    def func2(self):
        subprocess.call("shellscripts/./exploremap.sh", shell=True)

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.uno.clicked.connect(self.func1)
        self.map.clicked.connect(self.func2)

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
