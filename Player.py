import pickle

class Player:

    def __init__(self, name='Anonymous Player'):
        self.name=name

    def get_move(self, game_state):
        raise NotImplementedError("This method should be overridden in a subclass")
    
    def score(self, score):
        raise NotImplementedError("This method should be overridden in a subclass if necessary")

    def shutdown(self):
        raise NotImplementedError("This method should be overridden in a subclass if necessary")

    def save_table(self,table, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(dict(table), f)        

    def load_table(self, file_path):
        print('Loading table from file', file_path)
        try:
            with open(file_path, 'rb') as f:
                table = defaultdict(float, pickle.load(f))
        except FileNotFoundError:
            print(f'{file_path} not found. Using empty values instead.')
            table = defaultdict(float)
        return table

    def log_board(self, logger, board):
        """
        Print the current state of the game board. Empty spots are represented by ' ',
        and players' pieces are represented by 'X' and 'O'.
        """
        # Print the column numbers
        logger.debug('Board')
        # Print the board with row numbers
        for i, row in enumerate(board):
            logger.debug(' '.join(row))

    def print_board(self, board):
        """
        Print the current state of the game board. Empty spots are represented by ' ',
        and players' pieces are represented by 'X' and 'O'.
        """
        # Print the column numbers
        size = len(board)
        print('  ' + ' '.join([format(i, 'X') for i in range(size)]))

        # Print the board with row numbers
        for i, row in enumerate(board):
            print(format(i, 'X') + ' ' + ' '.join(row))

        print()    


class HumanPlayer(Player):

    def __init__(self, name):
        super().__init__(name)

    def get_move(self, game_state):
        # Optionally print game state here
        self.print_board(game_state['board'])
        move = input("Enter your move in hexadecimal format (e.g., 'A1'): ")
        x = int(move[0], 16)   # Convert the first part of the move to an integer
        y = int(move[1:], 16)  # Convert the second part of the move to an integer
        return x, y

    def score(self, score):
        print(f"Your score: {score}")

    def shutdown(self):
        pass


import random

class RandomPlayer(Player):

    def __init__(self, name):
        super().__init__(name)

    def get_move(self, game_state):
        # Get the current board from the game state
        board = game_state["board"]
        
        # Get the list of available moves (empty spots on the board)
        available_moves = [(i, j) for i, row in enumerate(board) for j, spot in enumerate(row) if spot == ' ']

        # Choose a random move from the list of available moves
        move = random.choice(available_moves)

        return move

    def score(self, score):
        pass
        # print(f"Random player score: {score}")

    def shutdown(self):
        pass
