
from gomoku import Gomoku  # assuming gomoku.py is the file containing the Gomoku class
from Player import Player  # assuming player.py is the file containing the Player classes

import logging
# # Create a logger
# logger = logging.getLogger('gomoku_logger')
# logger.setLevel(logging.DEBUG)

# # Create a file handler
# file_handler = logging.FileHandler('gomoku_games.log')
# file_handler.setLevel(logging.DEBUG)

# # Create a formatter and add it to the file handler
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)

# # Add the file handler to the logger
# logger.addHandler(file_handler)

class GomokuGame:
    def __init__(self, player1, player2, size = 15, pieces_in_row_to_win = 5, logger = None, starting_board=None, next_player=None, print_board=False):
        self.game = Gomoku(size = size, pieces_in_row_to_win = pieces_in_row_to_win, starting_board=starting_board, next_player=next_player)
        # Map 'X' and 'O' to player1 and player2
        self.players = {'X': player1, 'O': player2}
        self.logger = logger if logger else logging.getLogger('gomoku_logger')
        self.print_board = print_board    

    # Returns (player1 score, player2 score)
    def run_game(self,):
        # print("Welcome to the Gomoku game!")
        self.logger.info('New Game')
        # self.game.print_board()
        while not self.game.get_game_state()['game_over']:
            # print(f"Player {self.game.current_player}'s turn.")
            
            # Get the move from the current player
            x, y = self.players[self.game.current_player].get_move(self.game.get_game_state())
            self.logger.info(f'{self.game.current_player}: {x},{y}')

            # Make the move
            try:
                self.game.move(x, y)
            except Exception as e:
                print(e)                
                continue


            # Print the updated board
            if self.print_board:
                self.game.print_board()

            # Check if the game has ended
            if self.game.get_game_state()['game_over']:
                winner = self.game.get_game_state()['winner']
                if winner:
                    # print(f"Player {winner} has won!")
                    self.logger.info(f"Game ended in a win/lose!")
                    looser = self.players['O'] if 'X' == winner else self.players['X']
                    self.players[winner].score(1.0)
                    looser.score(0.0)
                    self.logger.info(f"Player {winner} won!")
                    return (1.0, 0.0) if 'X' == winner else (0.0, 1.0)
                else:
                    # print(f"Game ended in draw!")
                    self.logger.info(f"Game ended in a draw!")
                    self.players['X'].score(0.5)
                    self.players['O'].score(0.5)
                    self.logger.info(f"Players are updated.")
                    return (0.5, 0.5)
        # print("Thank you for playing!")
