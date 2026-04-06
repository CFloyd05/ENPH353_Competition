#!/usr/bin/env python3

import numpy as np
import tensorflow as tf
import os
from PIL import Image, ImageFont, ImageDraw
import cv2

ImageDataGenerator = tf.keras.preprocessing.image.ImageDataGenerator
datagen = ImageDataGenerator(rotation_range=2, zoom_range=0.01, brightness_range=[0.4, 1.4])
NUM_IMAGES_TO_GENERATE = 10
path = "/home/fizzer/ros_ws/src/clue_board_generator/src/clue_board_generator/"

def files_in_folder(folder_path):
    return sorted(os.listdir(folder_path))

# Load images:
images = files_in_folder(path + "images/")
for image in images:
  image_path = path + "images/" + image
  image_name = os.path.splitext(image)[0]

  # Create an array with a single image (we need it for the iterator)
  image_array = np.expand_dims(Image.open(image_path), 0)
  datagen_iterator = datagen.flow(image_array, batch_size=1)

  for j in range(NUM_IMAGES_TO_GENERATE):
    value = next(datagen_iterator)
    img = value[0].astype('uint8')
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Write license plate to file
    cv2.imwrite(os.path.join(path + "augmented_images/",
                             "{}_aug{}.png".format(image_name, j)),
                             img)
