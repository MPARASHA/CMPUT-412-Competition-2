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

import sys
from std_srvs.srv import Empty, EmptyRequest
from rotate import rotate



def localize():

    # Wait for the service client /trajectory_by_name to be running
    rospy.wait_for_service('/global_localization')
    # Create the connection to the service
    service = rospy.ServiceProxy('/global_localization', Empty)
    # Create an object of type TrajByNameRequest 
    service_req = EmptyRequest()
    # Fill the variable traj_name of this object with the desired value

    # Send through the connection the name of the trajectory to be executed by the robot
    service(service_req)
    # Print the result given by the service called

    try:
        # Testing our function
        rotate(360)
        pass
    except rospy.ROSInterruptException:
        pass





# Initialise a ROS node with the name service_client
rospy.init_node('main_competition2')

time.sleep(5)

localize()

print("\n\nLOCALIZED\n\n")

# Go to loby
print("\n\nGOING TO THE LOBBY...\n\n")
# Wait for the service client /get_coordinates to be running
rospy.wait_for_service('/get_coordinates')
# Create the connection to the service
service = rospy.ServiceProxy('/get_coordinates', MyServiceMessage)
# Create an object of type TrajByNameRequest
service_req = MyServiceMessageRequest()
# Fill the variable traj_name of this object with the desired value
service_req.label = "lobby"
# Send through the connection the name of the trajectory to be executed by the robot
result = service(service_req)
# Print the result given by the service called
print(result.message)



