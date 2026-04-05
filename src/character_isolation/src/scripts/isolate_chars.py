#!/usr/bin/env python3

import string
import random
from random import randint
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from PIL import Image, ImageFont, ImageDraw
import shutil
import re
from collections import Counter
import math

BOARD_WIDTH = 600
BOARD_HEIGHT = 400
CHAR_WIDTH = 48
CHAR_HEIGHT = 80
TOP_UPPER_ROW = 40
LEFT_UPPER_ROW = [249,294,339,384,429,474]
TOP_LOWER_ROW = 265
LEFT_LOWER_ROW = [27,72,118,163,209,253,299,343,389,433,479,524]
path = "/home/fizzer/ros_ws/src/character_isolation/src/scripts/"

def files_in_folder(folder_path):
    return sorted(os.listdir(folder_path))

images = files_in_folder(path + "images/")
for image in images:
  chars = []
  image_path = path + "images/" + image
  board_image = cv2.imread(image_path)

  for i in range (0,6):
    chars.append(board_image[TOP_UPPER_ROW:TOP_UPPER_ROW + CHAR_HEIGHT, LEFT_UPPER_ROW[i]:LEFT_UPPER_ROW[i] + CHAR_WIDTH])
  for i in range (0,12):
    chars.append(board_image[TOP_LOWER_ROW:TOP_LOWER_ROW + CHAR_HEIGHT, LEFT_LOWER_ROW[i]:LEFT_LOWER_ROW[i] + CHAR_WIDTH])

  for i in range (0,18):
    cv2.imwrite(os.path.join(path + "chars/", image[i] + ".png"), chars[i])
