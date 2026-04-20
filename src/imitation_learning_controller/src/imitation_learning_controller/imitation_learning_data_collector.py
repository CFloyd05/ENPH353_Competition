#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import cv2
import os
import csv
from cv_bridge import CvBridge
bridge = CvBridge()
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

RUN_ID = 115

rospy.init_node('imitation_learning_data_collector')

def image_callback(img_data):
  global csv_writer
  global frame_id
  global last_save_time
  time = rospy.Time.now().to_sec()

  if latest_vel == None:
    return

  if (time - last_save_time) < (1/sampling_rate):
    return

  try:
    img = bridge.imgmsg_to_cv2(img_data, "bgr8")
  except Exception as e:
    print("Image conversion failed")
    return

  image_name = "img_" + str(frame_id) + ".png"
  linear = latest_vel.linear.x
  angular = latest_vel.angular.z

  csv_writer.writerow([image_name, linear, angular, time])
  cv2.imwrite(os.path.join(path, image_name), img)

  frame_id += 1

def vel_callback(vel_data):
  global latest_vel
  latest_vel = vel_data

frame_id = 0
latest_vel = None
last_save_time = rospy.Time.now().to_sec()

path = "/home/fizzer/ros_ws/src/imitation_learning_controller/src/imitation_learning_controller/data/" + str(RUN_ID) + "/"
os.makedirs(path, exist_ok=True)
sampling_rate = 5
latest_vel = Twist()

csv_path = os.path.join(path, "data.csv")
csv_file = open(csv_path, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["image", "linear_x", "angular_z", "timestamp"])

def set_position(position):
        msg = ModelState()
        msg.model_name = 'B1'

        msg.pose.position.x = position[0]
        msg.pose.position.y = position[1]
        msg.pose.position.z = position[2]
        msg.pose.orientation.x = position[3]
        msg.pose.orientation.y = position[4]
        msg.pose.orientation.z = position[5]
        msg.pose.orientation.w = position[6]

        rospy.wait_for_service('/gazebo/set_model_state')
        try:
            set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
            resp = set_state( msg )

        except rospy.ServiceException:
            print ("Service call failed")

LINE_3 = [-4.1, -2.3, 0.05, 0, 0, 0, 1]
set_position(LINE_3)

sub_cam = rospy.Subscriber('/B1/rrbot/cameraFront/image_raw_front', Image, image_callback, queue_size=1)
sub_vel = rospy.Subscriber('/B1/cmd_vel', Twist, vel_callback, queue_size=1)

rospy.spin()
