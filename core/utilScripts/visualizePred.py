# This file should be run from core directory not parent directory
import os
import sys
sys.path.append(os.getcwd())

import cv2
from cv_model import pred
import argparse

# Parsing arguments
parser = argparse.ArgumentParser(description='Visualize output of detection model.')
parser.add_argument('imagePath', type=str, help='image path to read from and process')
parser.add_argument('--save', type=str, help="image path to save output to")

args = parser.parse_args()

# TODO: Inefficient - image is being read btth here and in predict function
# TODO: Inefficient - face detections are being made but not processed
# getting output from image
output = pred.predict(args.imagePath)
# returns whether image was successfully saved
image = cv2.imread(args.imagePath)

#printing image shape
print("Image shape", image.shape)

minScoreThreshold = 0.6
for i in range(len(output["detection_scores"])):
    score = output["detection_scores"][i]
    if (score < minScoreThreshold):
        break

    #defining box
    box_orig = output["detection_boxes"][i]
    box = [0,0,0,0]
    box[0] = int(box_orig[0]*image.shape[0])
    box[1] = int(box_orig[1]*image.shape[1])
    box[2] = int(box_orig[2]*image.shape[0])
    box[3] = int(box_orig[3]*image.shape[1])

    class_str = output["detection_classes"][i]

    # Note: Color in BGR
    color = (255, 0, 0)
    thickness = 2

    print("box_orig", box_orig, ", box", box, ", class", class_str, ", score", score)

    # Drawing rectange around prediction
    image = cv2.rectangle(image, (box[1], box[0]), (box[3], box[2]), color, thickness)
    # Adding text label above bounding box
    cv2.putText(image, class_str, (box[1], box[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, thickness)
    
if args.save:
    cv2.imwrite(args.save, image)
else:
    cv2.imshow("prediction", image)
