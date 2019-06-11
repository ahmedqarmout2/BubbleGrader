from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import numpy as np
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

orig_image = cv2.imread(args["image"])
image = cv2.resize(orig_image, (1200, 1600))

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#thresh = cv2.threshold(blurred,127,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
edged = cv2.Canny(blurred, 75, 200)
cv2.imwrite('./uploads/thresh.png', edged)
cv2.imshow("Original", cv2.resize(edged, (600, 800)))

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()

rectso = []
for c in cnts:
	M = cv2.moments(c)

	if (M["m00"] == 0):
		continue

	#cv2.drawContours(image, [c], -1, (255, 0, 0), -1)

	cX = int((M["m10"] / M["m00"]))
	cY = int((M["m01"] / M["m00"]))
	shape = sd.detect(c)

	if shape == "rectangle" or shape == "square":
		x,y,w,h = cv2.boundingRect(c)
		if h > 20 and h < 40 and w > 20 and w < 40:
			rectso.append((x, y, w, h))
			cv2.drawContours(image, [c], -1, (255, 0, 0), -1)
			cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
			print(shape, cX, cY)

if len(rectso) == 4:
	top_two_points = []
	bottom_two_points = []
	lowest_y = 12000
	for p in rectso:
		if p[1] < lowest_y:
			lowest_y = p[1]

	for p in rectso:
		if p[1] < lowest_y+100 and p[1] > lowest_y-100:
			top_two_points.append(p)
		else:
			bottom_two_points.append(p)

	if top_two_points[0][0] > top_two_points[1][0]:
		top_two_points[0], top_two_points[1] = top_two_points[1], top_two_points[0]

	if bottom_two_points[0][0] > bottom_two_points[1][0]:
		bottom_two_points[0], bottom_two_points[1] = bottom_two_points[1], bottom_two_points[0]

	print(top_two_points)
	print(bottom_two_points)

	p0 = (top_two_points[0][0] + top_two_points[0][2], top_two_points[0][1])
	p2 = (top_two_points[1][0], top_two_points[1][1])
	p1 = (bottom_two_points[0][0] + bottom_two_points[0][2], bottom_two_points[0][1] + bottom_two_points[0][3])
	p3 = (bottom_two_points[1][0], bottom_two_points[1][1] + bottom_two_points[1][3])

	print(p0, p1, p2, p3)

	cv2.circle(image, (int(p0[0]),int(p0[1])), int(4), (0,0,255))
	cv2.circle(image, (int(p1[0]),int(p1[1])), int(4), (0,0,255))
	cv2.circle(image, (int(p2[0]),int(p2[1])), int(4), (0,0,255))
	cv2.circle(image, (int(p3[0]),int(p3[1])), int(4), (0,0,255))

	pts1 = np.float32([[p0[0], p0[1]], [p1[0], p1[1]], [p2[0], p2[1]], [p3[0], p3[1]]])
	pts2 = np.float32([[0, 0], [0, 430], [420, 0], [420, 430]])
	M, status = cv2.findHomography(pts1, pts2)
	dst = cv2.warpPerspective(image, M, (430, 420))

	dst2 = dst
	dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
	dst = cv2.GaussianBlur(dst, (5, 5), 0)
	dst = cv2.threshold(dst,127,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]

	cv2.imshow("New Image", dst)

	studentNumber = '_'*10
	def_x = 18
	def_y = 10
	counter_x = def_x
	counter_y = def_y
	for i in range(10):
		counter_x = def_x
		counter_y += 18.5
		for j in range(10):
			avg = np.mean(dst[int(counter_y)-4:int(counter_y)+8,int(counter_x)-4:int(counter_x)+8])
			if avg and avg > 200:
				print('row:', i, 'col:', j, 'value:', avg)
				studentNumber = studentNumber[:j] + str(i) + studentNumber[j+1:]
				cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,0,255))
			else:
				cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,255,0))
			cv2.rectangle(dst2,(int(counter_x)-4,int(counter_y)-4),(int(counter_x)+8,int(counter_y)+8),(255,0,0))
			counter_x += 19

	print('Student Number: ', studentNumber)

	q1Number = '_'*2
	def_x = 18
	def_y = 210
	counter_x = def_x
	counter_y = def_y
	for i in range(2):
		counter_x = def_x
		counter_y += 18.5
		for j in range(10):
			avg = np.mean(dst[int(counter_y)-4:int(counter_y)+8,int(counter_x)-4:int(counter_x)+8])
			if avg and avg > 200:
				print('row:', i, 'col:', j, 'value:', avg)
				q1Number = q1Number[:i] + str(j) + q1Number[i+1:]
				cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,0,255))
			else:
				cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,255,0))
			cv2.rectangle(dst2,(int(counter_x)-4,int(counter_y)-4),(int(counter_x)+8,int(counter_y)+8),(255,0,0))
			counter_x += 19

	print('Q1: ', q1Number)

	q2Number = '_'*2
	def_x = 18
	def_y = 250
	counter_x = def_x
	counter_y = def_y
	for i in range(2):
		counter_x = def_x
		counter_y += 18.5
		for j in range(10):
			avg = np.mean(dst[int(counter_y)-4:int(counter_y)+8,int(counter_x)-4:int(counter_x)+8])
			if avg and avg > 200:
				print('row:', i, 'col:', j, 'value:', avg)
				q2Number = q2Number[:i] + str(j) + q2Number[i+1:]
				cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,0,255))
			else:
				cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,255,0))
			cv2.rectangle(dst2,(int(counter_x)-4,int(counter_y)-4),(int(counter_x)+8,int(counter_y)+8),(255,0,0))
			counter_x += 19

	print('Q2: ', q2Number)

	def_x = 18
	def_y = 290
	counter_x = def_x
	counter_y = def_y
	for i in range(2):
		counter_x = def_x
		counter_y += 18.5
		for j in range(10):
			avg = np.mean(dst[int(counter_y)-4:int(counter_y)+8,int(counter_x)-4:int(counter_x)+8])
			if avg and avg > 200:
				print('row:', i, 'col:', j, 'value:', avg)
				cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,0,255))
			else:
				cv2.circle(dst2, (int(counter_x),int(counter_y)), int(6), (0,255,0))
			cv2.rectangle(dst2,(int(counter_x)-4,int(counter_y)-4),(int(counter_x)+8,int(counter_y)+8),(255,0,0))
			counter_x += 19

	cv2.imshow("New Image 2", dst2)

cv2.imwrite('./uploads/result.png', cv2.resize(image, (600, 800)))
cv2.imshow("Image", cv2.resize(image, (600, 800)))
cv2.waitKey(0)