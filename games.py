import numpy as np
# needs a map input, outputs updated map(s?)

class GameOfLife:
	def __init__(self, game_board, sim_steps=25, birth=3, survive=(2,3)):
		self.game_board = game_board
		self.birth = birth
		self.survive = survive
		self.sim_steps = sim_steps


	def run_game_one_step(self):
		# survive means value already exists (1/True) and it remains existing; need to check this precondition
			# survive must be an AND operation
		# birth means value does not exist (0/False) and it starts existing (1/True); need to check this precondition
			# birth must be an AND operation with NOT original board
		
		neighbors = self.find_neighbors(neighborhood='moore')
		board_mask = np.ma.make_mask(self.game_board.board)
		
		survive_temp = np.ma.masked_inside(neighbors, self.survive[0], self.survive[1])
		survive_board = np.ma.logical_and(board_mask, survive_temp.mask)
		
		birth_temp = np.ma.masked_equal(neighbors, self.birth)
		birth_board = np.ma.logical_and(np.logical_not(board_mask), birth_temp.mask)

		new_board = np.ma.logical_or(survive_board, birth_board)

		self.game_board.board = np.ma.logical_or(survive_board, birth_board).astype(int)
		self.game_board.state_log.append(self.game_board.board)


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
		padded_game_board = np.pad(self.game_board.board, pad_width=pad, mode='constant')

		return padded_game_board