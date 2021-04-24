#!/usr/bin/env python
import rospy
# because when we seach for the topic info we can see the type then we import the topic we want from the msg type
from nav_msgs.msg import Odometry 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import time
from geometry_msgs.msg import Point
from math import atan2
import math
from sensor_msgs.msg import Image
import rospy, cv2, cv_bridge
import numpy  as np
from cv_bridge import CvBridge, CvBridgeError

class TurtlebotTopic():
    def __init__(self):
        rospy.init_node('Turtlebot_topic_node', anonymous=True)
        self.subOdome = rospy.Subscriber('/odom',Odometry,self.Odom_callback)
        self.sub = rospy.Subscriber('/kobuki/laser/scan',LaserScan,self.callback)
        self.TurtlebotPublisher = rospy.Publisher('/cmd_vel',Twist,queue_size= 10)
        self.Turtle_msg = Twist()
        self.laser_msg  = LaserScan()
        self.odom_msg = Odometry()
        self.odom_x = 0
        self.odom_y = 0
        self.odom_theta =0
        self.shape = None
        self.color = None
        self.is_wanted = False
        self.start_detect = False 
        self.start_shape_detect = False 
        self.rate = rospy.Rate(1)
        self.roll = self.pitch = 0.0


        
    def get_shape(self):
        return self.shape

    def get_color(self):
        return self.color

    def move_straight(self):
        # going foward so we give an initial volocity 
        self.Turtle_msg.linear.x = 0.2
        self.Turtle_msg.linear.y = 0.2
        self.Turtle_msg.linear.z = 0
        self.Turtle_msg.angular.x = 0
        self.Turtle_msg.angular.y = 0
        self.Turtle_msg.angular.z = 0
        i=0
        while i <=2:
            self.TurtlebotPublisher.publish(self.Turtle_msg)
            self.rate.sleep()
            i+=1

    def move_backward(self):
        # going foward so we give an initial volocity 
        self.Turtle_msg.linear.x = -1
        self.Turtle_msg.linear.y = 0
        self.Turtle_msg.linear.z = 0
        self.Turtle_msg.angular.x = 0
        self.Turtle_msg.angular.y = 0
        self.Turtle_msg.angular.z = 0
        self.TurtlebotPublisher.publish(self.Turtle_msg)

    
    def stop_robot(self):
        self.Turtle_msg.linear.x = 0
        self.Turtle_msg.angular.z = 0
        self.Turtle_msg.linear.y = 0
        self.TurtlebotPublisher.publish(self.Turtle_msg)

    
    def get_distance(self, ang):
        time.sleep(1)
        return self.laser_msg.ranges[ang]
        
    
    def turn_angle(self,direc,speed,time):

        self.Turtle_msg.linear.x = 0
        self.Turtle_msg.linear.y = 0
        self.Turtle_msg.linear.z = 0
        self.Turtle_msg.angular.x = 0
        self.Turtle_msg.angular.y = 0

        if direc == "clockwise":
            self.Turtle_msg.angular.z = -speed
        else:
            self.Turtle_msg.angular.z = speed

        i = 0
        while i <= time:
            self.TurtlebotPublisher.publish(self.Turtle_msg)
            i+=1
            self.rate.sleep()
        self.stop_robot()

    def callback(self,msg):
        self.laser_msg = msg

    def Odom_callback(self,msg):
        self.odom_x = msg.pose.pose.position.x
        self.odom_y = msg.pose.pose.position.y
        rot  = msg.pose.pose.orientation
        (self.roll, self.pitch, self.odom_theta) = euler_from_quaternion([rot.x,rot.y,rot.z,rot.w])

    def goto_pos(self,des_x,des_y):
        #print("Test1")
        cw = False 
        sm3 = False 
        trigger = True
        
        while not rospy.is_shutdown():
            inc_x = des_x - self.odom_x
            inc_y = des_y - self.odom_y
                
            if abs(inc_x) < 0.2 and abs(inc_y) <0.2:
                self.rate.sleep()
                return

            angle_to_goal = atan2(inc_y,inc_x)
            angle_diff = angle_to_goal - self.odom_theta
            if trigger  == True:
                #print("Diff angle: " + str(angle_diff))
                if abs(angle_diff) >3 :
                    sm3 = True 
                    if angle_diff > 0:
                        print("here")
                        cw = "cw"
                    elif angle_diff <0:
                        cw = "ccw" 
                else:
                    if angle_diff > 0:
                        print("here")
                        cw = "cw"
                    elif angle_diff <0:
                        cw = "ccw" 
                    sm3 = False
                trigger = False 

            if not sm3:
                if cw == "cw" :
                    if abs(angle_diff) > 0.3:
                        #print("Text2")
                        #print(abs(angle_to_goal - self.odom_theta) )
                        
                        self.Turtle_msg.linear.x = 0.0
                        self.Turtle_msg.angular.z = 0.2
                        #print("Loc 1")
                    else:
                        #print("Text3")
                        self.Turtle_msg.linear.x = 0.35
                        self.Turtle_msg.linear.y = 0.35
                        self.Turtle_msg.angular.z = 0
                        trigger = True 
                elif cw == "ccw":
                    if abs(angle_diff) > 0.3:
                    
                        #print("Text2")
                        #print(abs(angle_to_goal - self.odom_theta) )
                        self.Turtle_msg.linear.x = 0.0
                        self.Turtle_msg.angular.z = -0.2
                        #print("Loc 2")
                    else:
                        #print("Text3")
                        self.Turtle_msg.linear.x = 0.5
                        self.Turtle_msg.linear.y = 0.5
                        self.Turtle_msg.angular.z = 0
                        trigger = True 

            else:
                if abs(angle_diff) > 0.3:
                    #print("Text2")
                    #print(abs(angle_to_goal - self.odom_theta) )
                    
                    self.Turtle_msg.linear.x = 0.0
                    self.Turtle_msg.angular.z = 0.2
                    #print("Loc 3")
                else:
                    #print("Text3")
                    self.Turtle_msg.linear.x = 0.5
                    self.Turtle_msg.linear.y = 0.5
                    self.Turtle_msg.angular.z = 0
                    trigger = True 

            self.TurtlebotPublisher.publish(self.Turtle_msg)





def main():
    turtlebotMove = TurtlebotTopic()
    turtlebotMove.move_straight()

if __name__ == '__main__':
    main()