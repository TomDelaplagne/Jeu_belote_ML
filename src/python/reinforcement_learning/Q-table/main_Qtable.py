"""module to train the Q table on one deck"""
import random

import numpy as np
from tqdm import tqdm

from src.python.reinforcement_learning.gym_env import BeloteGameEnv
from q_player_class import QPlayer
from src.python.player.player_class import DumbPlayer

def greedy_policy(Qtable, state):
	# Exploitation: take the action with the highest state, action value
	state_idx = state_to_idx(state)
	action = np.argmax(Qtable[state_idx][:])
	return action

def epsilon_greedy_policy(Qtable, state, epsilon):

	# Randomly generate a number between 0 and 1
	random_int = random.uniform(0,1)
	# if random_int > greater than epsilon --> exploitation
	if random_int > epsilon:
		# Take the action with the highest value given a state
		# np.argmax can be useful here
		action = greedy_policy(Qtable, state)
	# else --> exploration
	else:
		action = np.random.choice([0,1,2])

	return action

def evaluate_agent(env, max_steps, n_eval_episodes, Q, seed):
	"""
	Evaluate the agent for ``n_eval_episodes`` episodes and returns average reward and std of reward.
	:param env: The evaluation environment
	:param n_eval_episodes: Number of episode to evaluate the agent
	:param Q: The Q-table
	:param seed: The evaluation seed array
	"""
	episode_rewards = []
	for episode in tqdm(range(n_eval_episodes)):
		if seed:
			state, _ = env.reset(seed=seed[episode])
		else:
			state, _ = env.reset()
		done = False
		total_rewards_ep = 0

		for _ in range(max_steps):
			# Take the action (index) that have the maximum expected future reward given that state
			action = greedy_policy(Q, state)
			new_state, reward, done, _ = env.step(action)
			total_rewards_ep += reward

			if done:
				break
			state = new_state
		episode_rewards.append(total_rewards_ep)
	mean_reward = np.mean(episode_rewards)
	std_reward = np.std(episode_rewards)

	return mean_reward, std_reward

def train(n_training_episodes, min_epsilon, max_epsilon, decay_rate, env, max_steps, Qtable, learning_rate, gamma):
	for episode in tqdm(range(n_training_episodes)):
		# Reduce epsilon (because we need less and less exploration)
		epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode)
		# Reset the environment
		state, _ = env.reset()

		done = False

		# repeat
		for _ in range(max_steps):
			# Choose the action At using epsilon greedy policy
			action = epsilon_greedy_policy(Qtable, state, epsilon)

			# Take action At and observe Rt+1 and St+1
			# Take the action (a) and observe the outcome state(s') and reward (r)
			new_state, reward, done, _ = env.step(action)

			# Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]
			state_idx = state_to_idx(state)
			new_state_idx = state_to_idx(new_state)

			Qtable[state_idx][action] = Qtable[state_idx][action] + learning_rate * (reward + gamma * np.max(Qtable[new_state_idx]) - Qtable[state_idx][action])

			# Qtable[state][action] = Qtable[state][action] + learning_rate * (reward + gamma * np.max(Qtable[new_state]) - Qtable[state][action])

			# If done, finish the episode
			if done:
				break

			# Our next state is the new state
			state = new_state
	return Qtable

def state_to_idx(state):
	"""
	Maps a state (represented as a tuple of 7 values)
	to an index between 0 and 16,806.
	"""
	idx = 0
	for i, value in enumerate(state):
		idx += value * (7 ** i)
	return idx

def main():
	"""main function to train the Q table"""
	q_player = QPlayer("QPlayer")

	env = BeloteGameEnv(q_player, DumbPlayer("Player2"))

	print("_____OBSERVATION SPACE_____ \n")
	print("Observation Space", env.observation_space)
	sample = env.observation_space.sample()
	state_spaces = env.observation_space.shape[0]
	state_value = 7
	print("Sample observation", sample, "with the associated idx value of ", state_to_idx(sample)) # Get a random observation
	print("There are ", state_spaces, " observationnal variable")
	print("There is ", state_value, " possible values for each variable")
	print("There is ", state_spaces ** state_value, " possible states")

	print("\n _____ACTION SPACE_____ \n")
	print("Action Space Shape", env.action_space.n)
	print("Action Space Sample", env.action_space.sample()) # Take a random action

	# space_n1, space_n2 = state_space
	# print("There are ", space_n1 * space_n2, " possible states")

	action_space = env.action_space.n
	print("There are ", action_space, " possible actions")

	print("\n _____TRAINING_____ \n")
	print("Training the Q table...")


	# Initialize the Q table
	Qtable = np.zeros((7 ** 7 - 1, action_space))

	# Training parameters
	n_training_episodes = 5_000_000  # Total training episodes
	learning_rate = 0.1          	# Learning rate

	# Evaluation parameters
	n_eval_episodes = 1000       	 # Total number of test episodes

	# Environment parameters
	max_steps = 10	             	# Max steps per episode
	gamma = 0.95                 	# Discounting rate
	eval_seed = []               	# The evaluation seed of the environment

	# Exploration parameters
	max_epsilon = 1.0             	# Exploration probability at start
	min_epsilon = 0.05            	# Minimum exploration probability
	decay_rate = 0.000005           	# Exponential decay rate for exploration prob

	# Train our Agent
	Qtable = train(n_training_episodes, min_epsilon, max_epsilon, decay_rate, env, max_steps, Qtable, learning_rate, gamma)

	# save the Q table
	np.save("Qtable.npy", Qtable)

	# Evaluate our Agent
	mean_reward, std_reward = evaluate_agent(env, max_steps, n_eval_episodes, Qtable, eval_seed)
	print(f"Mean_reward={mean_reward:.2f} +/- {std_reward:.2f}")

if __name__ == "__main__":
	main()
