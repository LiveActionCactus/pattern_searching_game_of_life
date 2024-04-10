import numpy as np
# needs a map input, outputs updated map(s?)

class GameOfLife:
	def __init__(self, game_board, birth=3, survive=(2,3)):
		self.game_board = game_board
		self.birth = birth
		self.survive = survive

	def find_neighbors(self, neighborhood='moore'):

		if neighborhood == 'moore':
			kernel, padded_game_board = self.moore_neighborhood_kernel()

		neighbors = np.zeros((self.game_board.rows, self.game_board.cols), dtype=int)

		for i in range(0, self.game_board.rows):
			for j in range(0, self.game_board.cols):
				neighbors[i,j] = np.multiply(kernel, padded_game_board[(i):(i+3), (j):(j+3)]).sum() 		# calculate num. neighbors

		return neighbors

	def	moore_neighborhood_kernel(self):
		padded_game_board = self.pad_game_board(self)
		kernel = np.array([[1,1,1], [1,0,1], [1,1,1]])

		return kernel, padded_game_board



	###
	# Helper functions
	###

	def pad_game_board(self, game_board, pad=1):
		padded_game_board = np.pad(self.game_board.map, pad_width=pad, mode='constant')

		return padded_game_board