#!/usr/bin/env python3

import numpy as np
import string
import tensorflow as tf
from character_isolation.isolate_chars import isolate_chars_runtime

chars = string.ascii_uppercase + string.digits + " "

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path="conv_model.tflite")

# Allocate tensors (necessary to prepare the interpreter for inference)
interpreter.allocate_tensors()

# Get input and output tensor details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def read_board(board):
  output_clue_type = ""
  output_clue_value = ""
  input_chars = isolate_chars_runtime(board)
  i = 0
  for char in input_chars:
    input_data = char/255.0
    input_tensor = np.expand_dims(input_data, axis=0).astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_tensor)
    # Invoke the interpreter to run inference
    interpreter.invoke()
    # Get the output tensor
    output_data = interpreter.get_tensor(output_details[0]['index'])
    # Intepret the output tensor
    output_index = np.argmax(output_data[0])
    if i < 6:
      output_clue_type += chars[output_index]
    else:
      output_clue_value += chars[output_index]
    i += 1
  return output_clue_type.rstrip(), output_clue_value.rstrip()


