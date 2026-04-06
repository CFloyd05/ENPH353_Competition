#!/usr/bin/env python3

import string
import cv2
import os

BOARD_WIDTH = 600
BOARD_HEIGHT = 400
CHAR_WIDTH = 48
CHAR_HEIGHT = 80
TOP_UPPER_ROW = 40
LEFT_UPPER_ROW = [249,294,339,384,429,474]
TOP_LOWER_ROW = 265
LEFT_LOWER_ROW = [27,72,118,163,209,253,299,343,389,433,479,524]

def isolate_chars_training(images, path):
  output = {}
  i = 1
  for image in images:
    image_path = path + image
    board_image = cv2.imread(image_path)
    chars = extract_chars(board_image)
    j = 0
    for char in chars:
      output[image[j] + "_" + str(i) + "_" + str(j+1)] = char
      j += 1
    i += 1
  return output

def isolate_chars_runtime(image):
  image = cv2.resize(image,(600,400))
  return(extract_chars(image))

def extract_chars(image):
  chars = []
  for i in range (0,6):
    chars.append(image[TOP_UPPER_ROW:TOP_UPPER_ROW + CHAR_HEIGHT, LEFT_UPPER_ROW[i]:LEFT_UPPER_ROW[i] + CHAR_WIDTH])
  for i in range (0,12):
    chars.append(image[TOP_LOWER_ROW:TOP_LOWER_ROW + CHAR_HEIGHT, LEFT_LOWER_ROW[i]:LEFT_LOWER_ROW[i] + CHAR_WIDTH])
  return chars
