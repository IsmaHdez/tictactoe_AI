class Gomoku:
    def __init__(self, size = 15, pieces_in_row_to_win = 5, starting_board=None, next_player=None):
        """
        Initialize the Gomoku game. Set up the game state with a size x size (15x15 by default) empty board,
        set the current player to 'X', and set `game_over` to False.
        """
        self.size = size
        self.board = [[' ' for _ in range(self.size)] for _ in range(self.size)] if starting_board is None else starting_board
        self.players = ['X', 'O']
        self.current_player = self.players[0] if next_player is None else next_player
        self.game_over = False
        self.winner = None  # Added winner to game state
        self.pieces_in_row_to_win = pieces_in_row_to_win
        self._empty_space = size*size if starting_board is None else sum(1 for c in sum(starting_board,[]) if c==' ')

    def print_board(self):
        """
        Print the current state of the game board. Empty spots are represented by ' ',
        and players' pieces are represented by 'X' and 'O'.
        """
        # Print the column numbers
        print('  ' + ' '.join([format(i, 'X') for i in range(self.size)]))

        # Print the board with row numbers
        for i, row in enumerate(self.board):
            print(format(i, 'X') + ' ' + ' '.join(row))

        print()

    def move(self, x, y):
        """
        Make a move. The current player places a piece at the specified coordinates (x, y).

        Args:
        x (int): The x-coordinate of the move.
        y (int): The y-coordinate of the move.

        Returns:
        True if the move is successful, False otherwise.
        """
        if self.game_over or self.board[x][y] != ' ':
            return False
        self.board[x][y] = self.current_player
        self._empty_space -= 1
        if self._check_winner(x, y):
            self.game_over = True
            self.winner = self.current_player
            # return f'Player {self.current_player} wins!'
            return False
        elif self._empty_space == 0:
            self.game_over = True
            self.winner = None
            return False
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]
        return True


    def get_game_state(self):
        """
        Get the current game state.

        Returns:
        A dictionary representing the game state. The keys are "board", "current_player", 
        "game_over", and "winner", and the corresponding values represent the state of the game.
        """
        return {
            "board": self.board,
            "current_player": self.current_player,
            "game_over": self.game_over,
            "winner": self.winner  # Added winner to game state
        }

    # Private methods
    def _check_winner(self, x, y):
        """
        Check if the current player has won the game after making a move at (x, y).

        Args:
        x (int): The x-coordinate of the move.
        y (int): The y-coordinate of the move.

        Returns:
        True if the current player has won, False otherwise.
        """
        # Define all 8 directions as (dx, dy) pairs
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dx, dy in directions:
            if self._count_consecutive_pieces(x, y, dx, dy) == self.pieces_in_row_to_win:
                return True

        return False

    def _count_consecutive_pieces(self, x, y, dx, dy):
        """
        Count the number of consecutive pieces of the same type along a certain direction.

        Args:
        x (int): The x-coordinate of the starting position.
        y (int): The y-coordinate of the starting position.
        dx (int): The x-component of the direction vector.
        dy (int): The y-component of the direction vector.

        Returns:
        The number of consecutive pieces of the same type along the direction (dx, dy).
        """
        # Check if the piece at the starting position matches the current player's piece
        if not self._is_same_piece(x, y):
            return 0

        # Count the pieces in the forward direction
        count_forward = 0
        while self._is_on_board(x + dx*count_forward, y + dy*count_forward) and self._is_same_piece(x + dx*count_forward, y + dy*count_forward):
            count_forward += 1

        # Count the pieces in the backward direction
        count_backward = 0
        while self._is_on_board(x - dx*count_backward, y - dy*count_backward) and self._is_same_piece(x - dx*count_backward, y - dy*count_backward):
            count_backward += 1

        return count_forward + count_backward - 1  # Subtract 1 to avoid double-counting the starting piece





    def _is_on_board(self, x, y):
        """
        Check if the position (x, y) is on the board.

        Args:
        x (int): The x-coordinate of the position.
        y (int): The y-coordinate of the position.

        Returns:
        True if the position is on the board, False otherwise.
        """
        return 0 <= x < self.size and 0 <= y < self.size




    def _is_same_piece(self, x, y):
        """
        Check if the piece at (x, y) is the same as the current player's piece.

        Args:
        x (int): The x-coordinate of the piece.
        y (int): The y-coordinate of the piece.

        Returns:
        True if the piece at (x, y) is the same as the current player's piece, False otherwise.
        """
        return self.board[x][y] == self.current_player


    def _is_empty_or_opponent(self, x, y):
        pass
