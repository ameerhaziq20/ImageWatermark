# cara pakai 
# python main.py --ekt460_logo watermark_ip.png --source input --destination output

from imutils import paths
import numpy as np
import argparse
import cv2
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--ekt460_logo", required=True,
	help="path to ekt460_logo image (assumed to be transparent PNG)")
ap.add_argument("-i", "--source", required=True,
	help="path to the source directory of images")
ap.add_argument("-o", "--destination", required=True,
	help="path to the destination directory")
ap.add_argument("-a", "--alpha", type=float, default=0.25,
	help="alpha transparency of the overlay (smaller is more transparent)")
ap.add_argument("-c", "--correct", type=int, default=1,
	help="flag used to handle if bug is displayed or not")
args = vars(ap.parse_args())

ekt460_logo = cv2.imread(args["ekt460_logo"], cv2.IMREAD_UNCHANGED)
(wH, wW) = ekt460_logo.shape[:2]

if args["correct"] > 0:
	(B, G, R, A) = cv2.split(ekt460_logo)
	B = cv2.bitwise_and(B, B, mask=A)
	G = cv2.bitwise_and(G, G, mask=A)
	R = cv2.bitwise_and(R, R, mask=A)
	ekt460_logo = cv2.merge([B, G, R, A])


for imagePath in paths.list_images(args["source"]):

	image = cv2.imread(imagePath)
	(h, w) = image.shape[:2]
	image = np.dstack([image, np.ones((h, w), dtype="uint8") * 255])

	overlay = np.zeros((h, w, 4), dtype="uint8")
	overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = ekt460_logo

	# blend the two images together using transparent overlays
	destination = image.copy()
	cv2.addWeighted(overlay, args["alpha"], destination, 1.0, 0, destination)

	# write the destination image to disk
	filename = imagePath[imagePath.rfind(os.path.sep) + 1:]
	p = os.path.sep.join((args["destination"], filename))
	cv2.imwrite(p, destination)