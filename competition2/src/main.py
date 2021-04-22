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
from parseImage import getbanditInfo, getrch, getrooms, getShapesInfo, path_to_bandit_img, path_to_rch_lobby, path_to_room_fig, path_to_shapes_figure



def localize():

    try:
        # Testing our function
        rotate(360)
        pass
    except rospy.ROSInterruptException:
        pass

    time.sleep(10)

    # Wait for the service client /trajectory_by_name to be running
    rospy.wait_for_service('/global_localization')
    # Create the connection to the service
    service_particles = rospy.ServiceProxy('/global_localization', Empty)
    # Create an object of type TrajByNameRequest 
    service_req_particles = EmptyRequest()
    # Fill the variable traj_name of this object with the desired value

    # Send through the connection the name of the trajectory to be executed by the robot
    service_particles(service_req_particles)
    # Print the result given by the service called

    try:
        # Testing our function
        rotate(360)
        pass
    except rospy.ROSInterruptException:
        pass





# Initialise a ROS node with the name service_client
rospy.init_node('main_competition2')

# ************************* STEP 1 STARTS HERE *********************************************

localize()

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

# **************************** STEP 1 ENDS HERE **************************************************************



