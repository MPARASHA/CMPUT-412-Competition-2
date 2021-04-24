#! /usr/bin/env python

# import ros stuff
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf import transformations

import math
pub_ = None
trigger = False 
regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}
state_ = 0


state_dict_ = {
    0: 'find the wall',
    1: 'turn left',
    2: 'follow the wall',
    3: 'out of maze'
}
def clbk_laser(msg):
    global regions_
    regions_ = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:713]), 10),
    }
    
    take_action()


def change_state(state):
    global state_, state_dict_
    if state is not state_:
        print( 'Wall follower - [%s] - %s' % (state, state_dict_[state]))
        state_ = state

####################################### Follow the right wall ###################################

# def take_action():
#     global regions_
#     regions = regions_
#     msg = Twist()
#     linear_x = 0
#     angular_z = 0
    
#     state_description = ''
    
#     d = 0.6
    
#     if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
#         state_description = 'case 1 - nothing'
#         change_state(0)
#     # elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
#     #     state_description = 'case 2 - front'
#     #     print(regions_)
#     #     change_state(1)
#     elif regions['front'] > d and regions['fleft'] > d and regions['fright'] < d:
#         state_description = 'case 3 - fright'
#         change_state(2)
#     elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
#         state_description = 'case 4 - fleft'
#         change_state(0)
#     elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
#         state_description = 'case 5 - front and fright'
#         print(regions_)
#         change_state(1)
#     # elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
#     #     state_description = 'case 6 - front and fleft'
#     #     print(regions_)
#     #     change_state(1)
#     elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
#         state_description = 'case 7 - front and fleft and fright'
#         print(regions_)
#         change_state(1)
#     elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
#         state_description = 'case 8 - fleft and fright'
#         change_state(2)
#     elif regions['front'] > 40:
#         change_state(3)

#     else:
#         state_description = 'unknown case'
#         rospy.loginfo(regions)


# def find_wall():
#     msg = Twist()
#     msg.linear.x = 0.3
#     msg.angular.z = -0.3
#     print("#################")
#     return msg

# def turn_left():
#     msg = Twist()
#     msg.angular.z = 0.7
#     return msg

# def turn_right():
#     msg = Twist()
#     msg.linear.x = 0.15
#     msg.angular.z = -0.5
#     return msg


# def follow_the_wall():
#     global regions_
    
#     msg = Twist()
#     msg.linear.x = 0.8
#     return msg
# def stop_robot():
#     msg = Twist()
#     msg.linear.x = 0
#     msg.linear.y = 0
#     msg.angular.z = 0
#     return msg


# def main():
#     global pub_,trigger
#     out_maze = False
    
#     rospy.init_node('reading_laser')
    
#     pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
#     sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, clbk_laser)
    
#     rate = rospy.Rate(20)
#     while not out_maze:
#         msg = Twist()
#         if state_ == 0 and trigger == False:
#             msg = find_wall()
#         elif state_  ==0 and trigger == True:
#             msg = turn_right()
            
#         elif state_ == 1:
#             msg = turn_left()
#             trigger = True 
#         elif state_ == 2:
#             msg = follow_the_wall()
#             trigger = True 
#             pass
#         elif state ==3:
#             msg = stop_robot()
#             out_maze = True 
#         else:
#             rospy.logerr('Unknown state!')
        
#         pub_.publish(msg)
        
#         rate.sleep()
##################################### Follow the Left wall ############################

def take_action():
    global regions_
    regions = regions_
    msg = Twist()
    linear_x = 0
    angular_z = 0
    
    state_description = ''
    
    d = 0.6
    
    if regions['front'] > d and regions['fleft'] > d and regions['fright'] > d:
        state_description = 'case 1 - nothing'
        change_state(1)
    # elif regions['front'] < d and regions['fleft'] > d and regions['fright'] > d:
    #     state_description = 'case 2 - front'
    #     change_state(1)
    # elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
    #     state_description = 'case 3 - fright'
    #     change_state(1)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 4 - fleft'
        change_state(2)
    elif regions['front'] < d and regions['fleft'] > d and regions['fright'] < d:
        state_description = 'case 5 - front and fright'
        change_state(1)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] > d:
        state_description = 'case 6 - front and fleft'
        change_state(0)
    elif regions['front'] < d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 7 - front and fleft and fright'
        change_state(0)
    elif regions['front'] > d and regions['fleft'] < d and regions['fright'] < d:
        state_description = 'case 8 - fleft and fright'
        change_state(2)
    elif regions['front'] > 40:
        change_state(3)

    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)


def find_wall():
    msg = Twist()
    msg.linear.x = 0.3
    msg.angular.z = 0.3
    print("#################")
    return msg

def turn_left():
    msg = Twist()
    msg.linear.x = 0.15
    msg.angular.z = 0.7
    return msg

def turn_right():
    msg = Twist()
    msg.angular.z = -1
    return msg


def follow_the_wall():
    global regions_
    msg = Twist()
    msg.linear.x = 0.8
    return msg
    
def stop_robot():
    msg = Twist()
    msg.linear.x = 0
    msg.linear.y = 0
    msg.angular.z = 0
    return msg


def main():
    global pub_,trigger
    out_maze = False
    trigger = False
    rospy.init_node('reading_laser')
    
    pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    sub = rospy.Subscriber('/kobuki/laser/scan', LaserScan, clbk_laser)
    
    rate = rospy.Rate(20)
    while not out_maze:
        msg = Twist()
        if state_ == 0 and trigger == False:
            msg = find_wall()

        elif state_  ==0 and trigger == True:
            msg = turn_right()
            
        elif state_ == 1:
            msg = turn_left()
            trigger = True 
        elif state_ == 2:
            msg = follow_the_wall()
            trigger = True 
            pass
        elif state ==3:
            msg = stop_robot()
            out_maze = True 
        else:
            rospy.logerr('Unknown state!')
        
        pub_.publish(msg)
        
        rate.sleep()

if __name__ == '__main__':
    main()