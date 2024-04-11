import numpy as np
# needs a map input, outputs updated map(s?)

class GameOfLife:
	def __init__(self, game_board, birth=3, survive=(2,3)):
		self.game_board = game_board
		self.birth = birth
		self.survive = survive


	def run_game_one_step(self):
		neighbors = self.find_neighbors(neighborhood='moore')
		birth_survive_board = np.ma.masked_inside(neighbors, self.survive[0], self.birth) # TODO: generalize this for arbitrary birth/survive values
		print(neighbors)
		print(birth_survive_board.mask)
		input()
		

	def find_neighbors(self, neighborhood='moore'):
		if neighborhood == 'moore':
			kernel, padded_game_board = self.moore_neighborhood_kernel()
		
		return self.apply_kernel_to_map(kernel, padded_game_board)		


	def	moore_neighborhood_kernel(self):
		padded_game_board = self.pad_game_board(self)
		kernel = np.array([[1,1,1], [1,0,1], [1,1,1]])

		return kernel, padded_game_board


	def apply_kernel_to_map(self, kernel, padded_game_board):
		kl, kw = kernel.shape 											# kernel length, kernel width
		neighbors = np.zeros((self.game_board.rows, self.game_board.cols), dtype=int)

		for i in range(0, self.game_board.rows):
			for j in range(0, self.game_board.cols):
				neighbors[i,j] = np.multiply(kernel, padded_game_board[(i):(i+kl), (j):(j+kw)]).sum() 		# calculate num. neighbors

		return neighbors


	###
	# Helper functions
	###

	def pad_game_board(self, game_board, pad=1):
		padded_game_board = np.pad(self.game_board.map, pad_width=pad, mode='constant')

		return padded_game_board