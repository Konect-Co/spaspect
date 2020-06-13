import os
import pathlib
 
if "models" in pathlib.Path.cwd().parts:
	while "models" in pathlib.Path.cwd().parts:
		os.chdir('..')
elif not pathlib.Path('models').exists():
	os.system("git clone --depth 1 https://github.com/tensorflow/models")
 
import numpy as np
import os
import sys
import tensorflow as tf
print("Tensorflow version", tf.__version__)

from matplotlib import pyplot as plt
from PIL import Image
 
# List of the strings that is used to add correct label for each box.
 
def load_model(model_name):
	base_url = 'http://download.tensorflow.org/models/object_detection/'
	model_file = model_name + '.tar.gz'
	model_dir = tf.keras.utils.get_file(fname=model_name, origin=base_url + model_file, untar=True)
	model_dir = pathlib.Path(model_dir)/"saved_model"

	model = tf.saved_model.load(str(model_dir))
	model = model.signatures['serving_default']

	return model
 
model_name = 'ssd_mobilenet_v1_coco_2017_11_17'
detection_model = load_model(model_name)
 
def run_inference_for_single_image(model, image):
	image = np.asarray(image)
	# The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
	input_tensor = tf.convert_to_tensor(image)
	
	# The model expects a batch of images, so add an axis with `tf.newaxis`.
	input_tensor = input_tensor[tf.newaxis,...]

	# Run inference
	output_dict = model(input_tensor)

	# All outputs are batches tensors.
	# Convert to numpy arrays, and take index [0] to remove the batch dimension.
	# We're only interested in the first num_detections.
	num_detections = int(output_dict.pop('num_detections'))
	output_dict = {key:value[0, :num_detections].numpy() for key,value in output_dict.items()}
	
	output_dict['num_detections'] = num_detections

	# detection_classes should be ints.
	output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)

	return output_dict

def makePeopleCoordinates(image_path):
	image_np = np.array(Image.open(image_path))
	output_dict = run_inference_for_single_image(detection_model, image_np)

	peoplePixelCoordinates = []

	for i in range(output_dict["num_detections"]):
		#want to only use detection outputs that are likely
		if (output_dict["detection_scores"][i] < 0.7):
			break
		#we only care about detection outputs that include people

		relevantClasses = [1]
		if(output_dict["detection_classes"][i] in relevantClasses):
			box = output_dict["detection_boxes"][i]
			ymin, xmin, ymax, xmax = box

			width = image_np.shape[1]
			height = image_np.shape[0]

			personCoordinate = [(xmax+xmin)*0.5-1/2,(ymax*height-height/2)/width]
			#coordinates are scaled down by factor of width and origin is placed at center of image
			#so, width max is 0.5 and height max is height/2*width
			peoplePixelCoordinates.append(personCoordinate)

	#TODO: Center at 0
	return peoplePixelCoordinates
