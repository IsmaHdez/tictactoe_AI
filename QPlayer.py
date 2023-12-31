from Player import Player, RandomPlayer
import os
import random
import copy
import pandas as pd

LEARNING_RATE = 0.95
DISCOUNT_FACTOR_GAMMA = 0.15
CSV_COLUMNS = ["board",
                    "mv_0_0",
                    "mv_0_1",
                    "mv_0_2",
                    "mv_1_0",
                    "mv_1_1",
                    "mv_1_2",
                    "mv_2_0",
                    "mv_2_1",
                    "mv_2_2"]

class QPlayer(Player):
    
    #-----------| Init |-----------#
    def __init__(self, name):
        super().__init__(name)
        self.QTable = self._init_table()
        self.last_game_state = {}
        self.last_move = ()


    #----------| Public |----------#
    def get_move(self,game_state):
        move = self._get_best_move(game_state)
        
        self._set_reward(game_state,move,0)
        self.last_game_state = copy.deepcopy(game_state)
        self.last_move = copy.deepcopy(move)
        return move

    def score(self, score):
        reward = -10 if score == 0 else 10 if score == 1 else 5
        self._set_reward(self.last_game_state,self.last_move,reward)

    def shutdown(self):
        self._store_table()

    #---------| Private |---------#
    def _get_best_move(self, game_state):
        if self._is_state_in_QTable(game_state)==False:
            return self._get_random_move(game_state)
        else:
            row = self.QTable.loc[self.QTable['board'] == self._serialize_board(game_state)]
            valid_moves = self._valid_moves_as_columns(game_state)
            max_value = row[valid_moves].max(axis=1).values[0]
            mask = row == max_value
            columns_with_max_value = row.loc[:, mask.values[0]].columns
            column_with_best_move = random.choice(columns_with_max_value)
            return self._column_header_as_move(column_with_best_move)
        
    def _get_random_move(self, game_state):
        move = RandomPlayer('Temp').get_move(game_state)
        if self._is_state_in_QTable(game_state)==False:
            self._generate_new_row(game_state)
        return move

    def _generate_new_row(self, game_state):
        init_moves = {key: 0 for key in CSV_COLUMNS if key!='board'}
        new_row = pd.DataFrame([{'board': self._serialize_board(game_state), **init_moves}])
        self.QTable = pd.concat([self.QTable,new_row])
    
    def _set_reward(self, game_state, move, reward):
        q_value = self._get_Qvalue(game_state,move)
        updated_q_value = q_value + LEARNING_RATE *(reward + DISCOUNT_FACTOR_GAMMA * self._get_max_potential_reward(game_state,move) - q_value)
        self.QTable.loc[self.QTable['board']==self._serialize_board(game_state),self._move_as_column_header(move)] = updated_q_value

    def _get_Qvalue(self, game_state, move):
        return self.QTable.loc[self.QTable['board']==self._serialize_board(game_state),self._move_as_column_header(move)]
    
    def _get_max_potential_reward(self,game_state,move):
        new_game_state = copy.deepcopy(game_state)
        new_game_state['board'][move[0]][move[1]] = game_state['current_player']
        if self._is_state_in_QTable(new_game_state):
            q_table_row = self.QTable.loc[self.QTable['board']==self._serialize_board(new_game_state)]
            return q_table_row.iloc[:,1:].max().max()
        else:
            return 0

    #-------| Persistence |--------#
    def _init_table(self):
        file_path = f"./Qtable_{self.name}.csv"
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            return pd.DataFrame(columns=CSV_COLUMNS)

    def _store_table(self):
        file_path = f"./Qtable_{self.name}.csv"
        self.QTable.fillna(0).to_csv(file_path,index=False)        
    
    #---------| Utility |---------#
    def _is_state_in_QTable(self,game_state):
        return self.QTable['board'].eq(self._serialize_board(game_state)).any()
    
    def _serialize_board(self, game_state):
        return ''.join('E' if position == ' ' else 'P' if position==game_state['current_player'] else 'R' for row in game_state['board'] for position in row)

    def _move_as_column_header(self, move):
        return "mv_" + str(move[0]) + "_" + str(move[1])
    
    def _column_header_as_move(self, column_header):
        return tuple(map(int, column_header.split('_')[1:]))

    def _valid_moves_as_columns(self, game_state):
        board = game_state['board']
        available_moves = [(i, j) for i, row in enumerate(board) for j, spot in enumerate(row) if spot == ' ']
        columns_to_check=[]
        for move in available_moves:
            columns_to_check += [self._move_as_column_header(move)]
        return columns_to_check