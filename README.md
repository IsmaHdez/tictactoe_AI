# TicTacToe QPlayer project
This is a demonstration of Q-Table reinforncement learning using TicTacToe in Python.

## Working algorithm
1. The QPlayer takes a game_state as an input, which includes the board and current_player.
2. Looks up the board in its internal QTable to see if this state has already been explored.
3. If it has, it locates the best move and selects it.
4. If the state has not been explored, it selects a random move.
5. If several moves are the best move, it selects a random move from the set of best moves.
6. After selecting a move, it updates the corresponding Q-Table entry using the following formula.
$$
Q(S_t,A_t)\leftarrow Q(S_t,A_t) + \alpha[R_{t+1}+\gamma \max_a Q(S_{t+1},a)-Q(S_t,A_t)]
$$
7. It returns the move.

Additionally, whenever a game ends, the player updates the last board/selected move combination in the QTable. This means every path to victory is retroactively computed from the final states. 