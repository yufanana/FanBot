#!/usr/bin/env python

import numpy as np
import cv2

def filter_color(rgb_image, lower_bound_color, upper_bound_color):
    #convert the image into the HSV color space
    hsv_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2HSV)

    #define a mask using the lower and upper bounds of the yellow color 
    mask = cv2.inRange(hsv_image, lower_bound_color, upper_bound_color)

    return mask

def getContours(mask):      
    contours, hierarchy = cv2.findContours(mask.copy(), 
                                            cv2.RETR_EXTERNAL,
	                                        cv2.CHAIN_APPROX_SIMPLE)
    return contours


def draw_ball_contour(binary_image, rgb_image, contours):
    
    max_area = 0
    max_c = None
    for c in contours:
        area = cv2.contourArea(c)

        if area > max_area:
            max_area = area
            max_c = c
        # # only draw contours that are sufficiently large
        if (area>3000):
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            cv2.drawContours(rgb_image, [c], -1, (150,250,150), 2)
            #cx, cy = get_contour_center(c)
            #cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),2)
            #print ("Area: {}".format(area))

    # draw circle for the largest contour
    ((x, y), radius) = cv2.minEnclosingCircle(max_c)
    cv2.drawContours(rgb_image, [c], -1, (150,250,150), 2)
    cx, cy = get_contour_center(max_c)
    cv2.circle(rgb_image, (cx,cy),(int)(radius),(0,0,255),2)

    #print ("number of contours: {}".format(len(contours)))
    cv2.imshow("RGB Image Contours",rgb_image)

def get_contour_center(contour):
    M = cv2.moments(contour)
    cx=-1
    cy=-1
    if (M['m00']!=0):
        cx= int(M['m10']/M['m00'])
        cy= int(M['m01']/M['m00'])
    return cx, cy

def on_trackbar(val):
    pass

def createTrackBars():
    cv2.namedWindow("TrackedBars")
    cv2.resizeWindow("TrackedBars", 640, 100)
    cv2.createTrackbar("Hue Min", "TrackedBars", 40, 179, on_trackbar)
    cv2.createTrackbar("Hue Max", "TrackedBars", 65, 179, on_trackbar)
    cv2.createTrackbar("Sat Min", "TrackedBars", 120, 255, on_trackbar)
    cv2.createTrackbar("Sat Max", "TrackedBars", 255, 255, on_trackbar)
    cv2.createTrackbar("Val Min", "TrackedBars", 50, 255, on_trackbar)
    cv2.createTrackbar("Val Max", "TrackedBars", 255, 255, on_trackbar)

def getTrackBarValues():

    hue_min = cv2.getTrackbarPos("Hue Min", "TrackedBars")
    hue_max = cv2.getTrackbarPos("Hue Max", "TrackedBars")
    sat_min = cv2.getTrackbarPos("Sat Min", "TrackedBars")
    sat_max = cv2.getTrackbarPos("Sat Max", "TrackedBars")
    val_min = cv2.getTrackbarPos("Val Min", "TrackedBars")
    val_max = cv2.getTrackbarPos("Val Max", "TrackedBars")

    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])
    return lower,upper

def main():
    # create capture object from file
    video_capture = cv2.VideoCapture('videos/ball_video1.mp4')
    createTrackBars()

    frame_counter = 0
    while(True):
        frame_counter += 1
        ret, frame = video_capture.read()
        lower,upper = getTrackBarValues()
        
        # loop the video
        if frame_counter == video_capture.get(cv2.CAP_PROP_FRAME_COUNT):
            frame_counter = 0
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # #reached end of video, exit program
        # if ret == False: 
        #     print('ret is False')
        #     break

        waitKey = cv2.waitKey(1) & 0xFF
        if waitKey == ord('r'):
            frame_counter = 0
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            print('R pressed. Restarting...')

        elif waitKey == ord('q'):
            print('Q pressed. Exiting...')
            break

        # ball detection algorithm
        # yellowLower = (30, 150, 100)
        # yellowUpper = (50, 255, 255)
        # binary_frame_mask = filter_color(frame, yellowLower, yellowUpper)
        binary_frame_mask = filter_color(frame, lower, upper)
        contours = getContours(binary_frame_mask)
        draw_ball_contour(binary_frame_mask, frame,contours)

    lower,upper = getTrackBarValues()
    print("lower: {}, upper: {}".format(lower,upper))
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()