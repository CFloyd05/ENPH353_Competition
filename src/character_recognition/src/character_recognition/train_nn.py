#!/usr/bin/env python3

import string
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import optimizers
from tensorflow.keras.utils import plot_model
from tensorflow.keras import backend
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

NUMBER_OF_EPOCHS = 2
CHAR_HEIGHT = 80
CHAR_WIDTH = 48
path = "/home/fizzer/ros_ws/src/character_recognition/src/character_recognition/"

def files_in_folder(folder_path):
    return sorted(os.listdir(folder_path))

# Generate one-hot encoding
# Use hotEncodingMatrix[charIndices['Letter/Number']] to get the one hot encoding
chars = string.ascii_uppercase + string.digits + " "
charIndices = {}
for i, c in enumerate(chars):
    charIndices[c] = i
hotEncodingMatrix = np.eye(37)

# CNN architecture
# Input - Conv - Pool - Conv - Pool - Dense - Output
conv_model = models.Sequential()
conv_model.add(layers.Input(shape=(CHAR_HEIGHT, CHAR_WIDTH, 3)))
conv_model.add(layers.Conv2D(32, (3,3), activation='relu'))
conv_model.add(layers.MaxPooling2D((2,2)))
conv_model.add(layers.Conv2D(64, (3,3), activation='relu'))
conv_model.add(layers.MaxPooling2D((2,2)))
conv_model.add(layers.Flatten())
conv_model.add(layers.Dropout(0.5))
conv_model.add(layers.Dense(512, activation='relu'))
conv_model.add(layers.Dense(37, activation = 'softmax'))

LEARNING_RATE = 1e-4
conv_model.compile(loss='categorical_crossentropy', optimizer=optimizers.RMSprop(learning_rate=LEARNING_RATE), metrics=['acc'])

# Load chars
X = []
Y = []

augmentedChars = files_in_folder(path + "augmented_chars/")
for char in augmentedChars:
  X.append(cv2.imread(path + "augmented_chars/" + char))
  Y.append(hotEncodingMatrix[charIndices[char[0]]])

X = np.array(X, dtype=np.float32) / 255.0
Y = np.array(Y, dtype=np.float32)

# Split data into test and validation sets
X_train, X_val, Y_train, Y_val = train_test_split(
    X, Y, test_size=0.2, random_state=42, shuffle=True
)

# Train Model
history = conv_model.fit(
    X_train, Y_train,
    validation_data=(X_val, Y_val),
    epochs=NUMBER_OF_EPOCHS,
    batch_size=64,
    shuffle=True
)

#Plot loss vs epoch
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train loss', 'val loss'], loc='upper left')
plt.savefig("loss_graph.png")

# Convert the model
converter = tf.lite.TFLiteConverter.from_keras_model(conv_model)
tflite_model = converter.convert()

# Save the TFLite model
with open('conv_model.tflite', 'wb') as f:
    f.write(tflite_model)
