import os
import sys
import torch
import PIL.Image as pil
from torchvision import transforms
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm

#if running from same directory: import networks
from cv_model import networks
from cv_model.layers import disp_to_depth

import torchvision.models as models
import torch

import cv2

faster_rcnn = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
faster_rcnn.eval()

keypoint_rcnn = models.detection.keypointrcnn_resnet50_fpn(pretrained=True)
keypoint_rcnn.eval()

model_name = "mono+stereo_640x192"
base_path = sys.path[1]#os.getcwd()
paths = [os.path.join(base_path, "keywest2.jpg")]
output_directory = base_path

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

model_path = os.path.join(base_path, "cv_model", "models", model_name)
#encoder_path = os.path.join(model_path, "/cv_model/models/encoder.pth")
encoder_path = "./cv_model/models/mono+stereo_640x192/encoder.pth"
#depth_decoder_path = os.path.join(model_path, "depth.pth")
depth_decoder_path = "./cv_model/models/mono+stereo_640x192/depth.pth"

# LOADING PRETRAINED MODEL
encoder = networks.ResnetEncoder(18, False)
loaded_dict_enc = torch.load(encoder_path, map_location=device)

# extract the height and width of image that this model was trained with
feed_height = loaded_dict_enc['height']
feed_width = loaded_dict_enc['width']
filtered_dict_enc = {k: v for k, v in loaded_dict_enc.items() if k in encoder.state_dict()}
encoder.load_state_dict(filtered_dict_enc)
encoder.to(device)
encoder.eval()

depth_decoder = networks.DepthDecoder(
    num_ch_enc=encoder.num_ch_enc, scales=range(4))

loaded_dict = torch.load(depth_decoder_path, map_location=device)
depth_decoder.load_state_dict(loaded_dict)

depth_decoder.to(device)
depth_decoder.eval()

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

def predict(image_path):
    with torch.no_grad():
        # Load image and preprocess
        input_image_pil = pil.open(image_path).convert('RGB')
        original_width, original_height = input_image_pil.size
        input_image = input_image_pil.resize((feed_width, feed_height), pil.LANCZOS)
        input_image = transforms.ToTensor()(input_image).unsqueeze(0)

        # PREDICTION
        input_image = input_image.to(device)
        features = encoder(input_image)
        
        outputs = depth_decoder(features)

        disp = outputs[("disp", 0)]
        disp_resized = torch.nn.functional.interpolate(
            disp, (original_height, original_width), mode="bilinear", align_corners=False)
        
        _, depth = disp_to_depth(disp_resized, 0.1, 100)
        depth = depth.numpy()
        depth = np.reshape(depth, (original_height, original_width))
        
        new_width, new_height = 800, 800
        input_image = input_image_pil.resize((new_width, new_height), pil.LANCZOS)
        input_image = transforms.ToTensor()(input_image).unsqueeze(0)
        #output = faster_rcnn(input_image)[0]
        output = keypoint_rcnn(input_image)[0]

        #[top left x position, top left y position, width, height]
        output["boxes"] = output["boxes"].numpy()
        output["labels"] = output["labels"].numpy()
        output["keypoints"] = output["keypoints"].numpy()
        output["scores"] = output["scores"].numpy()

        output["labels"] = [ coco_labels[label] for label in output["labels"] ]
        output["boxes"][:,::2] *= original_width/new_width
        output["boxes"][:,1::2] *= original_height/new_height
        output["keypoints"][:,:,0] *= original_width/new_width
        output["keypoints"][:,:,1] *= original_height/new_height

        #TODO: Sort output so it includes only labels with highest probability predictions

        output["depth"] = depth

        return output