#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Image
import cv2
import os
import cvs
from cv_bridge imoprt CvBridge

rospy.init_node('imitation_learning_data_collector')

def image_callback(img_data):
  global frame_id
  time = rospy.Time.now().to_sec()

  if latest_vel == None:
    return

  if (time - last_save_time) < (1/sampling_rate):
    return

  try:
    img = CvBridge.imgmsg_to_cv2(img_data, "bgr8")
  except Exception as e:
    print("Image conversion failed"
    return

  last_save_time = rospy.Time.now().to_sec()
  img = cv2.resize(img, (120,120))
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  edges = cv2.Canny(gray, 50, 150)

  image_name = ##
  linear = latest_vel.linear.x
  angular = latest_vel.angular.z

  csv_writer.writerow(image_name, linear, angular, time.to_sec())
  cv2.imwrite(image_path, cv_image) ##

  frame_id += 1

def vel_callback(vel_data):
  global latest_vel = vel_data

sub_cam = rospy.Subscriber('/B1/rrbot/cameraFront/image_raw_front', Image, image_callback, queue_size=1)
sub_vel = rospy.Subscriber('/B1/cmd_vel', Twist, vel_callback, queue_size=1)
path = "/home/fizzer/ros_ws/src/imitation_learning_controller/src/imitation_learning_controller/"
sampling_rate = 5
latest_vel = Twist()

csv_path = os.path.join(path, "data.csv")
csv_file = open(csv_path, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["image", "linear_x", "angular_z", "timestamp"])


frame_id = 0
last_save_time = rospy.Time.now().to_sec()

