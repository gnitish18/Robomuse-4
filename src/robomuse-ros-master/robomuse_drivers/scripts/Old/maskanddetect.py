import cv2
import numpy as np

#cap = cv2.VideoCapture(0)

#while(1):

    # Take each frame
def detect(frame):
    # frame = cv2.imread('test.png',1)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([0,0,0])
    upper_blue = np.array([255,255,40])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    cv2.imshow("Image windo", mask)
    cv2.waitKey(3)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    count = 0
    cx = 0
    cy = 0
    area_max = 0
    while (count < len(contours)):
        #approx = cv2.approxPolyDP(contours[count],0.01*cv2.arcLength(contours[count],True),True)
        area = cv2.contourArea(contours[count])
        #if (len(approx)==4):# and (area > 1000 and area < 15000)):
        if(area>area_max):
            index = count
            area_max = area
        count += 1
    cv2.drawContours(frame,contours,index,(0,255,0),3)
    print area_max
    M = cv2.moments(contours[index])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    if(area_max>8100 and area_max<9720):
        cx = 0
        cy = 0
    # cv2.imshow('cont',frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return cx,cy
