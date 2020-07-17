import os
import sys
import PIL.Image as pil
import numpy as np
import tensorflow as tf

import cv2
import cv_model.detectMask as detectMask

base_path = sys.path[1]#os.getcwd()
paths = [os.path.join(base_path, "keywest.jpg")]
output_directory = base_path

coco_labels = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

loaded = tf.saved_model.load("./cv_model/models/mobilenet-model")
infer = loaded.signatures["serving_default"]


def predict(image_path):
	new_width = 800
	new_height = 800

	"""
	input_image_pil = pil.open(image_path).convert('RGB')
	original_width, original_height = input_image_pil.size
	input_image = input_image_pil.resize((new_width,new_height), pil.LANCZOS)
	"""

	# Load image and preprocess
	input_image = cv2.imread(image_path)
	original_width, original_height = input_image.shape[:-1]
	input_image = cv2.resize(input_image, (new_width, new_height))
	input_image = np.expand_dims(input_image, 0)

	output = infer(tf.constant(input_image))

	output["detection_boxes"] = output["detection_boxes"].numpy()[0]
	output["detection_scores"] = output["detection_scores"].numpy()[0]
	output["detection_classes"] = output["detection_classes"].numpy()[0]

	#TODO: Sort output so it includes only labels with highest probability predictions
	#[top left x position, top left y position, width, height]

	output["detection_classes"] = [ coco_labels[int(label)] for label in output["detection_classes"] ]
	output["detection_boxes"][:,::2] *= original_width/new_width
	output["detection_boxes"][:,1::2] *= original_height/new_height

	output["masks"] = detectMask.genPredictions(image_path)

	return output
