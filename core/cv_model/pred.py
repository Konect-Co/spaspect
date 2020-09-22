import numpy as np
import tensorflow as tf

import cv2
import cv_model.detectMask as detectMask

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

#loading tensorflow model
loaded = tf.saved_model.load("./cv_model/models/mobilenetModel")
infer = loaded.signatures["serving_default"]

# This function returns CV model output in a raw format, as returned 
# by the object detection and mask classification model. Outputs of 
# this function are processed further to yield data for aggregate and
# realtime dashboard.
def predict(input_image_orig):
	# Load image and preprocess
	input_image = np.expand_dims(input_image_orig, 0)

	# Run inference on the input image
	odResults = infer(tf.constant(input_image))

	#[top left x position, top left y position, width, height]
	odResults["detection_boxes"] = odResults["detection_boxes"].numpy()[0]
	odResults["detection_scores"] = odResults["detection_scores"].numpy()[0]
	odResults["detection_classes"] = odResults["detection_classes"].numpy()[0]
	# Replace number labels with strings corresponding with object name
	odResults["detection_classes"] = [ coco_labels[int(label)] for label in odResults["detection_classes"] ]
	
	output = {"boxes":[], "scores":[], "classes":[]}

	# Run image through mask detection network and store inference results
	output["masks"] = detectMask.genPredictions(input_image_orig)

	for i in range(len(odResults["detection_boxes"])):
		score = odResults["detection_scores"][i]
		_class = odResults["detection_classes"][i]
		box = odResults["detection_boxes"][i]

		if (score < 0.2):
			break
		if (not _class == "person"):
			continue

		output["boxes"].append(box.tolist())
		output["scores"].append(score)
		output["classes"].append(_class)

	# Return entirety of results back to caller
	return output
