import numpy as np
import cv2
import cv2.aruco as aruco
import time
from ArUco_library import *
#from task1_cb import *
import vrep

# Frame size = 1280 * 720
# Working Arena's dimensions = 2.4384 * 1.798
# Total Arena = 2.7432 * 2.1336
# l_distance, w_distance calculated using workingArena/FrameSize
l_distance = 0.0019
w_distance = 0.0024

vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)
if clientID!=-1:
    print "connected to remote api server"
else:
    print 'connection not successful'
    sys.exit("could not connect")

returnCode = vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)
emptyBuff = bytearray()
returnCode,truck_handle=vrep.simxGetObjectHandle(clientID,'TRUCK',vrep.simx_opmode_oneshot_wait)
returnCode,reference1=vrep.simxGetObjectHandle(clientID,'Reference1',vrep.simx_opmode_oneshot_wait)
returnCode,reference2=vrep.simxGetObjectHandle(clientID,'Reference2',vrep.simx_opmode_oneshot_wait)
returnCode,reference3=vrep.simxGetObjectHandle(clientID,'Reference3',vrep.simx_opmode_oneshot_wait)
returnCode,reference4=vrep.simxGetObjectHandle(clientID,'Reference4',vrep.simx_opmode_oneshot_wait)

vidcap = cv2.VideoCapture("robot1.avi")
width = vidcap.get(3)
height = vidcap.get(4)
while(vidcap.isOpened()):
    success,image = vidcap.read()
    cv2.waitKey(5)
    if success == True:
        cv2.imshow("Frame" , image)
        Detected_ArUco_markers = detect_ArUco(image)								    
        try:
            # Detect all aruco markers using aruco library of task 1.1
            value = Detected_ArUco_markers[1][0,][0]
            if value != None:
                # Reference points with x1 = top left, x3 = bottom right, x2 = top right, x4 = bottom left
                x1 = Detected_ArUco_markers[10][1,][0] * l_distance
                y1 = Detected_ArUco_markers[10][1,][1] * w_distance
                x2 = (Detected_ArUco_markers[11][2,][0] - x1) * l_distance
                y2 = (Detected_ArUco_markers[11][2,][1] - y1) * w_distance
                x = (Detected_ArUco_markers[1][0,][0] - x1) * l_distance
                y = (Detected_ArUco_markers[1][0,][1] - y1) * w_distance
                print(x1,y1,x2,y2)
                returnCode = vrep.simxSetObjectPosition(clientID,reference1,-1,(x1,y1,0),vrep.simx_opmode_blocking)
                returnCode = vrep.simxSetObjectPosition(clientID,reference2,-1,(x2,y1,0),vrep.simx_opmode_blocking)
                returnCode = vrep.simxSetObjectPosition(clientID,reference3,-1,(x2,y2,0),vrep.simx_opmode_blocking)
                returnCode = vrep.simxSetObjectPosition(clientID,reference4,-1,(x1,y2,0),vrep.simx_opmode_blocking)
                angle = Calculate_orientation_in_degree(Detected_ArUco_markers,image)			
                angle[1] = float(angle[1][0])
                returnCode,inints,inflts,instrs,inbuffs = vrep.simxCallScriptFunction(clientID,'LuaFunctions',vrep.sim_scripttype_childscript,'add_cyl',[],[x,y,0.,0,0,math.radians(angle[1])],[],emptyBuff,vrep.simx_opmode_oneshot_wait)
            else:
                continue
        except KeyError:
            pass
    else:
        cv2.destroyAllWindows()
        vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot)
        break;

