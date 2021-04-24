#!/usr/bin/env python
from robot_node import TurtlebotTopic
import numpy as np
import time 

from VelocityController import VelocityController, OdometryReader, go_to, normalize

class turtlebot_control():
    def __init__(self,speed,time):
        self.robot=TurtlebotTopic()
        self.right_direct = 'clockwise'
        self.left_direct = 'counter_clockwise'
        self.right_speed= 0.25
        self.right_time = 6.2
        self.left_speed= 0.22
        self.left_time = 7
        self.out_maze = False
    def get_foward_dist(self):
        return self.robot.get_distance(360)
    def get_right_dist(self):
        return self.robot.get_distance(90)
    def get_left_dist(self):
        return self.robot.get_distance(180)

    def move(self):
        # self.robot.goto_pos(1.5,-4)
        # self.robot.goto_pos(1.5,-8)
        # self.robot.goto_pos(1.5,-11.5)
        self.robot.stop_robot()
    def play_maze(self):
        self.robot.move_straight()
        self.robot.move_straight()
        self.robot.move_straight()
        self.robot.stop_robot()
        # time.sleep(1)
        # self.robot.turn_angle(self.left_direct,self.left_speed,self.left_time)
        # time.sleep(2)
        # self.robot.move_straight()
        # self.robot.move_straight()
        # self.robot.stop_robot()
        # print(self.get_left_dist())
        # print(self.get_foward_dist())
        # print(self.get_right_dist())
        
    
        # while self.get_right_dist() < 1.2 and self.get_foward_dist() > 0.5:
        #     print(self.get_right_dist())
        #     print(self.get_left_dist())
        #     self.robot.move_straight()
        # self.robot.stop_robot()
        # if self.get_right_dist() < 0.6 and self.get_foward_dist() <= 0.35:
        #     self.robot.turn_angle(self.right_direct,self.right_speed,self.right_time)
        #     print(self.get_right_dist())
        #     print(self.get_left_dist())



       
        
        

        
turtlebot= turtlebot_control( speed=0.25, time = 7.7)
turtlebot.play_maze()