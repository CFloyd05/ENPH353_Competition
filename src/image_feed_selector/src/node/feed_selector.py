#! /usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image

rospy.init_node('image_feed_selector')
selected_cam = "front"

def cam_select_callback(camera):
  global selected_cam
  selected_cam = camera.data

def image_callback_front(data):
  if selected_cam == "front":
    pub.publish(data)

def image_callback_rear(data):
  if selected_cam == "rear":
    pub.publish(data)

def image_callback_left(data):
  if selected_cam == "left":
    pub.publish(data)

def image_callback_right(data):
  if selected_cam == "right":
    pub.publish(data)

sub_front_cam = rospy.Subscriber('/B1/rrbot/cameraFront/image_raw_front', Image, image_callback_front, queue_size=1)
sub_rear_cam = rospy.Subscriber('/B1/rrbot/cameraRear/image_raw_rear', Image, image_callback_rear, queue_size=1)
sub_left_cam = rospy.Subscriber('/B1/rrbot/cameraLeft/image_raw_left', Image, image_callback_left, queue_size=1)
sub_right_cam = rospy.Subscriber('/B1/rrbot/cameraRight/image_raw_right', Image, image_callback_right, queue_size=1)
sub_cam_select = rospy.Subscriber('/camera_to_read', String, cam_select_callback, queue_size=1)
pub = rospy.Publisher('/selected_camera_feed', Image, queue_size=1)

rospy.spin()
