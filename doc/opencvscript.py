# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 10:29:52 2018
Color detection
@author: 2jzyz
"""
# import the necessary packages
import cv2
import numpy as np
from matplotlib import pyplot as plt

# load the image
image = cv2.imread("out.jpg")
# Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# convert to RGB
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#display image
plt.imshow(rgb)
plt.show()

#RGB
#(lower, upper) = ([25, 146, 190], [62, 174, 250]) #RGB
(lower1, upper1) =([25,140,100],[45,255,255])
(lower2, upper2) =([20, 100, 100],[30, 255, 255])
# create NumPy arrays from the boundaries
print("range 1:\n")
lower = np.array(lower1, dtype = "uint8")
upper = np.array(upper1, dtype = "uint8")
# find the colors within the specified boundaries and apply
# the mask
mask = cv2.inRange(hsv, lower, upper)
output = cv2.bitwise_and(hsv, image, mask = mask)
# show result image
plt.imshow(output)
plt.show()

print("range 2:\n")
lower = np.array(lower2, dtype = "uint8")
upper = np.array(upper2, dtype = "uint8")
# find the colors within the specified boundaries and apply
# the mask
mask = cv2.inRange(hsv, lower, upper)
output = cv2.bitwise_and(hsv, image, mask = mask)
# show result image
plt.imshow(output)
plt.show()

#canny edge detection
canny_thresholds = [80,200]
edges = cv2.Canny(image, canny_thresholds[0], canny_thresholds[1], apertureSize = 3)
edge_colored = cv2.bitwise_and(hsv, image,mask = edges)
plt.imshow(edge_colored)
plt.show()




