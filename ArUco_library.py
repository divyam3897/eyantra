############## Task1.1 - ArUco Detection ##############
import numpy as np
import cv2
import cv2.aruco as aruco
import sys
import math
import time

def detect_ArUco(img):
    ## function to detect ArUco markers in the image using ArUco library
    ## argument: img is the test image
    ## return: dictionary named Detected_ArUco_markers of the format {ArUco_id_no : corners}, where ArUco_id_no indicates ArUco id and corners indicates the four corner position of the aruco(numpy array)
    ## 		   for instance, if there is an ArUco(0) in some orientation then, ArUco_list can be like
    ## 				{0: array([[315, 163],
    #							[319, 263],
    #							[219, 267],
    #							[215,167]], dtype=float32)}

    Detected_ArUco_markers = {}
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
    parameters = aruco.DetectorParameters_create()
    corners,ids, _ = aruco.detectMarkers(img,aruco_dict,parameters=parameters)
#    if ids == None:
 #       return None
    for i in range(0,ids.shape[0]):
        Detected_ArUco_markers[ids[i][0,]] = corners[i][0,]
    for i in Detected_ArUco_markers:
        id_str = str(i)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,id_str,(Detected_ArUco_markers[i][0][0],Detected_ArUco_markers[i][0][1]), font, 0.5,(0,0,255),2,cv2.LINE_AA)
    return Detected_ArUco_markers


def Calculate_orientation_in_degree(Detected_ArUco_markers,img):
    ## function to calculate orientation of ArUco with respective to the scale mentioned in Problem_Statement.pdf
    ## argument: Detected_ArUco_markers  is the dictionary returned by the function detect_ArUco(img)
    ## return : Dictionary named ArUco_marker_angles in which keys are ArUco ids and the values are angles (angles have to be calculated as mentioned in the ProblemStatement.pdf)
    ##			for instance, if there are two ArUco markers with id 1 and 2 with angles 120 and 164 respectively, the 
    ##			function should return: {1: 120 , 2: 164}

    ArUco_marker_angles = {}
    cnt = 0
    ans_x = 0
    ans_y = 0
    midpoint_x = 0
    midpoint_y = 0
    right_x = 0
    right_y = 0
    for i in Detected_ArUco_markers:
        for j in Detected_ArUco_markers[i]:
            if (cnt%4) == 0:
                ans_x = j[0,]
                ans_y = j[1,]
                midpoint_x = ans_x
                midpoint_y = ans_y
                cnt = 1
            else:
                cnt += 1
                if cnt == 2:
                    midpoint_x = (midpoint_x + j[0,])/2
                    midpoint_y = (midpoint_y + j[1,])/2
                    right_x = j[0,]
                    right_y = j[1,]
                ans_x += j[0,]
                ans_y += j[1,]
        ans_x = int(ans_x/4)
        ans_y = int(ans_y/4)
        midpoint_x = int(midpoint_x)
        midpoint_y = int(midpoint_y)
        cv2.circle(img,(ans_x,ans_y), 5, (0,0,255), -1)
        cv2.line(img,(ans_x,ans_y),(midpoint_x,midpoint_y),(255,0,0),5)
        midpoint_x = midpoint_x - ans_x
        midpoint_y = -(midpoint_y - ans_y)

        ans_x = 0
        ans_y = 0
        id_str = str(i)
        font = cv2.FONT_HERSHEY_SIMPLEX
        if midpoint_y < 0:
            ang = str(int((360-np.arccos(np.inner([1,0],[midpoint_x,midpoint_y])/np.linalg.norm([midpoint_x,midpoint_y]))*180/np.pi))),
            ArUco_marker_angles[i] = ang
        else:
            ang = str(int((np.arccos(np.inner([1,0],[midpoint_x,midpoint_y])/np.linalg.norm([midpoint_x,midpoint_y]))*180/np.pi))),
            ArUco_marker_angles[i] = ang
    return ArUco_marker_angles	## returning the angles of the ArUco markers in degrees as a dictionary


def mark_ArUco(img,Detected_ArUco_markers,ArUco_marker_angles):
    ## function to mark ArUco in the test image as per the instructions given in problem_statement.pdf 
    ## arguments: img is the test image 
    ##			  Detected_ArUco_markers is the dictionary returned by function detect_ArUco(img)
    ##			  ArUco_marker_angles is the return value of Calculate_orientation_in_degree(Detected_ArUco_markers)
    ## return: image namely img after marking the aruco as per the instruction given in Problem_statement.pdf

    ## enter your code here ##
    for i in Detected_ArUco_markers:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,ArUco_marker_angles[i][0],(int(Detected_ArUco_markers[i][2][0]),int(Detected_ArUco_markers[i][2][1])), font, 0.5,(0,255,0),2,cv2.LINE_AA)
        cv2.circle(img,(Detected_ArUco_markers[i][3][0],Detected_ArUco_markers[i][3][1]), 5, (255,255,255), -1)
        cv2.circle(img,(Detected_ArUco_markers[i][2][0],Detected_ArUco_markers[i][2][1]), 5, (180,105,255), -1)
        cv2.circle(img,(Detected_ArUco_markers[i][1][0],Detected_ArUco_markers[i][1][1]), 5, (0,255,0), -1)
        cv2.circle(img,(Detected_ArUco_markers[i][0][0],Detected_ArUco_markers[i][0][1]), 5, (128,128,128), -1)
    return img


