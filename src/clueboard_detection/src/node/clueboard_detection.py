#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import rospy
from std_msgs.msg import Bool
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
# Connor's character recognition
from character_recognition.call_nn import read_board
from score_board_publisher.score_board_publisher import publish_clue


class ClueboardFinder:

    def __init__(self):

        rospy.loginfo("initiating")

        self.pub = rospy.Publisher('/clueboard', Bool, queue_size=1)
        self.rate = rospy.Rate(2)

        self.subscriber = rospy.Subscriber("/selected_camera_feed", Image, self.image_callback)

        self.bridge = CvBridge()

        # Keeps track of whether or not there's a clueboard - True if there is a clueboard
        self.clueboard = False

        # How many frames we go before trying to detect the clueboard
        self.framesbetween = 5 # Obviously change as needed

        # Keep track of how many frames have happened
        self.framecount = 0

        # Initialize normal and filtered contours lists
        self.filtered_contours =[]
        self.contours =[]

        # Tell us which part of the screen to look at
        self.screenfraction = 3

        # Callback function begins here - this tells the node what to do when we receive an image
    def image_callback(self, msg):

        if self.framecount == 0:

            self.frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding= "bgr8")


            self.cropstart = self.frame.shape[0] // self.screenfraction
            self.cropend = self.frame.shape[0]

        # Increment the frame count
        self.framecount += 1

        # Checks if enough frames have passed
        if self.framecount % self.framesbetween == 0:
            # Puts the image from the feed into opencv format
            self.frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding= "bgr8")

            self.frame = self.frame[self.cropstart:self.cropend, :]

            self.contours = self.MaskAndFindContours_HSV()
            self.filtered_contours = self.FilterContoursByArea()

            if len(self.filtered_contours) >= 1:
                self.clueboard = True
                self.framesbetween = 1
            else:
                self.framesbetween = 5
                self.clueboard = False

            self.changeClueboard()

            self.perspectiveTransform()

            self.readClueboardandPublish()



        # Update the clueboard thing


    def MaskAndFindContours_HSV(self):
        # Check if the image was loaded successfully
        if self.frame is None:
            print(f"Error: Could not load image. Please ensure the file exists and the path is correct.")
            return [] # Return empty list if image not loaded

        # Convert BGR to HSV
        hsv_image = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)

        # Define blue color range in HSV
        lower_blue_hsv = np.array([90, 100, 50]) # Increased lower-bound saturation to eliminate false alarms from water
        upper_blue_hsv = np.array([130, 255, 255])

        # Filter for only blue stuff using HSV
        mask = cv.inRange(hsv_image, lower_blue_hsv, upper_blue_hsv)
        # Apply the mask back to the original BGR image
        blue_only = cv.bitwise_and(self.frame, self.frame, mask=mask)

        # plt.imshow(cv.cvtColor(blue_only, cv.COLOR_BGR2RGB))
        # plt.title("Blue Filtered (HSV)")
        # plt.show()

        imgray = cv.cvtColor(blue_only, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray, 130, 255, cv.THRESH_TOZERO_INV)

        # plt.imshow(thresh, cmap='gray')
        # plt.show()

        # Detect contours
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contourimg = self.frame.copy()
        contourimg = cv.drawContours(contourimg, contours, -1, (0,255,0), 3)

        #   plt.imshow(cv.cvtColor(contourimg, cv.COLOR_BGR2RGB))
        #   plt.title("Contours Detected (HSV Filter)")
        #   plt.show()

        return contours

    def FilterContoursByArea(self):
        min_area = 600
        # max_area = 100000 # Increased this a bit to be safe
        filtered_contours = []

        for contour in self.contours:
            area = cv.contourArea(contour)

            # 1. Area Filter
            if min_area < area:
                # 2. Shape Filter (Aspect Ratio)
                x, y, w, h = cv.boundingRect(contour)
                aspect_ratio = float(w) / h

                if 0.4 < aspect_ratio < 2.5: # Adjust based on sign shape
                    filtered_contours.append(contour)

        # Draw for debugging
        filteredcontourimg = self.frame.copy()
        # cv.drawContours(filteredcontourimg, filtered_contours, -1, (0, 255, 0), 2) # Thickness 2 makes it easier to see

        # plt.imshow(cv.cvtColor(filteredcontourimg, cv.COLOR_BGR2RGB))
        # plt.show()

        return filtered_contours


    def perspectiveTransform(self):

        numberofcontours = len(self.filtered_contours)


        if numberofcontours > 1:

            # print(len(self.filtered_contours))

            # Sort the filtered contours by area in descending order so that the largest contour (the board) is always at index 0
            self.filtered_contours.sort(key=cv.contourArea, reverse=True)

            # Now the largest contour (the board) is ALWAYS at index 0
            desiredcontour = 1


            perimeter = cv.arcLength(self.filtered_contours[desiredcontour], True)
            vertices = cv.approxPolyDP(self.filtered_contours[desiredcontour], 0.02*perimeter, True)
            ordered_vertices = self.order_points_for_perspective_transform(vertices.reshape(-1, 2).astype(np.float32)) # Reshape to match reference vertices and sort just to be safe

            referenceVertices_raw = np.array([[0,0], [834,0],[834,544],[0,544]], dtype=np.float32) # adjusted reference vertices
            ordered_referenceVertices = self.order_points_for_perspective_transform(referenceVertices_raw)

            # Test that we can find the corners
            parallelogram = cv.polylines(self.frame.copy(), vertices, True, (0, 255, 0), 3)

            # # Display the image with the drawn parallelogram
            # plt.imshow(cv.cvtColor(parallelogram, cv.COLOR_BGR2RGB))
            # plt.show()

            if len(ordered_vertices) == 4: # Check if we have 4 vertices to perform perspective transform
                M = cv.getPerspectiveTransform(ordered_vertices, ordered_referenceVertices)

                self.transformedImg = cv.warpPerspective(self.frame.copy(),M,(834,544))

                # plt.imshow(cv.cvtColor(self.transformedImg, cv.COLOR_BGR2RGB))
                # plt.show()



    def order_points_for_perspective_transform(self, pts):
        # the first entry in the list is the top-left,
        # the second entry is the top-right, the third is the
        # bottom-right, and the fourth is the bottom-left
        rect = np.zeros((4, 2), dtype = "float32")

        # the top-left point will have the smallest sum, whereas
        # the bottom-right point will have the largest sum
        s = pts.sum(axis = 1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # now, compute the difference between the points, the
        # top-right point will have the smallest difference,
        # whereas the bottom-left will have the largest difference
        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        # return the ordered coordinates
        return rect
    
    def readClueboardandPublish(self):
        if hasattr(self, 'transformedImg'):

            # plt.imshow(cv.cvtColor(self.transformedImg, cv.COLOR_BGR2RGB))  
            # plt.title("Transformed Image")
            # plt.show()

            type, clueboard_text = read_board(self.transformedImg)
            # print(clueboard_text) # output of nn
            publish_clue(type, clueboard_text)
            print(f"Clueboard read: {type} - {clueboard_text}")


    def changeClueboard(self):

        msg = Bool()
        msg.data = self.clueboard
        self.pub.publish(msg)




if __name__ == '__main__':

  rospy.init_node('clueboarddetecting')
  lineFollower = ClueboardFinder()
  rospy.spin()
