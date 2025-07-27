import os
import time
import random


class Colors:
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	BLUE = '\033[34m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'
	WHITE = '\033[37m'
	RESET = '\033[0m'


class FrozenLake:
	"""
		0: frozen
		1: hole
		2: goal
	"""
	map: list[list[int]] = None
	map_size = 4

	R: list[list[int]] = None
	Q: [list[list[list[int]]]] = None
	action_size = 4

	S: list[int] = [0, 0]

	hole = [[1, 1], [3, 1], [3, 2], [0, 3]]

	def __init__(self, map_size: int = 4, action_size = 4):
		frozen_map = [[0 for i in range(map_size)] for i in range(map_size)]
		frozen_map[3][3] = 2

		R = [[0 for i in range(map_size)] for i in range(map_size)]
		R[3][3] = 1

		Q = [[[0 for i in range(action_size)] for i in range(map_size)] for i in range(map_size)]  # [L: 0, U: 1, D: 2, R: 3]

		for pos in self.hole:
			frozen_map[pos[1]][pos[0]] = 1
			R[pos[1]][pos[0]] = -1

		self.map = frozen_map
		self.R = R
		self.Q = Q
		self.S = [0, 0]

	def done_condition(self, state: list[int]):
		if state[0] == 3 and state[1] == 3:
			return True

		elif state in self.hole:
			return True

		else:
			return False

	def step(self, action: int):
		vec_x = 0
		vec_y = 0

		if action == 0:
			vec_x = -1

		elif action == 1:
			vec_y = -1

		elif action == 2:
			vec_y = 1
		elif action == 3:
			vec_x = 1

		s = self.S

		next_x = s[0] + vec_x
		next_y = s[1] + vec_y

		reward = self.R[next_y][next_x]
		self.Q[s[1]][s[0]][action] = reward + max(self.Q[next_y][next_x])

		s[0] = next_x
		s[1] = next_y

		return [next_x, next_y], reward, self.done_condition(s)

	def argmax(self, Q):
		indices = [idx for idx, val in enumerate(Q) if val == max(Q)]
		removes = []

		for index in indices:
			vec_x = 0
			vec_y = 0

			if index == 0:
				vec_x = -1

			elif index == 1:
				vec_y = -1

			elif index == 2:
				vec_y = 1

			elif index == 3:
				vec_x = 1

			if self.S[0] + vec_x >= self.map_size or self.S[0] + vec_x < 0 or self.S[1] + vec_y >= self.map_size or self.S[1] + vec_y < 0:
				removes.append(index)

		for rmv in removes:
			indices.remove(rmv)

		return random.choice(indices)

	def reset(self):
		self.S = [0, 0]
		return self.S

	# noinspection PyMethodMayBeStatic
	def map_symbol(self, num):
		if num == 0:
			return Colors.BLUE + '☐'
		if num == 1:
			return '\033[30m' + '☐'
		if num == 2:
			return Colors.GREEN + '☐'

	def print_map(self):
		for y in range(4):
			for x in range(4):
				print(Colors.YELLOW + '☐' if x == self.S[0] and y == self.S[1] else self.map_symbol(self.map[y][x]), end='   ')

			print('\n')


env = FrozenLake()

episodes = 1000
action_count = 0
for episode in range(episodes):
	state = env.reset()
	total_reward = 0

	os.system('cls')
	print(f'{Colors.RESET}episode: {episode + 1}, action: {action_count}')
	env.print_map()
	time.sleep(0.2)

	done = False

	while not done:
		action = env.argmax(env.Q[state[1]][state[0]])
		new_state, reward, done = env.step(action)

		total_reward += reward
		state = new_state

		action_count += 1

		os.system('cls')
		print(f'{Colors.RESET}episode: {episode + 1}, action {action_count}')
		env.print_map()
		time.sleep(0.2)
