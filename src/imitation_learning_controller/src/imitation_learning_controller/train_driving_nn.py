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
import pandas as pd

NUMBER_OF_EPOCHS = 30
IMG_HEIGHT = 100
IMG_WIDTH = 140
BATCH_SIZE = 15
path = "/home/fizzer/ros_ws/src/imitation_learning_controller/src/imitation_learning_controller/data/"
images = []
labels = []

def files_in_folder(folder_path):
    return sorted(os.listdir(folder_path))

# CNN architecture
conv_model = models.Sequential()
conv_model.add(layers.Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1)))
conv_model.add(layers.Conv2D(16, (5,5), activation='relu'))
conv_model.add(layers.Conv2D(32, (5,5), activation='relu'))
conv_model.add(layers.Conv2D(64, (3,3), activation='relu'))

conv_model.add(layers.Flatten())
conv_model.add(layers.Dropout(0.5))

conv_model.add(layers.Dense(64, activation='relu'))
conv_model.add(layers.Dense(2))

LEARNING_RATE = 1e-4
conv_model.compile(loss='mse', optimizer=optimizers.Adam(learning_rate=LEARNING_RATE), metrics=['mae'])

#Import data
samples = []

run_folder = files_in_folder(path)
for run in run_folder:
    run_path = os.path.join(path, run)
    csv_path = os.path.join(run_path, "data.csv")

    if not os.path.exists(csv_path):
        continue

    data = pd.read_csv(csv_path)

    for _, row in data.iterrows():
        img_path = os.path.join(run_path, row["image"])
        samples.append((img_path, row["linear_x"], row["angular_z"]))

def data_generator(samples, batch_size):
    while True:
        np.random.shuffle(samples)

        for start in range(0, len(samples), batch_size):
            batch = samples[start:start + batch_size]

            images = []
            labels = []

            for img_path, linear_x, angular_z in batch:
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue

                img = img[1000:, :]
                img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                img = img.astype(np.float32) / 255.0
                img = img.reshape(IMG_HEIGHT, IMG_WIDTH, 1)

                images.append(img)
                labels.append([linear_x, angular_z])

            if len(images) == 0:
                continue

            yield np.array(images, dtype=np.float32), np.array(labels, dtype=np.float32)


np.random.shuffle(samples)

split_index = int(0.9 * len(samples))
train_samples = samples[:split_index]
val_samples = samples[split_index:]

train_gen = data_generator(train_samples, BATCH_SIZE)
val_gen = data_generator(val_samples, BATCH_SIZE)


early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

#Train
history = conv_model.fit(
    train_gen,
    steps_per_epoch=max(1, len(train_samples) // BATCH_SIZE),
    validation_data=val_gen,
    validation_steps=max(1, len(val_samples) // BATCH_SIZE),
    epochs=NUMBER_OF_EPOCHS,
    callbacks=[early_stop]
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

