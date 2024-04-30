import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib import colors
import time

# TODO: implement user def'd board

class Board:
	def __init__(self, rows=10, cols=10):
		self.rows = rows
		self.cols = cols
		self.board = np.zeros((rows,cols))
		self.state_log = []

	def init_agents_random(self, num_agents=0):
		for i in range(0,num_agents):
			self.board[random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)] = 1

		self.state_log.append(self.board)

	def init_blinker(self):
		r = (self.rows//2)  		# helps center the pattern
		c = (self.cols//2) - 1

		for i in range(0,3):
			self.board[r,c+i] = 1

	def init_boat(self):
		r = (self.rows//2)  		# helps center the pattern
		c = (self.cols//2) - 1

		self.board[r+1, c]		= 1
		self.board[r+1, c+1]	= 1
		self.board[r, c] 		= 1
		self.board[r, c+2]		= 1
		self.board[r-1, c+1]	= 1

	def init_clock(self):
		r = (self.rows//2)  		# helps center the pattern
		c = (self.cols//2) - 1

		self.board[r+2,c+1]		= 1
		self.board[r+1,c+1]		= 1
		self.board[r+1,c+3]		= 1
		self.board[r,c]			= 1
		self.board[r,c+2]		= 1
		self.board[r-1,c+2]		= 1


	def plot_board(self, blocking=False, delay=0.5):
		# Create discrete colormap
		cmap = colors.ListedColormap(['white', 'black'])
		norm = colors.BoundaryNorm([0, 1], cmap.N)

		plt.ion()

		fig, ax = plt.subplots()
		axim = ax.imshow(self.state_log[0], cmap=cmap, norm=norm)
		
		ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.25)		# draw gridlines
		ax.set_xticks(np.arange(0.5, self.rows, 1))
		ax.set_yticks(np.arange(0.5, self.cols, 1))
		plt.tick_params(axis='both', which='both', bottom=False,   
						left=False, labelbottom=False, labelleft=False)
		plt.title("Iter 0")
		plt.show()
		
		# Plot simulation results with delay
		for idx, state in enumerate(self.state_log):
			plt.title("Iter " + str(idx))
			axim.set_data(state)
			fig.canvas.flush_events()
			time.sleep(delay)

			if np.sum(state) == 0:
				break

		plt.show(block=blocking)
