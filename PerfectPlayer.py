from Player import Player

"""
Implements the Newell and Simon strategy detailed in TicTacToe's Wikipedia page: https://en.wikipedia.org/wiki/Tic-tac-toe

This player can be used to train and test the QTable Player. 
"""


class PerfectPlayer(Player):
    
    #-----------| Init |-----------#
    def __init__(self, name):
        super().__init__(name)
        

    #----------| Public |----------#
    def get_move(self,game_state):
        board = game_state['board']
        current_player = game_state['current_player']
        #Win
        move = self._check_for_win(board, current_player)
        if move:
            if len(move)>1:
                
                return move[0]
            
            return move[0]
        #Prevent win
        move = self._check_for_block(board, current_player)
        if move:
            
            return move
        #Create fork
        move = self._check_for_fork(board, current_player)
        if move:
            
            return move
        #Prevent fork
        move = self._check_for_opponent_fork(board, current_player)
        if move:
            
            return move

        available_moves = [(i, j) for i, row in enumerate(board) for j, spot in enumerate(row) if spot == ' ']
        #Play center
        if (1,1) in available_moves:
            
            return (1,1)
        #Play opposite corner
        move = self._get_opposite_corner(board, current_player)
        if move:
            
            return move
        #Play empty corner
        move = self._get_first_empty_corner(board)
        if move:
            
            return move
        #empty side
        move = self._get_first_empty_side(board)
        if move:
            
            return move

    def score(self, score):
        pass

    def shutdown(self):
        pass

    #---------| Private |---------#
    def _check_for_win(self, board, current_player):
        winning_moves = []

        for i in range(3):
            if board[i].count(current_player) == 2 and board[i].count(' ') == 1:
                winning_moves.append((i, board[i].index(' ')))

            if [board[j][i] for j in range(3)].count(current_player) == 2 and [board[j][i] for j in range(3)].count(' ') == 1:
                winning_moves.append(([board[j][i] for j in range(3)].index(' '), i))


        if [board[i][i] for i in range(3)].count(current_player) == 2 and [board[i][i] for i in range(3)].count(' ') == 1:
            for i in range(3):
                if board[i][i]==' ':
                    position = i
            winning_moves.append((position, position))

        if [board[i][2 - i] for i in range(3)].count(current_player) == 2 and [board[i][2 - i] for i in range(3)].count(' ') == 1:
            for i in range(3):
                if board[i][2-i]==' ':
                    position = i
            winning_moves.append((position, 2-position))

        return winning_moves

    def _check_for_block(self, board, current_player):

        opponent = 'O' if current_player == 'X' else 'X'

        for i in range(3):
            if board[i].count(opponent) == 2 and board[i].count(' ') == 1:
                return i, board[i].index(' ')

            if [board[j][i] for j in range(3)].count(opponent) == 2 and [board[j][i] for j in range(3)].count(' ') == 1:
                return [board[j][i] for j in range(3)].index(' '), i

        if [board[i][i] for i in range(3)].count(opponent) == 2 and [board[i][i] for i in range(3)].count(' ') == 1:
            return [board[i][i] for i in range(3)].index(' '), [board[i][i] for i in range(3)].index(' ')

        if [board[i][2 - i] for i in range(3)].count(opponent) == 2 and [board[i][2 - i] for i in range(3)].count(' ') == 1:
            return [board[i][2 - i] for i in range(3)].index(' '), 2 - [board[i][2 - i] for i in range(3)].index(' ')

        return False
    
    def _check_for_fork(self, board, current_player):
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = current_player
                    winning_moves = self._check_for_win(board, current_player)
                    board[i][j] = ' '  
                    if len(winning_moves) >= 2:
                        return i, j
        return False
    
    def _check_for_opponent_fork(self, board, current_player):
        opponent = 'O' if current_player == 'X' else 'X'

        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = opponent
                    opponent_winning_moves = self._check_for_win(board, opponent)
                    board[i][j] = ' '  # Reset the board cell

                    if len(opponent_winning_moves) >= 2:
                        return i, j
        return False
    
    def _get_opposite_corner(self, board, current_player):
        opponent = 'O' if current_player == 'X' else 'X'
        available_moves = [(i, j) for i, row in enumerate(board) for j, spot in enumerate(row) if spot == ' ']
        for i in [0, 2]:
            for j in [0, 2]:
                if board[i][j] == opponent and (2 - i, 2 - j) in available_moves:
                    return (2 - i, 2 - j)
        return False
    
    def _get_first_empty_corner(self, board):
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]

        for corner in corners:
            i, j = corner
            if board[i][j] == ' ':
                return corner

        return False
    
    def _get_first_empty_side(self, board):
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]

        for side in sides:
            i, j = side
            if board[i][j] == ' ':
                return side

        return False