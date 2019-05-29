# import the necessary packages
import numpy as np
import cv2

def detect(image):
	# convert the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# compute the Scharr gradient magnitude representation of the images
	# in both the x and y direction
	# gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
	# gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)
	gradX = cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=-1)
	gradY = cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=-1)

	# subtract the y-gradient from the x-gradient
	gradient = cv2.subtract(gradX, gradY)
	gradient = cv2.convertScaleAbs(gradient)

	# blur and threshold the image
	blurred = cv2.blur(gradient, (9, 9))
	(_, thresh) = cv2.threshold(blurred, 220, 255, cv2.THRESH_BINARY)
	cv2.imshow("thresh",thresh)
	cv2.waitKey(3)
	# construct a closing kernel and apply it to the thresholded image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

	# perform a series of erosions and dilations
	closed = cv2.erode(closed, None, iterations = 4)
	closed = cv2.dilate(closed, None, iterations = 4)


	# find the contours in the thresholded image
	# cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
	# 	cv2.CHAIN_APPROX_SIMPLE)
	im2, contours, hierarchy = cv2.findContours(closed.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	# if no contours were found, return None
	if len(contours) == 0:
		cx= 0
		cy= 0
	count = 0
	print len(contours)
	area_max = 0
	while(count < len(contours)):
		flag = 1
		area = cv2.contourArea(contours[count])
		if(area > area_max):
			index = count
			area_max = area
		count+=1

	if flag == 1:
		M = cv2.moments(contours[index])
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
	print cx,cy
	cv2.drawContours(image, contours, index, (0,255,0), 3)

	if(cx>310 and cx<330):
		print "ok"
	return cx,cy
