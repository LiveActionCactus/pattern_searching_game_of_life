from board import Board
from games import GameOfLife


if __name__ == "__main__":
	rows = 5
	cols = 5

	# Initialize game board
	game_board = Board(rows, cols)

	# Choose initial state 
	#game_board.init_agents_random(num_agents=10)			# TODO: doesn't guarantee 10 unique agents, could be collisions
	# game_board.init_blinker()
	# game_board.init_boat()
	game_board.init_clock()

	# Initialize game to play on the board
	game = GameOfLife(game_board, sim_steps=10)

	# Run game
	for i in range(0, game.sim_steps):
		game.run_game_one_step()

	# Plot results
	game_board.plot_board()