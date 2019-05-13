import argparse
import numpy as np
import cv2

# global vars
WIDTH = 1200
HEIGHT = 1600
OUTPUT_PATH = './output'

# read user input
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,	help="path to the input image")
ap.add_argument("-d", "--debug", required=False, help="show debug messages")
args = vars(ap.parse_args())
image_path = args["image"]
debug_on = args["debug"].lower() == 'true' if args["debug"] else False

if (debug_on):
    print("Debug is enabled.")

# read original image into an array
orig_image = cv2.imread(image_path)

# resize image. Full size image will have too much details and noise
# resizing the image helps the detection of circles and other shapes
image = cv2.resize(orig_image, (WIDTH, HEIGHT))

# apply filters to help the detection process
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred,127,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C)[1]
edged = cv2.Canny(thresh, 75, 200)

img = cv2.imread(image_path,0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=10,maxRadius=30) 
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    avg = np.mean(img[i[1]-10:i[1]+10,i[0]-10:i[0]+10])
    if avg and avg < 100:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

# display the original image after applying the filter
# used for debugging
if (debug_on):
    print(circles)
    cv2.imwrite(OUTPUT_PATH + '/thresh.png', cimg)
    cv2.imshow("Original Image", cv2.resize(cimg, (600, 800)))
    cv2.waitKey(0)

