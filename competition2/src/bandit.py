import numpy as np
import time
import rospy
import datetime
from competition2.srv import BanditStep, BanditAnswer



def epsilon_greedy_policy(epsilon, q, narm):
    """
    epsilon greedy policy.
    """

    if np.random.uniform() >= epsilon:
        action = np.argmax(q)

    else:
        action = np.random.choice(np.arange(narm))

    return action


def solve_bandit(passcode, narm):
    print("\n\nSOLVING BANDIT PROBLEM... \n\n")
    start = time.time()
    
    rospy.wait_for_service("/bandit_step")
    bandit_step_client = rospy.ServiceProxy("/bandit_step", BanditStep)

    rospy.wait_for_service("/bandit_answer")
    bandit_answer_client = rospy.ServiceProxy("/bandit_answer", BanditAnswer)

    epsilon = 0.01

    q = np.zeros(narm)
    n = np.zeros(narm)

    ns = 0
    num_simulations = 1000


    while (ns < (narm * num_simulations)):

        action = epsilon_greedy_policy(epsilon, q, narm) 

        response = bandit_step_client(passcode, action+1)
        reward = response.reward
        valid = response.valid

        n[action] += 1
        q[action] += (1. / n[action]) * (reward - q[action])

        ns += 1
    
    best_arm = np.where(q == np.max(q))[0]

    # Make sure only 1 best arm
    while len(best_arm) > 1:
        num_simulations += 100
        while (ns < (narm * num_simulations)):

            action = epsilon_greedy_policy(epsilon, q, narm) 

            response = bandit_step_client(passcode, action+1) 
            reward = response.reward
            valid = response.valid

            n[action] += 1
            q[action] += (1. / n[action]) * (reward - q[action])

            ns += 1

        best_arm = np.where(q == np.max(q))[0]

    print("Best Arm:",best_arm[0]+1, "\n\n")
    response = bandit_answer_client(best_arm[0]+1)

    room = response.room
    where = response.where

    print("response from server:\n")
    print("maze room:", room)
    print("where:", where, "\n\n")

    

    print("\nOrderings of Arms")
    q_copy = np.copy(q).tolist()
    a = 0
    while a < narm:
        max_ = max(q_copy)
        max_index = q_copy.index(max_)
        q_copy[max_index] = -1
        print("Arm: {}".format(max_index+1))
        a += 1
    

    


    end = time.time()

    completion_time = end - start

    print("\nTotal Bandit Time: {} seconds\n\n".format(completion_time))

    return room, where