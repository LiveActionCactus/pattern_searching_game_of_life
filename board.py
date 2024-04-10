import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

class Board:
	def __init__(self, rows=10, cols=10):
		self.rows = rows
		self.cols = cols
		self.board = np.zeros((rows,cols))


	def plot_board(self):
		# Create discrete colormap
		cmap = colors.ListedColormap(['white', 'black'])
		norm = colors.BoundaryNorm([0, 1], cmap.N)

		fig, ax = plt.subplots()
		ax.imshow(self.board, cmap=cmap, norm=norm)
		ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.25)		# draw gridlines
		ax.set_xticks(np.arange(0.5, self.rows, 1))
		ax.set_yticks(np.arange(0.5, self.cols, 1))
		plt.tick_params(axis='both', which='both', bottom=False,   
						left=False, labelbottom=False, labelleft=False)
		plt.show() 