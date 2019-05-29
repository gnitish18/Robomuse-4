#!/usr/bin/env python
#pocketsphinx speech recognition engine with wxwidget application
#Library imports for Speech Recognition,wxwidget(GUI), ROS Node

import wx
import speech_recognition as sr
import os

from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

import rospy
from geometry_msgs.msg import PoseStamped

# ROS Node Initialization

pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=5)
rospy.init_node('menu', anonymous=True)

""" Location 1 - LHC1 """
pose1 = PoseStamped()

pose1.header.frame_id = "map"

pose1.pose.position.x = -0.533
pose1.pose.position.y = 0.0
pose1.pose.position.z = 0.0

pose1.pose.orientation.x = 0.0
pose1.pose.orientation.y = 0.0
pose1.pose.orientation.z = 0.0
pose1.pose.orientation.w = 1.0

""" Location 2- LHC2 """
pose2 = PoseStamped()

pose2.header.frame_id = "map"

pose2.pose.position.x = -3.04
pose2.pose.position.y = 2.56
pose2.pose.position.z = 0.0

pose2.pose.orientation.x = 0.0
pose2.pose.orientation.y = 0.0
pose2.pose.orientation.z = 0.0
pose2.pose.orientation.w = 1.0

""" Location 3- LHC3 """
pose3 = PoseStamped()

pose3.header.frame_id = "map"

pose3.pose.position.x = 1.31
pose3.pose.position.y = 0.545
pose3.pose.position.z = 0.0

pose3.pose.orientation.x = 0.0
pose3.pose.orientation.y = 0.0
pose3.pose.orientation.z = 0.0
pose3.pose.orientation.w = 1.0


""" Definition for Speech Recognition Parameters"""

MODELDIR = "/usr/local/share/pocketsphinx/model"
DATADIR = "/usr/local/share/pocketsphinx"
MYDIR = "/home/subbu/Documents/TAR0717"

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MYDIR, '0717.lm'))
config.set_string('-dict', path.join(MYDIR, '0717.dic'))
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

import pyaudio

"""End of Speech reCog parameters"""
"""Start Of GUI Parameters"""

class Menu(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, size=(300,400), title='Robomuse') #300,220

        self.panel = wx.Panel(self, wx.ID_ANY)

        title = wx.StaticText(self.panel, wx.ID_ANY, '       Welcome to AIR 2017.\nPlease Select a Destination')

        btn1 = wx.Button(self.panel, wx.ID_ANY, 'LHC1')
        btn2 = wx.Button(self.panel, wx.ID_ANY, 'LHC2')
        btn3 = wx.Button(self.panel, wx.ID_ANY, 'LHC3')
        btn4 = wx.Button(self.panel, wx.ID_ANY, 'Voice Commands')

        self.Bind(wx.EVT_BUTTON, self.onclkbtn1, btn1)
        self.Bind(wx.EVT_BUTTON, self.onclkbtn2, btn2)
        self.Bind(wx.EVT_BUTTON, self.onclkbtn3, btn3)
        self.Bind(wx.EVT_BUTTON, self.onclkbtn4, btn4)

        topSizer    = wx.BoxSizer(wx.VERTICAL)
        titleSizer  = wx.BoxSizer(wx.HORIZONTAL)
        btn1Sizer   = wx.BoxSizer(wx.HORIZONTAL)
        btn2Sizer   = wx.BoxSizer(wx.HORIZONTAL)
        btn3Sizer   = wx.BoxSizer(wx.HORIZONTAL)
        btn4Sizer   = wx.BoxSizer(wx.HORIZONTAL)

        titleSizer.Add(title, 0, wx.ALL, 5)
        btn1Sizer.Add(btn1, 1, wx.ALL, 5)
        btn2Sizer.Add(btn2, 1, wx.ALL, 5)
        btn3Sizer.Add(btn3, 1, wx.ALL, 5)
        btn4Sizer.Add(btn4, 1, wx.ALL, 5)

        topSizer.Add(titleSizer, 0, wx.CENTER)
        topSizer.Add(wx.StaticLine(self.panel,), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btn1Sizer, 1, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btn2Sizer, 1, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btn3Sizer, 1, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btn4Sizer, 1, wx.ALL|wx.EXPAND, 5)

        self.panel.SetSizer(topSizer)
        self.SetPosition((303,283))
#        topSizer.Fit(self)

    def onclkbtn1(self, event):
        print 'btn1'
        pub.publish(pose1)
    def onclkbtn2(self, event):
        print 'btn2'
        pub.publish(pose2)
    def onclkbtn3(self, event):
        print 'btn3'
        pub.publish(pose3)
    def onclkbtn4(self, event):

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
                        if(inOpt=="LECTURE HALL COMPLEX ROOM NUMBER ONE"):
                            print "okay ... breaking"
                            pub.publish(pose1)
                            break
                        elif(inOpt=="LECTURE HALL COMPLEX ROOM NUMBER TWO"):
                            pub.publish(pose2)
                            break
                        elif(inOpt=="LECTURE HALL COMPLEX ROOM NUMBER THREE"):
                            pub.publish(pose3)
                            break
                        else:
                            print "Can you repeat option ?"
                            decoder.start_utt()
            else:
                break

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Menu().Show()
    app.MainLoop()
