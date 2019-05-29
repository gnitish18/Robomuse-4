#!/usr/bin/env python 
from pyquaternion import Quaternion as qn
import numpy as np

q1 = qn(1,1,1,1)
q1 = q1.normalised
print q1

q1[2] = 0
q1[3] = 0

q1 = q1.normalised

print q1