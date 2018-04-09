############## Task1.1 - ArUco Detection ##############
### YOU CAN EDIT THIS FILE FOR DEBUGGING PURPOSEs, SO THAT YOU CAN TEST YOUR ArUco_library.py AGAINST THE VIDEO Undetected ArUco markers.avi###
### BUT MAKE SURE THAT YOU UNDO ALL THE CHANGES YOU HAVE MADE FOR DEBUGGING PURPOSES BEFORE TESTING AGAINST THE TEST IMAGES ###

import numpy as np
import cv2
import cv2.aruco as aruco
import time
from ArUco_library import *


image_list = ["Test_image1.png"]
test_num = 1

for image in image_list:
    img = cv2.imread(image)
    Detected_ArUco_markers = detect_ArUco(img)									## detecting ArUco ids and returning ArUco dictionary
    angle = Calculate_orientation_in_degree(Detected_ArUco_markers,img)				## finding orientation of aruco with respective to the menitoned scale in Problem_statement.pdf
    img = mark_ArUco(img,Detected_ArUco_markers,angle)						## marking the parameters of aruco which are mentioned in the Problem_Statement.pdf
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    result_image = "../Test_images/Result_image"+str(test_num)+".png"
    cv2.imwrite(result_image,img)									## saving the result image
    test_num = test_num +1

