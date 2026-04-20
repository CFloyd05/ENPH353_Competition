#! /usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import cv2
import os
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from call_drive_nn import get_cmd_vel

rospy.init_node('testing_imitation_learning_driving')
rate = rospy.Rate(5)
move = Twist()
latest_image = None

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

move.linear.x = 0
move.angular.z = 0

def image_callback(data):
  global latest_image
  latest_image = data

pub = rospy.Publisher('/B1/cmd_vel', Twist, queue_size=1)
sub_cam = rospy.Subscriber('/B1/rrbot/cameraFront/image_raw_front', Image, image_callback, queue_size=1)

pub.publish(move)
LINE_3 = [-4.1, -2.3, 0.05, 0, 0, 0, 1]
set_position(LINE_3)
start_time = rospy.Time.now()

while True:
  if rospy.Time.now().to_sec() - start_time.to_sec() < 3:
    move.linear.x = 1.5
    pub.publish(move)
  else:
    if latest_image != None:
      cmd_vel = get_cmd_vel(latest_image)
      print(cmd_vel)
      move.linear.x = 1
      move.angular.z = cmd_vel[1]
      pub.publish(move)
  rate.sleep()
