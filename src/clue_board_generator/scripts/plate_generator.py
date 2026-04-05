#!/usr/bin/env python3

import cv2
import csv
import numpy as np
import os
import random
import requests
import string

from random import randint
from PIL import Image, ImageFont, ImageDraw
NUM_OF_PLATES = 10


def loadCrimesProfileCompetition(plates):
    clues = {}
    for i in range (plates):
        upperClue = ''
        lowerClue = ''
        for j in range (0,6):
            upperClue += (random.choice(string.ascii_uppercase + string.digits))
        for j in range (0, 12):
            lowerClue += (random.choice(string.ascii_uppercase + string.digits))
        clues[upperClue] = lowerClue
    return clues

# Find the path to this script
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__)) + "/"
TEXTURE_PATH = 'images/'

banner_canvas = cv2.imread(SCRIPT_PATH+'clue_banner.png')
PLATE_HEIGHT = 600
PLATE_WIDTH = banner_canvas.shape[1]
IMG_DEPTH = 3

clues = loadCrimesProfileCompetition(NUM_OF_PLATES)

for key, value in clues.items():
    entry = key + "," + value
    print(entry)

    # Generate plate

    # To use monospaced font for the license plate we need to use the PIL
    # package.
    # Convert into a PIL image (this is so we can use the monospaced fonts)
    blank_plate_pil = Image.fromarray(banner_canvas)
    # Get a drawing context
    draw = ImageDraw.Draw(blank_plate_pil)
    font_size = 90
    monospace = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf", 
                                    font_size)
    font_color = (255,0,0)
    draw.text((250, 30), key, font_color, font=monospace)
    draw.text((30, 250), value, font_color, font=monospace)
    # Convert back to OpenCV image and save
    populated_banner = np.array(blank_plate_pil)

    # Save image
    cv2.imwrite(os.path.join(SCRIPT_PATH+TEXTURE_PATH,key + value + ".png"), populated_banner)

