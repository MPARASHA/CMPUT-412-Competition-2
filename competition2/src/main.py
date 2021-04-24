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
from bandit import solve_bandit, epsilon_greedy_policy

from parseImage import getFinalRoom, getbanditInfo, getrch, getrooms, getShapesInfo, path_to_bandit_img, path_to_rch_lobby, path_to_room_fig, path_to_shapes_figure, path_to_maze_figure

# rospy for the subscriber
import rospy
# ROS Image message
from sensor_msgs.msg import Image
# ROS Image message -> OpenCV2 image converter
from cv_bridge import CvBridge, CvBridgeError
# OpenCV2 for saving an image
import cv2

from rotate import rotate

from PIL import Image as Im
import pytesseract
import argparse
import os

# Instantiate CvBridge
bridge = CvBridge()

preproc = "thresh"



path_to_sign_text = 'camera_image.png'
alldetected = []
def detectText():

    detected = False
    # load the example image and convert it to grayscale
    image = cv2.imread(path_to_sign_text)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image
    if preproc == "thresh":
        gray = cv2.threshold(gray, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise
    elif preproc == "blur":
        gray = cv2.medianBlur(gray, 3)
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file
    text = pytesseract.image_to_string(Im.open(filename))

    text.replace("\n", "")
    text.replace("\x0c", "")
    text.replace(" ", "")

    textList = text.split()


    if(text != '' and  len(textList) != 0):
        detected = True 

    return detected

def image_callback(msg):
    # print("Received an image!")
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError:
        print(e)
    
    # Save your OpenCV2 image as a jpeg 
    cv2.imwrite('camera_image.png', cv2_img)

    alldetected.append(detectText())


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

label = "roomc" + banditroomLetter

service_req_nav.label = label
result = service_nav(service_req_nav)
# Print the result given by the service called
print(result.message)
end = time.time()

completion_time = end - start3

start = time.time()

print("\nTotal Time Taken to Go to Bandit Room: {} seconds\n\n".format(completion_time))

print("\nDetecting Sign...\n")

image_topic = "/camera/rgb/image_raw"
# Set up your subscriber and define its callback
rospy.Subscriber(image_topic, Image, image_callback)

rotate(360)

time.sleep(10)

end = time.time()

completion_time = end - start


print("\nTotal Time Taken to detect sign: {} seconds\n\n".format(completion_time))

start = time.time()

print("\n\nReading the Passcode and Number of arms from the PNG File...\n")

passcode, narm = getbanditInfo()

end = time.time()

completion_time = end - start


print("\nTotal Time Taken to read Bandit Info: {} seconds\n\n".format(completion_time))

print("\nStarting to Solve Bandit...\n")


mazeroom, where = solve_bandit(passcode, narm)


ind = np.where(rooms == mazeroom)[0]

mazeroomLetter = roomsLetters[ind[0]]

print("\nMaze Room:", mazeroomLetter, "\n\n")


end = time.time()

completion_time = end - start3

print("\nTotal Time for Step 3: {} seconds\n\n".format(completion_time))

# **************************** STEP 3 ENDS HERE **************************************************************

print("\n\nSKIPPING MAZE........\n\n")
# Add maze above



passcode, fr = getFinalRoom()

ind = np.where(rooms == fr)[0]

finalroomLetter = roomsLetters[ind[0]]

print("\n\nFinal Room:", finalroomLetter, "\n")

label = "roomc" + finalroomLetter

service_req_nav.label = label
result = service_nav(service_req_nav)
# Print the result given by the service called
print(result.message)

print("\nWhere: ", where)

end = time.time()

completion_time = end - start1

print("\nTotal Time for Demo: {} seconds\n\n".format(completion_time))







