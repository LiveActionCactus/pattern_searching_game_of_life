import matplotlib.pyplot as plt
#import matplotlib.colors as colors
from matplotlib import colors
import numpy as np
import random

def plot_grid(data):
	fig, ax = plt.subplots()
	ax.imshow(data, cmap=cmap, norm=norm)
	ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.25)		# draw gridlines
	ax.set_xticks(np.arange(0.5, rows, 1))
	ax.set_yticks(np.arange(0.5, cols, 1))
	plt.tick_params(axis='both', which='both', bottom=False,   
					left=False, labelbottom=False, labelleft=False)
	plt.show() 

def moore_neighborhood_kernel(data_pad, rows, cols):
	kernel = np.array([[1,1,1], [1,0,1], [1,1,1]])
	neighbors = np.zeros(rows*cols).reshape(rows,cols)

	for i in range(0,rows):
		for j in range(0,cols):
			neighbors[i,j] = np.multiply(kernel, data_pad[(i):(i+3), (j):(j+3)]).sum() 		# calculate num. neighbors

	return neighbors

def place_agents(data, num_agents):
	for i in range(0,num_agents):
		data[random.randint(0, rows - 1), random.randint(0, cols - 1)] = 1

	return(data)

###
# Begin main
###

# Cell options
EMPTY_CELL = 0
START_CELL = 1

# Create discrete colormap
cmap = colors.ListedColormap(['white', 'black'])
bounds = [EMPTY_CELL, START_CELL]
norm = colors.BoundaryNorm(bounds, cmap.N)

if __name__ == "__main__":
	rows = 10
	cols = 10

	data = np.zeros(rows * cols).reshape(rows, cols)
	data = place_agents(data, 4)
	data_pad = np.pad(data, pad_width=1, mode='constant')

	neighbors = moore_neighborhood_kernel(data_pad, rows, cols)

	print(neighbors)

	plot_grid(data)