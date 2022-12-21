#runnerCode python pyimagesearch.py --video xfile.mp4 


# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import math

"""
    frame = frame[:,180:1790]  # masanın ucundan fileye 130cm ölçüldü, bu da 1610 pixel'e denk geliyor
"""
auto = 1
m_pix_ratio = 1.3 / 1610  
secBetweenFrames = 1 / 60 

# return m/s
def MeasureSpeed(prevLocation, currentLocation):
    return math.sqrt(
        (prevLocation[0]-currentLocation[0])**2 + (prevLocation[1]-currentLocation[1])**2) *m_pix_ratio / secBetweenFrames

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

speed = 0
prevLocation=[0,0]

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (5, 142, 204-80)#greenLower = (29, 86, 6)
# (15,58,87.8)
greenUpper = (45, 178+40 , 255-55)#greenUpper = (64, 255, 255) 


pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=0).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
	# grab the current frame
    frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
    frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
    if frame is None:
        break
    
    """
    # block some stuff in case unwanted orange color exist
    frame = frame[:,200:1100]
    y= 580
    for x in range(y):
        frame[x ,0:math.floor( (y-x)/1.6 ),:]=0
    """
    frame[0:500,0:180] = 0

	
    # resize the frame, blur it, and convert it to the HSV
	# color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
	# only proceed if at least one contour was found
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        
        speed = MeasureSpeed(prevLocation,[x,y])
        prevLocation = [x,y]

        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
        if radius > 5:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            cv2.putText(frame, str(round(speed,2)) + " m/s", (10,30), cv2.FONT_HERSHEY_SIMPLEX , 1.0, (0,0,255), 1 )
	# update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
        if pts[i - 1] is None or pts[i] is None:
            continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 1) #2.5
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(auto) & 0xFF
	# if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
    vs.stop()
# otherwise, release the camera
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()