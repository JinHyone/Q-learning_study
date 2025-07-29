import random
import pygame
from pygame.transform import scale
from enum import Enum, auto


class RenderModeEnum(Enum):
	Graphic = auto()
	Console = auto()


class Colors:
	RED = '\033[31m'
	BLACK = '\033[30m'
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
	Q: [list[list[list[float]]]] = None
	action_size = 4

	S: list[int] = [0, 0]

	hole = [[1, 1], [3, 1], [3, 2], [0, 3], [8, 8], [7, 8], [3, 5], [3, 6], [6, 6], [6, 2], [8, 3], [2, 7], [2, 8], [8, 2], [6, 5], [7, 5], [5, 9]]

	goal = [[7, 9]]

	gamma = 0.9

	window_size = [800, 800]

	render_mode: RenderModeEnum = RenderModeEnum.Graphic

	screen: pygame.Surface = None

	image: pygame.Surface = None

	clock: pygame.time.Clock = None

	limit_frame = 60
	wait_time = 1 / limit_frame

	def __init__(self, map_size: int = 4, action_size: int = 4, gamma: float = 0.9,
	             render_mode: RenderModeEnum = RenderModeEnum.Graphic, window_size: list[int] = [800, 800]):
		frozen_map = [[0 for i in range(map_size)] for i in range(map_size)]

		R = [[0 for i in range(map_size)] for i in range(map_size)]
		Q = [[[0.0 for i in range(action_size)] for i in range(map_size)] for i in
		     range(map_size)]  # [L: 0, U: 1, D: 2, R: 3]

		self.gamma = gamma

		for pos in self.hole:
			frozen_map[pos[1]][pos[0]] = 1
			R[pos[1]][pos[0]] = -1

		for pos in self.goal:
			frozen_map[pos[1]][pos[0]] = 2
			R[pos[1]][pos[0]] = 1

		self.map = frozen_map
		self.map_size = map_size
		self.R = R
		self.Q = Q
		self.S = [0, 0]
		self.render_mode = render_mode

		if render_mode == RenderModeEnum.Graphic:
			pygame.init()
			self.window_size = window_size
			self.screen = pygame.display.set_mode(window_size)
			self.clock = pygame.time.Clock()
			self.image = pygame.image.load('penguin-removebg-preview.png')

			self.image = scale(self.image, [window_size[0] / (map_size * 1.5), window_size[0] / (map_size * 1.5)])
			pygame.display.set_caption('Q-learning')

	def done_condition(self, state: list[int]):
		if state in self.goal:
			return True

		elif state in self.hole:
			return True

		else:
			return False

	def step(self, action: int, episode: int):
		vec_x = 0
		vec_y = 0

		epsilon = random.random()

		if epsilon * 0.75 * (episode + 1) < 0.3:
			print(f'epsilon: {epsilon} < 0.3')

			indices = [0, 1, 2, 3]
			removes = []

			for index in indices:
				vec_xx = 0
				vec_yy = 0

				if index == 0:
					vec_xx = -1

				elif index == 1:
					vec_yy = -1

				elif index == 2:
					vec_yy = 1

				elif index == 3:
					vec_xx = 1

				if self.S[0] + vec_xx >= self.map_size or self.S[0] + vec_xx < 0 or self.S[1] + vec_yy >= self.map_size or \
						self.S[1] + vec_yy < 0:
					removes.append(index)

			for rmv in removes:
				indices.remove(rmv)

			action = random.choice(indices)

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
		self.Q[s[1]][s[0]][action] = reward + self.gamma * max(self.Q[next_y][next_x])

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

			if self.S[0] + vec_x >= self.map_size or self.S[0] + vec_x < 0 or self.S[1] + vec_y >= self.map_size or \
					self.S[1] + vec_y < 0:
				removes.append(index)

		for rmv in removes:
			indices.remove(rmv)

		return random.choice(indices)

	def reset(self):
		self.S = [0, 0]
		return self.S

	# noinspection PyMethodMayBeStatic
	def map_print_symbol(self, num):
		if num == 0:
			return Colors.BLUE + '☐'
		if num == 1:
			return Colors.BLACK + '☐'
		if num == 2:
			return Colors.GREEN + '☐'

	# noinspection PyMethodMayBeStatic
	def map_render_symbol(self, num):
		if num == 0:
			return 0, 0, 255
		if num == 1:
			return 0, 0, 0
		if num == 2:
			return 0, 255, 0

	def print_map(self):
		for y in range(self.map_size):
			for x in range(self.map_size):
				print(
					Colors.YELLOW + '☐' if x == self.S[0] and y == self.S[1] else self.map_print_symbol(self.map[y][x]),
					end='   ')

			print('\n')

	def render_map(self):
		self.screen.fill([255, 255, 255])
		cell_size = self.window_size[0] / self.map_size

		for column_index in range(self.map_size):
			for row_index in range(self.map_size):
				pygame.draw.rect(self.screen, self.map_render_symbol(env.map[column_index][row_index]),
				                 pygame.Rect(row_index * cell_size, column_index * cell_size, cell_size, cell_size))

		self.screen.blit(self.image, (self.image.get_size()[0] / 4 + cell_size * self.S[0], self.image.get_size()[0] / 4 + cell_size * self.S[1]))
		pygame.display.flip()

		self.clock.tick(self.limit_frame)


env = FrozenLake(gamma=0.8, map_size=10)

episodes = 1000
action_count = 0

total_rewards = []

for episode in range(episodes):
	state = env.reset()
	total_reward = 0

	# os.system('cls')
	# print(f'{Colors.RESET}episode: {episode + 1}, action: {action_count}')
	# env.print_map()
	# time.sleep(0.2)

	done = False

	env.render_map()

	while not done:
		action = env.argmax(env.Q[state[1]][state[0]])
		new_state, reward, done = env.step(action, episode)

		total_reward += reward
		state = new_state

		action_count += 1

		env.render_map()
	print(f'episode: {episode}, action: {action_count}')

	# os.system('cls')
	# print(f'{Colors.RESET}episode: {episode + 1}, action {action_count}')
	# env.print_map()
	# time.sleep(0.2)
