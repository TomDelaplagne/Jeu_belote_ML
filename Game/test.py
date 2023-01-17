""" import rlcard
from rlcard.agents import RandomAgent

# print(env.num_actions) # 2
# print(env.num_players) # 1
# print(env.state_shape) # [[2]]
# print(env.action_shape) # [None]

env = rlcard.make('blackjack')
env.set_agents([RandomAgent(num_actions=env.num_actions)])

print(env.num_actions) # 2
print(env.num_players) # 1
print(env.state_shape) # [[2]]
print(env.action_shape) # [None]
trajectories, payoffs = env.run() """

# Python program to find maximum contiguous subarray

# Function to find the maximum contiguous subarray
""" from sys import maxint """
from sys import maxsize

def maxSubArraySum(a, size):

	max_so_far = -maxsize - 1
	max_ending_here = 0

	for i in range(0, size):
		max_ending_here = max_ending_here + a[i]

		if (max_so_far < max_ending_here):
			max_so_far = max_ending_here

		if max_ending_here < 0:
			max_ending_here = 0
		
	return max_so_far

# Driver function to check the above function

a = [-2, -3, 4, -1, -2, 1, 5, -3]

print ("Maximum contiguous sum is", maxSubArraySum(a, len(a)))


