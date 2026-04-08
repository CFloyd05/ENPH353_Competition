#!/usr/bin/env python3

import cv2
import os
from character_isolation.isolate_chars import isolate_chars_training

basic_input_path = "/home/fizzer/ros_ws/src/clue_board_generator/src/clue_board_generator/images/"
basic_output_path = "/home/fizzer/ros_ws/src/character_recognition/src/character_recognition/basic_chars/"
aug_input_path = "/home/fizzer/ros_ws/src/clue_board_generator/src/clue_board_generator/augmented_images/"
aug_output_path = "/home/fizzer/ros_ws/src/character_recognition/src/character_recognition/augmented_chars/"

def files_in_folder(folder_path):
  return sorted(os.listdir(folder_path))

clue_boards = files_in_folder(basic_input_path)
output = isolate_chars_training(clue_boards, basic_input_path)
for name, chars in output.items():
  cv2.imwrite(os.path.join(basic_output_path, name + ".png"), chars)


clue_boards = files_in_folder(aug_input_path)
output = isolate_chars_training(clue_boards, aug_input_path)
for name, chars in output.items():
  cv2.imwrite(os.path.join(aug_output_path, name + ".png"), chars)
