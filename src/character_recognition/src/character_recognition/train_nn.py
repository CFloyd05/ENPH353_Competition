import string
import random
from random import randint
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from PIL import Image, ImageFont, ImageDraw
import shutil
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import optimizers
from tensorflow.keras.utils import plot_model
from tensorflow.keras import backend
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
ImageDataGenerator = tf.keras.preprocessing.image.ImageDataGenerator
import re
from collections import Counter
import math

# Generate one-hot encoding
# Use hotEncodingMatrix[charIndices['Letter/Number']] to get the one hot encoding
chars = string.ascii_uppercase + string.digits + " "
charIndices = {}
for i, c in enumerate(chars):
    charIndices[c] = i
hotEncodingMatrix = np.eye(37)

