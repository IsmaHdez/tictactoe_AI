
from gomoku import Gomoku  # assuming gomoku.py is the file containing the Gomoku class
from GomokuGame import GomokuGame
from Player import Player, HumanPlayer, RandomPlayer
import logging
import sys


# Create a logger
logger = logging.getLogger('gomoku_training_logger')
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler('gomoku_training.log')
file_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the file handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


training_episodes = 100

if len(sys.argv) > 1:
    # Get the integer argument
    training_episodes = int(sys.argv[1])

import random

# player1_buffer = [RandomPlayer('RandomPlayer')]
player1_buffer = [HumanPlayer('HumanPlayer')]

player2_buffer = [RandomPlayer('RandomPlayer')]
# player2_buffer = [HumanPlayer('HumanPlayer')]

p1_score, p2_score, draws = 0.0, 0.0, 0
t_p1_score, t_p2_score, t_draws = 0.0, 0.0, 0

for i in range(1, training_episodes + 1):
    player1 = random.choice(player1_buffer)
    player2 = random.choice(player2_buffer)
    logger.info(f'Player1 type {type(player1)}, Player2 type {type(player2)}')
    game = GomokuGame(player1, player2, size=3, pieces_in_row_to_win=3, logger=logger, print_board=True)
    result = game.run_game()
    logger.info(f'Episode {i}, {result}')
    p1_score += result[0]
    p2_score += result[1]
    if result[0]==result[1]:
        draws += 1
    if i % 100 == 0 :
        d_p1 = p1_score - t_p1_score
        d_p2 = p2_score - t_p2_score
        d_draws = draws - t_draws
        log_str = f'After {i} episodes, scores: {d_p1}, {d_p2}, draws {d_draws} (p1 win = {d_p1-d_draws/2}, p2 win = {d_p2-d_draws/2})'
        print(log_str)
        t_p1_score, t_p2_score, t_draws = p1_score, p2_score, draws

log_str = f'{training_episodes} episodes. Scores: {p1_score}, {p2_score}, draws {draws} | p1 win = {int(p1_score-draws/2)} ({(p1_score-draws/2)/training_episodes*100:.2f}%), p2 win = {int(p2_score-draws/2)} ({(p2_score-draws/2)/training_episodes*100:.2f}%)'
logger.info(log_str)
print(log_str)

print(f'model perf. diff {((p1_score-draws/2)/training_episodes*100 - (p2_score-draws/2)/training_episodes*100):.2f}')

for p in player1_buffer:
    p.shutdown()
for p in player2_buffer:
    p.shutdown()