#! /usr/bin/env python

import rospy
from my_localization.srv import MyServiceMessage, MyServiceMessageResponse, MyServiceMessageRequest
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseAction, MoveBaseResult, MoveBaseGoal
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseWithCovarianceStamped

import actionlib
from actionlib_msgs.msg import GoalStatus

import time
import os
import rosparam

import numpy as np

import sys
from std_srvs.srv import Empty, EmptyRequest
from rotate import rotate
from competition2.srv import ShapesAnswer

from parseImage import getbanditInfo, getrch, getrooms, getShapesInfo, path_to_bandit_img, path_to_rch_lobby, path_to_room_fig, path_to_shapes_figure

SKIP_LOC = True  

def localize():
    print("\n\nLOCALIZING...\n")
    # try:
    #     # Testing our function
    #     rotate(360)
    #     pass
    # except rospy.ROSInterruptException:
    #     pass

    # time.sleep(10)


    # Wait for the service client /trajectory_by_name to be running
    rospy.wait_for_service('/global_localization')
    # Create the connection to the service
    service_particles = rospy.ServiceProxy('/global_localization', Empty)
    # Create an object of type TrajByNameRequest 
    service_req_particles = EmptyRequest()
    # Fill the variable traj_name of this object with the desired value

    print("\nDistributing Paricles...\n")
    # Send through the connection the name of the trajectory to be executed by the robot
    service_particles(service_req_particles)
    # Print the result given by the service called

    

    rotate(360)


    time.sleep(10)

    # print("\nDistributing Paricles...\n")

    # service_particles(service_req_particles)

    # # TODO go to hallway
    # rotate(360)
    # time.sleep(10)



# Initialise a ROS node with the name service_client
rospy.init_node('main_competition2')
start1 = time.time()
start = time.time()

# ************************* STEP 1 STARTS HERE *********************************************
if(not SKIP_LOC):
    localize()
else:
    time.sleep(15) # TIME TO GIVE MANUAL POSE ESTIMATE
    rotate(360)
    time.sleep(10)


print("\n\nLOCALIZED\n\n")

# Go to loby
print("\n\nGOING TO THE LOBBY...\n\n")
# Wait for the service client /get_coordinates to be running
rospy.wait_for_service('/get_coordinates')
# Create the connection to the service
service_nav = rospy.ServiceProxy('/get_coordinates', MyServiceMessage)

service_req_nav = MyServiceMessageRequest()

# These two lines for navigation
service_req_nav.label = "lobby"
result = service_nav(service_req_nav)
# Print the result given by the service called
print(result.message)
end = time.time()

completion_time = end - start

print("\nTotal Lobby Travel Time: {} seconds\n\n".format(completion_time))

print("Reading from PNG file using Tesseract-OCR\n\n")
start = time.time()
rch = getrch()

roomsLetters = ['a', 'b','c', 'd', 'e', 'f',  'i', 'j', 'g','h', 'k', 'l', 'm', 'n', 'o', 'p', 'q']

rooms = np.array(getrooms())

print("\n\n")

print("The room assignments are as follows: \n")

for i in range(17):
    rooms[i] = int(rooms[i])
    print(roomsLetters[i], ":\t", rooms[i])

print("\n\n")

if rch == "highest":

    ind = np.argmax(rooms)
else:
    ind = np.argmin(rooms)

shaperoomLetter = roomsLetters[ind]

print("Shapes Room: ", roomsLetters[ind], "\n\n")


end = time.time()

completion_time = end - start

print("\nTotal Room Assignment Time: {} seconds\n\n".format(completion_time))

completion_time = end - start1

print("\nTotal Step 1 Time: {} seconds\n\n".format(completion_time))

# **************************** STEP 1 ENDS HERE **************************************************************

# **************************** STEP 2 STARTS HERE ************************************************************
start2 = time.time()
print("\nSKIPPING STEP 2 - SHAPES ROOM\n")
rospy.wait_for_service("/shapes_answer")
shapes_answer_client = rospy.ServiceProxy("/shapes_answer", ShapesAnswer)

response = shapes_answer_client(0)

banditroom = response.room

ind = np.where(rooms == banditroom)[0]

banditroomLetter = roomsLetters[ind[0]]

print("\nBandit Room:", banditroomLetter, "\n\n")

end = time.time()

completion_time = end - start2

print("\nTotal Step 2 Time: {} seconds\n\n".format(completion_time))

# **************************** STEP 2 ENDS HERE **************************************************************

# **************************** STEP 3 STARTS HERE ************************************************************

start3 = time.time()

# TODO GO TO BANDIT ROOM, FIND SIGN AND SOLVE BANDIT
