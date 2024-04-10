import numpy as np
import random
from board import Board
from games import GameOfLife




def place_agents_random(data, num_agents):
	for i in range(0,num_agents):
		data[random.randint(0, rows - 1), random.randint(0, cols - 1)] = 1

	return(data)

###
# Begin main
###

if __name__ == "__main__":
	rows = 10
	cols = 10

	# Build map and padded map
	game_board = Board(rows, cols) 
	game_board.map = place_agents_random(game_board.board, 20)


	# Calculate neighbors
	game = GameOfLife(game_board)
	neighbors = game.find_neighbors()

	print(neighbors)

	game_board.plot_board()