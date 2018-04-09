## Task 1.2 - Path Planning in V-REP ##
# Import modules
import sys
import vrep
import time
import math


# Write a function here to choose a goal.
def chooseGoal(goal,pos):
    a=goal[:]
    returnCode, cyl_pos = vrep.simxGetObjectPosition(clientID, a[0], -1, vrep.simx_opmode_blocking)
    min_dis = math.sqrt((pos[0]-cyl_pos[0])**2 + (pos[1]-cyl_pos[1])**2)
    index=0
    for i in range(len(a)-1):
        returnCode, cyl_pos = vrep.simxGetObjectPosition(clientID, a[i+1], -1, vrep.simx_opmode_blocking)
        distance = math.sqrt((pos[0]-cyl_pos[0])**2 + (pos[1]-cyl_pos[1])**2)
        #print distance
        if distance<=min_dis:
            min_dis=distance
            index=i
    point=goal.pop(index)
    return point


# Write a function(s) to set/reset goal and other so that you can iterate the process of path planning
def setGoal(cyl_handle,prev_cyl_handle):
    global last_visited
    returnCode, cyl_pos = vrep.simxGetObjectPosition(clientID,cyl_handle,-1,vrep.simx_opmode_blocking)
    returnCode = vrep.simxSetObjectPosition(clientID,goal_dummy_handle,-1,(cyl_pos[0],cyl_pos[1],cyl_pos[2]),vrep.simx_opmode_blocking)

    returnCode, rob_pos = vrep.simxGetObjectPosition(clientID,robot_handle,-1,vrep.simx_opmode_buffer)
    returnCode = vrep.simxSetObjectPosition(clientID,start_dummy_handle,-1,(rob_pos[0],rob_pos[1],rob_pos[2]),vrep.simx_opmode_blocking)
    
    returnCode, pos = vrep.simxGetObjectPosition(clientID,start_dummy_handle,-1,vrep.simx_opmode_blocking)
    returnCode, pos = vrep.simxGetObjectPosition(clientID,goal_dummy_handle,-1,vrep.simx_opmode_blocking)
    
    returnCode, inints,inflts,instrs,inbuffs = vrep.simxCallScriptFunction(clientID,'LuaFunctions',vrep.sim_scripttype_childscript,'remove_cyl',[cyl_handle,-1],[],[],emptyBuff,vrep.simx_opmode_oneshot_wait)
    if prev_cyl_handle!=-1:
        returnCode,inints,inflts,instrs,inbuffs = vrep.simxCallScriptFunction(clientID,'LuaFunctions',vrep.sim_scripttype_childscript,'add_cyl',[prev_cyl_handle,-1],[],[],emptyBuff,vrep.simx_opmode_oneshot_wait)
    last_visited = cyl_handle
    return


# Write a function to create a path from Start to Goal
def createPath():
    time.sleep(0.5)
    returnCode,path_plan,inflts,instrs,inbuffs = vrep.simxCallScriptFunction(clientID,'LuaFunctions',vrep.sim_scripttype_childscript,'path',[],[],[],emptyBuff,vrep.simx_opmode_oneshot_wait)
    return



# Write a function to make the robot move in the generated path. 
# Make sure that you give target velocities to the motors here in python script rather than giving in lua.
# Note that the your algorithm should also solve the conditions where partial paths are generated.
def moveBot(goal):
    dest=10
    wheel_seperation = 0.208
    diameter = 0.0701
    wheel_radius = diameter/2
    returnCode, goal_pos = vrep.simxGetObjectPosition(clientID, goal, -1, vrep.simx_opmode_blocking)
    pos_on_path = 0
    distance = 0
    while(dest > 0.25 and pos_on_path<1):
        returnCode, rob_pos = vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_buffer)
        dest = math.sqrt((rob_pos[0]-goal_pos[0])**2 + (rob_pos[1]-goal_pos[1])**2)
        returnCode,inints,path_pos,instrs,inbuffs = vrep.simxCallScriptFunction(clientID,'LuaFunctions',vrep.sim_scripttype_childscript,'calc_path_pos',[],[pos_on_path],[],emptyBuff,vrep.simx_opmode_oneshot_wait)
        returnCode,inints,path_pos,instrs,inbuffs = vrep.simxCallScriptFunction(clientID,'LuaFunctions',vrep.sim_scripttype_childscript,'path_pos_transform',[],path_pos,[],emptyBuff,vrep.simx_opmode_oneshot_wait)
    
        distance = math.sqrt(path_pos[0]**2 + path_pos[1]**2)
        phi = math.atan2(path_pos[1],path_pos[0])
    
        if(pos_on_path < 1):
            v_des = 0.1
            w_des = 0.8 * phi
        else:
            v_des = 0
            w_des = 0
        
        v_r = v_des + (wheel_seperation/2) * w_des
        v_l = v_des - (wheel_seperation/2) * w_des
        
        w_l = v_l/wheel_radius
        w_r = v_r/wheel_radius
        
        returnCode = vrep.simxSetJointTargetVelocity(clientID, leftjoint_handle, w_l, vrep.simx_opmode_streaming)
        returnCode = vrep.simxSetJointTargetVelocity(clientID, rightjoint_handle, w_r, vrep.simx_opmode_streaming)
        print w_l, w_r
    
        if(distance < 0.1):
            pos_on_path = pos_on_path + 0.1
    return




################ Initialization of handles. Do not change the following section ###################################

vrep.simxFinish(-1)

clientID=vrep.simxStart('127.0.0.1',19997,True,True,5000,5)

if clientID!=-1:
	print "connected to remote api server"
else:
	print 'connection not successful'
	sys.exit("could not connect")

returnCode,robot_handle=vrep.simxGetObjectHandle(clientID,'CollectorBot',vrep.simx_opmode_oneshot_wait)
returnCode,leftjoint_handle=vrep.simxGetObjectHandle(clientID,'left_joint',vrep.simx_opmode_oneshot_wait)
returnCode,rightjoint_handle=vrep.simxGetObjectHandle(clientID,'right_joint',vrep.simx_opmode_oneshot_wait)
returnCode,start_dummy_handle = vrep.simxGetObjectHandle(clientID,'Start',vrep.simx_opmode_oneshot_wait)
returnCode,goal_dummy_handle = vrep.simxGetObjectHandle(clientID,'Goal',vrep.simx_opmode_oneshot_wait)

returnCode,cylinder_handle1=vrep.simxGetObjectHandle(clientID,'Cylinder1',vrep.simx_opmode_oneshot_wait )
returnCode,cylinder_handle2=vrep.simxGetObjectHandle(clientID,'Cylinder2',vrep.simx_opmode_oneshot_wait )
returnCode,cylinder_handle3=vrep.simxGetObjectHandle(clientID,'Cylinder3',vrep.simx_opmode_oneshot_wait )
returnCode,cylinder_handle4=vrep.simxGetObjectHandle(clientID,'Cylinder4',vrep.simx_opmode_oneshot_wait )
returnCode,cylinder_handle5=vrep.simxGetObjectHandle(clientID,'Cylinder5',vrep.simx_opmode_oneshot_wait )
returnCode,cylinder_handle6=vrep.simxGetObjectHandle(clientID,'Cylinder6',vrep.simx_opmode_oneshot_wait )
returnCode,cylinder_handle7=vrep.simxGetObjectHandle(clientID,'Cylinder7',vrep.simx_opmode_oneshot_wait )
returnCode,cylinder_handle8=vrep.simxGetObjectHandle(clientID,'Cylinder8',vrep.simx_opmode_oneshot_wait )

cylinder_handles=[cylinder_handle1,cylinder_handle2,cylinder_handle3,cylinder_handle4,cylinder_handle5,cylinder_handle6,cylinder_handle7,cylinder_handle8]

#####################################################################################################################

# Write your code here
returnCode = vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)
emptyBuff = bytearray()
goals=cylinder_handles[0:5]
last_visited=-1
for i in range(len(goals)):
    returnCode, rob_pos = vrep.simxGetObjectPosition(clientID, robot_handle, -1, vrep.simx_opmode_streaming)
    goal=chooseGoal(goals,rob_pos)
    setGoal(goal,last_visited)
    createPath()
    moveBot(goal)
    returnCode = vrep.simxSetJointTargetVelocity(clientID, leftjoint_handle, 0, vrep.simx_opmode_streaming)
    returnCode = vrep.simxSetJointTargetVelocity(clientID, rightjoint_handle, 0, vrep.simx_opmode_streaming)
time.sleep(2)

################     Do not change after this #####################

#end of simulation
vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot)
time.sleep(0.1)
