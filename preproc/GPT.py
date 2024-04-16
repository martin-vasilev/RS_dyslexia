# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 15:41:12 2024

@author: marti
"""

def non_max_suppression(boxes, probs=None, overlapThresh=0.3):
    # If there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # If the bounding boxes are integers, convert them to floats
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # Initialize the list of picked indices
    pick = []

    # Grab the coordinates of the bounding boxes
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]

    # Compute the area of the bounding boxes
    area = (x2 - x1 + 1) * (y2 - y1 + 1)

    # Sort the bounding boxes by their probability/confidence scores
    if probs is not None:
        idxs = np.argsort(probs)

    # Keep looping while some indexes still remain in the indexes list
    while len(idxs) > 0:
        # Grab the last index in the indexes list and add it to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # Find the largest (x, y) coordinates for the start of the bounding box and
        # the smallest (x, y) coordinates for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # Compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # Compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # Delete all indexes from the index list that have overlap greater than the provided threshold
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    # Return only the bounding boxes that were picked
    return boxes[pick].astype("int")


import cv2
import pytesseract
import os

os.chdir(r'D:\R\RS_dyslexia\stimuli\img')

# Load the image
image = cv2.imread('TNR20text1Key.bmp')


import cv2
import numpy as np
import pytesseract

# Load pre-trained EAST text detector
net = cv2.dnn.readNet("frozen_east_text_detection.pb")

# Load pre-trained model configuration for text detection
conf_threshold = 0.5
nms_threshold = 0.4

# Load the input image
orig = image.copy()
(H, W) = image.shape[:2]

# Preprocess the image
blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),
                             (123.68, 116.78, 103.94), swapRB=True, crop=False)
net.setInput(blob)
(scores, geometry) = net.forward(["feature_fusion/Conv_7/Sigmoid",
                                  "feature_fusion/concat_3"])

# Decode the predictions and apply non-maxima suppression
def decode_predictions(scores, geometry):
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    for y in range(0, numRows):
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        for x in range(0, numCols):
            if scoresData[x] < conf_threshold:
                continue

            offsetX, offsetY = (x * 4.0, y * 4.0)

            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    return (rects, confidences)

(rects, confidences) = decode_predictions(scores, geometry)

# Apply non-maximum suppression to suppress weak, overlapping bounding boxes
boxes = non_max_suppression(np.array(rects), probs=confidences)

# Loop over the bounding boxes
for (startX, startY, endX, endY) in boxes:
    # Draw the bounding box around the text region
    cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
    
    # Extract the region of interest (ROI) containing the text
    roi = orig[startY:endY, startX:endX]
    
    # Convert the region of interest to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to segment the characters
    _, thresh = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Loop over the contours
    for contour in contours:
        # Compute the bounding box for each contour
        (x, y, w, h) = cv2.boundingRect(contour)
        
        # Draw the bounding box around the character
        cv2.rectangle(orig, (startX + x, startY + y), (startX + x + w, startY + y + h), (255, 0, 0), 1)

# Show the output image
cv2.imshow("Text Detection", orig)
cv2.waitKey(0)
cv2.destroyAllWindows()


