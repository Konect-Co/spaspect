import argparse
import cv2
import streamlink

# Parsing arguments
parser = argparse.ArgumentParser(description='Read from streamlink and save frame to file.')
parser.add_argument('link', type=str,
                    help='stream link to read from or link to extract from (if --extract specified)')
parser.add_argument('imagePath', type=str,
                    help='image path to save to')
parser.add_argument('--extract', help="extract streamLink from specified link", action="store_true")

args = parser.parse_args()

if args.extract:
    streams = streamlink.streams(args.link)
    streamLink = streams[list(streams.keys())[0]].url
    print("[INFO] Extracted link", streamLink)
else:
    streamLink = args.link

# Opening the stream and reading the image
cap = cv2.VideoCapture()
opened = cap.open(streamLink)

read, image = cap.read()

# Writing the image to specified file
if read:
    cv2.imwrite(args.imagePath, image)
else:
    print("[ERROR] Failed to read from specified streamlink " + streamLink + ".")
    exit(1)


