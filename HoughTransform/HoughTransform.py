#! usr/bin/python
#coding=utf-8
#doing all the relevant imports
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

#read image
image = mpimg.imread('exit-ramp.jpg')
#grayscale
gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

# Define a kernel size and apply Gaussian smoothing
kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

# Define our parameters for Canny and apply
low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

#Create a masked edge image
mask = np.zeros_like(edges)
ignore_mask_color = 255
#Define a four sided polygon to mask
imshape = image.shape
vertices = np.array([[(0,imshape[0]),(450,290),(490,290),(imshape[1],imshape[0])]],
                    dtype=np.int32)
print("(0,imshape[0]):",0,imshape[0],"   (imshape[1],imshape[0]):",imshape[1],imshape[0])
cv2.fillPoly(mask,vertices,ignore_mask_color)
masked_edges = cv2.bitwise_and(edges,mask)



#Make a blank the same size as origin image to show
rho = 1
theta = np.pi/180
threshold = 1
min_line_length = 40
max_line_gap = 20
line_image = np.copy(image)*0

#run Hough Transform on edge detected image
lines = cv2.HoughLinesP(masked_edges,rho,theta,threshold,np.array([]),
                        min_line_length,max_line_gap)


# Iterate over the output "lines" and draw lines on the blank
for line in lines:
    for x1,y1,x2,y2 in line:
        cv2.line(line_image,(x1,y1),(x2,y2),(0,255,0),10)

# Create a "color" binary image to combine with line image
color_edges = np.dstack((edges,edges,edges))

# Display the image
combo = cv2.addWeighted(color_edges, 1, line_image, 0.5, 0)
plt.subplot(221)
plt.imshow(image)
plt.subplot(222)
plt.imshow(edges)
plt.subplot(223)
plt.imshow(masked_edges)
plt.subplot(224)
plt.imshow(combo)
plt.show()
