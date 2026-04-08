#!/usr/bin/env python3

import os
import random
import cv2
from call_nn import read_board

use_augmented_boards = True

if use_augmented_boards:
  board_folder_path = "/home/fizzer/ros_ws/src/clue_board_generator/src/clue_board_generator/augmented_images/"
else:
  board_folder_path = "/home/fizzer/ros_ws/src/2025_competition/enph353/enph353_gazebo/media/materials/textures/unlabelled/"

def files_in_folder(folder_path):
  return sorted(os.listdir(folder_path))

boards = files_in_folder(board_folder_path)
for i in range(5):
  board_index = random.randrange(len(boards))
  board_name = boards[board_index]
  board_path = board_folder_path + board_name
  board_img = cv2.imread(board_path)
  if board_img is None:
    continue

  pred_clue_type, pred_clue_value = read_board(board_img)
  print(board_name)
  print(pred_clue_type + " - " + pred_clue_value)
