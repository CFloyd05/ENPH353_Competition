#! /usr//bin/env python3

import numpy as np
import rospy
import tensorflow as tf
from geometry_msgs.msg import Twist
import cv2
from cv_bridge import CvBridge
bridge = CvBridge()

IMG_HEIGHT = 100
IMG_WIDTH = 140

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="/home/fizzer/ros_ws/src/imitation_learning_controller/src/imitation_learning_controller/conv_model.tflite")

# Allocate tensors (necessary to prepare the interpreter for inference)
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Set the input tensor
def get_cmd_vel(data):
  img = bridge.imgmsg_to_cv2(data, "bgr8")
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img = img[1000:, :]
  img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
  img = img.astype(np.float32) / 255.0
  img = img.reshape(IMG_HEIGHT, IMG_WIDTH, 1)

  input_tensor = np.expand_dims(img, axis=0).astype(np.float32)
  interpreter.set_tensor(input_details[0]['index'], input_tensor)

  # Invoke the interpreter to run inference
  interpreter.invoke()

  # Get the output tensor
  output = interpreter.get_tensor(output_details[0]['index'])
  linear = output[0][0]
  angular = output[0][1]
  return(linear, angular)
