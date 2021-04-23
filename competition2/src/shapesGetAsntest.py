from competition2.srv import ShapesAnswer
import rospy
from parseImage import getbanditInfo, getrch, getrooms, getShapesInfo, path_to_bandit_img, path_to_rch_lobby, path_to_room_fig, path_to_shapes_figure
import time
import numpy as np

rch = getrch()

start = time.time()
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

completion_time = end - start

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

print(ind)

banditroomLetter = roomsLetters[ind[0]]

print("\nBandit Room:", banditroomLetter)