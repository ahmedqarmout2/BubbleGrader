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
orig_image = cv2.imread(args["image"])
# image = cv2.convertScaleAbs(orig_image, alpha=2.2, beta=50)
image = cv2.resize(orig_image, (1200, 1600))
# img_bin = cv2.threshold(cv2.cvtColor(cv2.GaussianBlur(image, (5, 5), 0), cv2.COLOR_BGR2GRAY),127,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
# cv2.imshow("Image2", img_bin)

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
# blurred = cv2.threshold(cv2.cvtColor(cv2.GaussianBlur(image, (5, 5), 0), cv2.COLOR_BGR2GRAY),127,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
# cv2.imshow("Image2", img_bin)
edged = cv2.threshold(blurred,127,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
thresh = cv2.Canny(edged, 75, 200)
cv2.imwrite('./uploads/thresh.png', thresh)
cv2.imshow("Original", cv2.resize(thresh, (600, 800)))

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

locationOfCircles = [[{"x":0,"y":12},{"x":20,"y":12},{"x":40,"y":12},{"x":60,"y":12},{"x":80,"y":12},{"x":100,"y":12},{"x":120,"y":12},{"x":140,"y":12},{"x":160,"y":12},{"x":180,"y":12},{"x":0,"y":32},{"x":20,"y":32},{"x":40,"y":32},{"x":60,"y":32},{"x":80,"y":32},{"x":100,"y":32},{"x":120,"y":32},{"x":140,"y":32},{"x":160,"y":32},{"x":180,"y":32}],[{"x":0,"y":60},{"x":20,"y":60},{"x":40,"y":60},{"x":60,"y":60},{"x":80,"y":60},{"x":100,"y":60},{"x":120,"y":60},{"x":140,"y":60},{"x":160,"y":60},{"x":180,"y":60},{"x":0,"y":80},{"x":20,"y":80},{"x":40,"y":80},{"x":60,"y":80},{"x":80,"y":80},{"x":100,"y":80},{"x":120,"y":80},{"x":140,"y":80},{"x":160,"y":80},{"x":180,"y":80}],[{"x":0,"y":108},{"x":20,"y":108},{"x":40,"y":108},{"x":60,"y":108},{"x":80,"y":108},{"x":100,"y":108},{"x":120,"y":108},{"x":140,"y":108},{"x":160,"y":108},{"x":180,"y":108},{"x":0,"y":128},{"x":20,"y":128},{"x":40,"y":128},{"x":60,"y":128},{"x":80,"y":128},{"x":100,"y":128},{"x":120,"y":128},{"x":140,"y":128},{"x":160,"y":128},{"x":180,"y":128}],[{"x":0,"y":156},{"x":20,"y":156},{"x":40,"y":156},{"x":60,"y":156},{"x":80,"y":156},{"x":100,"y":156},{"x":120,"y":156},{"x":140,"y":156},{"x":160,"y":156},{"x":180,"y":156},{"x":0,"y":176},{"x":20,"y":176},{"x":40,"y":176},{"x":60,"y":176},{"x":80,"y":176},{"x":100,"y":176},{"x":120,"y":176},{"x":140,"y":176},{"x":160,"y":176},{"x":180,"y":176}],[{"x":0,"y":204},{"x":20,"y":204},{"x":40,"y":204},{"x":60,"y":204},{"x":80,"y":204},{"x":100,"y":204},{"x":120,"y":204},{"x":140,"y":204},{"x":160,"y":204},{"x":180,"y":204},{"x":0,"y":224},{"x":20,"y":224},{"x":40,"y":224},{"x":60,"y":224},{"x":80,"y":224},{"x":100,"y":224},{"x":120,"y":224},{"x":140,"y":224},{"x":160,"y":224},{"x":180,"y":224}],[{"x":0,"y":252},{"x":20,"y":252},{"x":40,"y":252},{"x":60,"y":252},{"x":80,"y":252},{"x":100,"y":252},{"x":120,"y":252},{"x":140,"y":252},{"x":160,"y":252},{"x":180,"y":252},{"x":0,"y":272},{"x":20,"y":272},{"x":40,"y":272},{"x":60,"y":272},{"x":80,"y":272},{"x":100,"y":272},{"x":120,"y":272},{"x":140,"y":272},{"x":160,"y":272},{"x":180,"y":272}],[{"x":0,"y":300},{"x":20,"y":300},{"x":40,"y":300},{"x":60,"y":300},{"x":80,"y":300},{"x":100,"y":300},{"x":120,"y":300},{"x":140,"y":300},{"x":160,"y":300},{"x":180,"y":300},{"x":0,"y":320},{"x":20,"y":320},{"x":40,"y":320},{"x":60,"y":320},{"x":80,"y":320},{"x":100,"y":320},{"x":120,"y":320},{"x":140,"y":320},{"x":160,"y":320},{"x":180,"y":320}]]

sqrYs = []
sqrXs = []

sqrY = -1
sqrX = -1

# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)

	if (M["m00"] == 0):
		continue
	cX = int((M["m10"] / M["m00"]) * ratio) - 24
	cY = int((M["m01"] / M["m00"]) * ratio) + 34
	shape = sd.detect(c)

	if shape == "square":
		# for i in sqrXs:
		# 	if cX >= i-5 and cX <= i+5:
		# 		sqrX = cX
		for i in range(len(sqrYs)):
			dotY = sqrYs[i]
			if cY >= dotY-5 and cY <= dotY+5:
				if cX < sqrX or sqrX == -1:
					sqrX = cX
					sqrY = cY

		cv2.drawContours(image, [c], -1, (255, 0, 0), 2)
		sqrYs.append(cY)
		sqrXs.append(cX)

# print(sqrYs, sqrXs)

# loop over the contours
for c in cnts:
	# compute the center of the contour, then detect the name of the
	# shape using only the contour
	M = cv2.moments(c)

	cv2.drawContours(image, [c], -1, (0, 0, 255), 2)

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

		if radius > 8:
			cv2.circle(image, (int(x),int(y)), int(radius), (0,255,0),2)

		if float(total) > 100 and radius > 8:
			continue
			# print(shape, cX, cY, float(total), (x,y), radius)
			# cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
			# cv2.circle(image, (int(x),int(y)), int(radius), (0,255,0),2)
		if float(total) > 80 and radius < 16 and radius > 8:
			counterz += 1
			# print(shape, cX, cY, float(total), (x,y), radius)
			# cv2.circle(image, (int(x),int(y)), int(radius), (0,255,0),2)

			comX = int((x-sqrX)/1.8)-8
			comY = int((y-sqrY)/1.8)+12
			print(comX, comY)

			cv2.circle(image, (int(comX), int(comY)), int(radius), (0,0,255),2)

			for i in range(len(locationOfCircles)):
				listOfOptions = locationOfCircles[i]
				for j in range(len(listOfOptions)):
					option = listOfOptions[j]

					radiusF = (radius/8)

					tempY = int(option['y'])
					tempX = int(option['x'] - 2*j)
					
					# print((option['x'], option['y']), (tempX, tempY), (comX, comY), radiusF)
					# print((radius/8))
					# print((tempX, tempY), (int(x), int(y)), (sqrX, sqrY))
					if comX >= tempX-8 and comX <= tempX+8 and comY >= tempY-8 and comY <= tempY+8:
						# continue
						print("Found something at: ", (tempX, tempY), "Q: ", i+1, "I: ",j)
						# cv2.circle(image, (int(x),int(y)), int(radius), (0,255,0),2)
	#cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
	#	0.5, (255, 255, 255), 2)

	# show the output image

print((sqrX, sqrY), (locationOfCircles[0][1]['x'], locationOfCircles[0][1]['y']))
print((sqrX, sqrY), (locationOfCircles[1][0]['x'], locationOfCircles[1][0]['y']))
print((sqrX, sqrY), (locationOfCircles[0][16]['x'], locationOfCircles[0][16]['y']))
print((sqrX, sqrY), (locationOfCircles[1][14]['x'], locationOfCircles[1][14]['y']))

cv2.circle(image, (sqrX, sqrY), int(1), (0,0,255),2)

# new_image = cv2.convertScaleAbs(orig_image, alpha=1.2, beta=40)
cv2.imwrite('./uploads/result.png', cv2.resize(image, (600, 800)))
cv2.imshow("Image", cv2.resize(image, (600, 800)))
cv2.waitKey(0)

#print(counterz, shapes)
