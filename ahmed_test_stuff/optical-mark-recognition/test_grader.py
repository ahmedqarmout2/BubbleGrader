# USAGE
# python test_grader.py --image images/test_01.png

# import the necessary packages
from imutils.perspective import four_point_transform
from pyimagesearch.shapedetector import ShapeDetector
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to the input image")
args = vars(ap.parse_args())

# define the answer key which maps the question number
# to the correct answer
ANSWER_KEY = {0: 1, 1: 4, 2: 0, 3: 3, 4: 1}

# load the image, convert it to grayscale, blur it
# slightly, then find edges
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(blurred, 75, 200)

# find contours in the edge map, then initialize
# the contour that corresponds to the document
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
docCnt = None

# ensure that at least one contour was found
if len(cnts) > 0:
	# sort the contours according to their size in
	# descending order
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

	# loop over the sorted contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

		# if our approximated contour has four points,
		# then we can assume we have found the paper
		if len(approx) == 4:
			docCnt = approx
			#print('hi')
			break

#print(len(cnts))

# apply a four point perspective transform to both the
# original image and grayscale image to obtain a top-down
# birds eye view of the paper
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))

paper = cv2.resize(paper, (600, 800)) 
warped = cv2.resize(warped, (600, 800)) 

cv2.imwrite('paper.png',paper)
cv2.imwrite('warped.png',warped)

# apply Otsu's thresholding method to binarize the warped
# piece of paper
thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image, then initialize
# the list of contours that correspond to questions
cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST,
	cv2.CHAIN_APPROX_SIMPLE)
#cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
#print(len(cnts))

##########################################
ratio = 1
shapesX = []
shapesY = []
shapes = {}
sd = ShapeDetector()

def isOkDistance(cX, cY):
	for i in range(len(shapesX)):
		icx = shapesX[i]
		icy = shapesY[i]
		if (abs(icx - cX) < 10) and (abs(icy - cY) < 10):
			return False
	return True

# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)
	#if (M["m00"] != 0):
	cX = 1000 if M["m00"] == 0 else int((M["m10"] / M["m00"]) * ratio)
	cY = 1000 if M["m00"] == 0 else int((M["m01"] / M["m00"]) * ratio)
	shape = sd.detect(c)

	if isOkDistance(cX, cY):
		shapesX.append(cX)
		shapesY.append(cY)
		shapes[(cX, cY)] = shape
		#print(shape, cX, cY)
	    #print(cX, cY)
	
	# multiply the contour (x, y)-coordinates by the resize ratio,
	# then draw the contours and the name of the shape on the image
	#c = c.astype("float")
	#c *= ratio
	#c = c.astype("int")
	#cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	#cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
	#	0.5, (255, 255, 255), 2)

	# show the output image
	#cv2.imshow("Image", image)
	#cv2.waitKey(0)

#print(len(shapesX), len(shapesY), shapes)
##########################################
shapesX = []
shapesY = []
shapes = {}

questionCnts = []

def detect(c):
	# initialize the shape name and approximate the contour
	shape = "unidentified"
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	#print(approx)
    # if the shape is a triangle, it will have 3 vertices
	if len(approx) == 3:
		shape = "triangle"
		# if the shape has 4 vertices, it is either a square or
	    # a rectangle
	elif len(approx) == 4:
		# compute the bounding box of the contour and use the
		# bounding box to compute the aspect ratio
		(x, y, w, h) = cv2.boundingRect(approx)
		ar = w / float(h)
		# a square will have an aspect ratio that is approximately
		# equal to one, otherwise, the shape is a rectangle
		shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
		# if the shape is a pentagon, it will have 5 vertices
	elif len(approx) == 5:
		shape = "pentagon"
		# otherwise, we assume the shape is a circle
	elif len(approx) > 5:
		shape = "circle"
	#print(len(approx))
	# return the name of the shape
	return shape

Keys = [182, 208, 233, 261, 286, 312, 338, 364, 391, 418]
Values = [67, 91, 113, 134, 155, 178, 200, 221, 242, 266]
StudentNum = {}


# loop over the contours
for c in cnts:
	# compute the bounding box of the contour, then use the
	# bounding box to derive the aspect ratio
	(x, y, w, h) = cv2.boundingRect(c)
	ar = w / float(h)

	# in order to label the contour as a question, region
	# should be sufficiently wide, sufficiently tall, and
	# have an aspect ratio approximately equal to 1

	if w >= 10 and h >= 10 and w < 30 and h < 30:
		if isOkDistance(x, y):
			shapesX.append(x)
			shapesY.append(y)
			shape = detect(c)
			shapes[(cX, cY)] = shape
			cXX = int(x + w/2)
			cYY = int(y + h/2)
			#print(shape, cXX, cYY)
			for sk in range(len(Keys)):
				k = Keys[sk]
				if cXX <= k + 5 and cXX >= k - 5:
					#print(sk, k)
					for sv in range(len(Values)):
						v = Values[sv]
						if cYY <= v + 5 and cYY >= v - 5:
							if str(sk) in StudentNum:
								StudentNum[str(sk)].append(sv)
							else:
								StudentNum[str(sk)] = [sv]
			questionCnts.append(c)
			color = (0, 255, 0)
			cv2.drawContours(paper, [c], -1, color, 3)

print(StudentNum)
# sort the question contours top-to-bottom, then initialize
# the total number of correct answers
#print(len(questionCnts), shapes)
questionCnts = contours.sort_contours(questionCnts,	method="top-to-bottom")[0]
correct = 0

cv2.imwrite('paper.png',paper)

'''
# each question has 5 possible answers, to loop over the
# question in batches of 5
for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
	# sort the contours for the current question from
	# left to right, then initialize the index of the
	# bubbled answer
	cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
	bubbled = None

	# loop over the sorted contours
	for (j, c) in enumerate(cnts):
		# construct a mask that reveals only the current
		# "bubble" for the question
		mask = np.zeros(thresh.shape, dtype="uint8")
		cv2.drawContours(mask, [c], -1, 255, -1)

		# apply the mask to the thresholded image, then
		# count the number of non-zero pixels in the
		# bubble area
		mask = cv2.bitwise_and(thresh, thresh, mask=mask)
		total = cv2.countNonZero(mask)

		# if the current total has a larger number of total
		# non-zero pixels, then we are examining the currently
		# bubbled-in answer
		if bubbled is None or total > bubbled[0]:
			bubbled = (total, j)

	# initialize the contour color and the index of the
	# *correct* answer
	color = (0, 0, 255)
	k = ANSWER_KEY[q]

	# check to see if the bubbled answer is correct
	if k == bubbled[1]:
		color = (0, 255, 0)
		correct += 1

	# draw the outline of the correct answer on the test
	cv2.drawContours(paper, [cnts[k]], -1, color, 3)

# grab the test taker
score = (correct / 5.0) * 100
print("[INFO] score: {:.2f}%".format(score))
cv2.putText(paper, "{:.2f}%".format(score), (10, 30),
	cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
cv2.imshow("Original", image)
cv2.imshow("Exam", paper)
cv2.waitKey(0)'''
