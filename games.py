import numpy as np
import matplotlib.pyplot as plt

class GameOfLife:
	def __init__(self, game_board, sim_steps=25, birth=3, survive=(2,3)):
		self.game_board = game_board
		self.birth = birth
		self.survive = survive
		self.sim_steps = sim_steps

		# State info for metrics to run the FourierLife analysis
		self.birth_log = []
		self.survive_log = []
		self.death_log = [] 


	def run_game_one_step(self):
		# survive means value already exists (1/True) and it remains existing; need to check this precondition
			# survive must be an AND operation
		# birth means value does not exist (0/False) and it starts existing (1/True); need to check this precondition
			# birth must be an AND operation with NOT original board
		
		neighbors = self.find_neighbors(neighborhood='moore')
		board_mask = np.ma.make_mask(self.game_board.board, shrink=False)
		
		birth_temp = np.ma.masked_equal(neighbors, self.birth)
		birth_board = np.ma.logical_and(np.logical_not(board_mask), birth_temp.mask)
		self.birth_log.append(np.sum(birth_board))

		survive_temp = np.ma.masked_inside(neighbors, self.survive[0], self.survive[1])
		survive_board = np.ma.logical_and(board_mask, survive_temp.mask)
		self.survive_log.append(np.sum(survive_board))

		new_board = np.ma.logical_or(survive_board, birth_board)
		
		death_board = np.ma.logical_and(board_mask, np.logical_not(new_board))
		self.death_log.append(np.sum(death_board))

		self.game_board.board = new_board.astype(int)
		self.game_board.state_log.append(self.game_board.board)


	def find_neighbors(self, neighborhood='moore'):
		if neighborhood == 'moore':
			kernel, padded_game_board = self.moore_neighborhood_kernel()
		
		return self.apply_kernel_to_map(kernel, padded_game_board)		


	def	moore_neighborhood_kernel(self):
		padded_game_board = self.pad_game_board()
		kernel = np.array([[1,1,1], [1,0,1], [1,1,1]])

		return kernel, padded_game_board


	def apply_kernel_to_map(self, kernel, padded_game_board):
		kl, kw = kernel.shape 											# kernel length, kernel width
		neighbors = np.zeros((self.game_board.rows, self.game_board.cols), dtype=int)

		for i in range(0, self.game_board.rows):
			for j in range(0, self.game_board.cols):
				neighbors[i,j] = np.multiply(kernel, padded_game_board[(i):(i+kl), (j):(j+kw)]).sum() 		# calculate num. neighbors

		return neighbors


	def pattern_analysis_1d(self):
		#TODO: not working; fix this up
		data_flat = np.empty(0)
		for state in self.game_board.state_log:
			data_flat = np.concatenate((data_flat, state.flatten()))

		fft_1d_data = np.fft.fft(data_flat)
		#self.plot_fft_1d(fft_1d_data)
		self.plot_fft_1d(data_flat)


	def pattern_analysis_Nd(self):
		#TODO: not working; fix this up
		data = []
		for state in self.game_board.state_log:
			data.append(state)

		data = np.array(data)
		test = data.reshape(50,5).transpose()

		fft_Nd_data = np.fft.fftn(test)
		print(fft_Nd_data)
		print(fft_Nd_data.shape)
		input()

		plt.imshow(abs(fft_Nd_data))
		plt.show(block=True)

	def pattern_analysis_fl_metric(self):
		total_cells = self.game_board.cols * self.game_board.rows

		birth_percent = np.array(self.birth_log) / total_cells
		survive_percent = np.array(self.survive_log) / total_cells
		death_percent = np.array(self.death_log) / total_cells
		x = np.linspace(0, self.sim_steps-1, self.sim_steps, dtype=int)

		fft_birth = np.fft.fft(birth_percent)
		fft_survive = np.fft.fft(survive_percent)
		fft_death = np.fft.fft(death_percent)

		plt.figure()
		plt.subplot(1,2,1)
		plt.plot(x, birth_percent, label="birth")
		plt.plot(x, survive_percent+10, label="survive+10")
		plt.plot(x, death_percent+20, label="death+20")
		plt.legend()
		plt.grid()

		plt.subplot(1,2,2)
		plt.plot(x, fft_birth, label="birth")
		plt.plot(x, fft_survive+20, label="survive+20")
		plt.plot(x, fft_death+40, label="death+40")
		plt.legend()
		plt.grid()

		plt.show(block=True)


	###
	# Helper functions
	###

	def pad_game_board(self, pad=1):
		padded_game_board = np.pad(self.game_board.board, pad_width=pad, mode='constant')

		return padded_game_board


	def plot_fft_1d(self, fft_1d_data):
		# TODO: a promising metric is to look at ratio of alive/dead cells in the game and find periods from that 1-d metric
		#dummy, N = fft_1d_data.shape

		# Number of samplepoints
		N = 600
		# sample spacing
		T = 1.0 / 800.0
		x = np.linspace(0.0, N*T, N)
		y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
		yf = np.fft.fft(fft_1d_data, N)
		xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

		fig, ax = plt.subplots()
		ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
		plt.grid()
		plt.show()

	def plot_fft_Nd(self, fft_Nd_data):
		N = fft_Nd_data.shape[1]
		T = 1/(3*N)

		yf = np.fft.fftn(fft_1d_data, s=fft_Nd_data.shape)
		print(yf)
