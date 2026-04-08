import cv2 as cv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

import rospy
from std_msgs.msg import Bool
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class ClueboardFinder:

    def __init__(self):

        rospy.loginfo("initiating")
    
        self.pub = rospy.Publisher('/clueboard', Bool, queue_size=1)
        self.rate = rospy.Rate(2)

        self.subscriber = rospy.Subscriber("/B1/rrbot/camera1/image_raw", Image, self.image_callback)

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


            self.cropstart = self.frame.shape[0] // 3 * 2
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



        # Update the clueboard thing


    def MaskAndFindContours_HSV(self):
        # Check if the image was loaded successfully
        if self.frame is None:
            print(f"Error: Could not load image. Please ensure the file exists and the path is correct.")
            return [] # Return empty list if image not loaded

        # Convert BGR to HSV
        hsv_image = cv.cvtColor(self.frame, cv.COLOR_BGR2HSV)

        # Define blue color range in HSV
        lower_blue_hsv = np.array([90, 50, 50])
        upper_blue_hsv = np.array([130, 255, 255])

        # Filter for only blue stuff using HSV
        mask = cv.inRange(hsv_image, lower_blue_hsv, upper_blue_hsv)
        # Apply the mask back to the original BGR image
        blue_only = cv.bitwise_and(self.frame, self.frame, mask=mask)

        #   plt.imshow(cv.cvtColor(blue_only, cv.COLOR_BGR2RGB))
        #   plt.title("Blue Filtered (HSV)")
        #   plt.show()

        imgray = cv.cvtColor(blue_only, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray, 150, 255, cv.THRESH_TOZERO_INV)

        # Detect contours
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contourimg = self.frame.copy()
        contourimg = cv.drawContours(contourimg, contours, -1, (0,255,0), 3)

        #   plt.imshow(cv.cvtColor(contourimg, cv.COLOR_BGR2RGB))
        #   plt.title("Contours Detected (HSV Filter)")
        #   plt.show()

        return contours

    def FilterContoursByArea(self):
        # Filter contours by area to ignore small noise and the sky (big)
        min_contour_area = 400 # adjust this value as needed
        max_contour_area = 4000 # adjust this value as needed - not in use right now

        filtered_contours = []
        for contour in self.contours:
            area = cv.contourArea(contour)
            if area > min_contour_area:
                filtered_contours.append(contour)

        #   print(f"Original number of contours: {len(contours)}")
        #   print(f"Number of contours after filtering: {len(filtered_contours)}")

        # Draw filtered contours on the original image
        filteredcontourimg = self.frame.copy()
        filteredcontourimg = cv.drawContours(filteredcontourimg, filtered_contours, -1, (0, 255, 0), 1)

        #   plt.imshow(cv.cvtColor(filteredcontourimg, cv.COLOR_BGR2RGB))
        #   plt.title(f'Filtered Contours (Area > {min_contour_area})')
        #   plt.show()

        return filtered_contours
    
    def changeClueboard(self):
        
        msg = Bool()
        msg.data = self.clueboard
        self.pub.publish(msg)

            


if __name__ == '__main__':

  rospy.init_node('clueboarddetecting')
  lineFollower = ClueboardFinder()
  rospy.spin()
