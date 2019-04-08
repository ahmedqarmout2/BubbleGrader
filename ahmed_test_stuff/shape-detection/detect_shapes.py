# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import numpy as np
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
image = cv2.resize(image, (1200, 1600)) 
#resized = imutils.resize(image, width=600)
#ratio = image.shape[0] / float(resized.shape[0])
resized = image
ratio = 1

# convert the resized image to grayscale, blur it slightly,
# and threshold it
#gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
#blurred = cv2.GaussianBlur(gray, (1, 1), 0)
#thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.Canny(blurred, 75, 200)
cv2.imshow("Original", thresh)

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

shapesX = []
shapesY = []
shapes = {}

def isOkDistance(cX, cY):
	for i in range(len(shapesX)):
		icx = shapesX[i]
		icy = shapesY[i]
		if (abs(icx - cX) < 20) and (abs(icy - cY) < 20):
			return False
	return True

counterz = 0

# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)

	if (M["m00"] == 0):
		continue
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)

	if shape == "circle" and isOkDistance(cX, cY): # and isOkDistance(cX, cY):
		(x,y),radius = cv2.minEnclosingCircle(c)
		shapesX.append(cX)
		shapesY.append(cY)
		shapes[(cX, cY)] = shape

		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)
		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)
	
	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	#c = c.astype("float")
	#c *= ratio
	#c = c.astype("int")
		if float(total) > 200 and radius > 10:
			continue
			# print(shape, cX, cY, float(total), (x,y), radius)
			# cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
			#cv2.circle(image, (int(x),int(y)), int(radius), (0,255,0),2)
		if float(total) > 80 and radius < 20 and radius > 10:
			counterz += 1
			print(shape, cX, cY, float(total), (x,y), radius)
			cv2.circle(image, (int(x),int(y)), int(radius), (0,255,0),2)
	#cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
	#	0.5, (255, 255, 255), 2)

	# show the output image
cv2.imshow("Image", image)
cv2.waitKey(20000)

print(counterz, shapes)
