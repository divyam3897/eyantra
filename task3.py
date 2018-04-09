import sys
import vrep
import time
import math

vrep.simxFinish(-1)
clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)
if clientID!=-1:
    print "connected to remote api server"
else:
    print 'connection not successful'
    sys.exit("could not connect")

emptyBuff = bytearray()
returnCode,truck_handle=vrep.simxGetObjectHandle(clientID,'TRUCK',vrep.simx_opmode_oneshot_wait)
returnCode, position1=vrep.simxGetObjectPosition(clientID,truck_handle,-1,vrep.simx_opmode_blocking)
returnCode = vrep.simxSetObjectPosition(clientID,truck_handle,-1,(2,2,0.2),vrep.simx_opmode_blocking)
print(position1)
#end of simulation
#vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot)
#time.sleep(0.1)
