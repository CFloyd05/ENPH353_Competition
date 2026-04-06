#!/usr/bin/env python3

import cv2
import os
from character_isolation.isolate_chars import isolate_chars_training

input_path = "/home/fizzer/ros_ws/src/clue_board_generator/src/clue_board_generator/images/"
output_path = "/home/fizzer/ros_ws/src/character_recognition/src/character_recognition/basic_chars/"

def files_in_folder(folder_path):
  return sorted(os.listdir(folder_path))

clue_boards = files_in_folder(input_path)
output = isolate_chars_training(clue_boards, input_path)
for name, chars in output.items():
  cv2.imwrite(os.path.join(output_path, name + ".png"), chars)


