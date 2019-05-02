# s3595854 - Japan Patel
from connectfour.agents.computer_player import RandomAgent
import random
import math


class StudentAgent(RandomAgent):

    opponent_player = 2
    opponent_moves = []

    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 2

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            A tuple of two integers, (row, col)
        """
        # assigns id to the opponent player
        if(self.id != 1):
            self.opponent_player = 1

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            # print(str(moves))
            next_state = board.next_state(self.id, move[1])
            moves.append(move)
            vals.append(self.dfMiniMax(next_state, 1))
            print(str(moves))
            print(str(vals))
        bestMove = moves[vals.index(max(vals))]

        # return best row and column
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states
        if depth == self.MaxDepth:
            if board.winner() == self.id:
                print("student is winning")
                return 10000
            elif board.winner() == self.opponent_player:
                print("opponent is winning")
                return -10000
            else:
                return self.evaluateBoardState(board)

        moves = []
        if depth % 2 == 1:
            # Minimising player
            min_vals = []
            val = math.inf
            for move in board.valid_moves():
                next_state = board.next_state(self.id % 2 + 1, move[1])
                moves.append(move)
                min_vals.append(self.dfMiniMax(next_state, depth + 1))
                new_reward = min(min_vals)
        else:
            # maximising player
            max_vals = []
            val = -math.inf
            for move in board.valid_moves():
                next_state = board.next_state(self.id, move[1])
                moves.append(move)
                max_vals.append(self.dfMiniMax(next_state, depth + 1))
                new_reward = max(max_vals)

        return new_reward

    def reward_next_move(self, board):
        reward = 0

        # reward for vertical
        for row in range(board.DEFAULT_HEIGHT):
            rows = []
            for column in range(board.DEFAULT_WIDTH):
                rows.append(board.get_cell_value(row, column))
            for c in range(board.DEFAULT_WIDTH - 3):
                connect = rows[c:c + board.num_to_connect]
                reward += self.assess_reward(connect)

        # reward for horizontal
        for column in range(board.DEFAULT_WIDTH):
            columns = []
            for row in range(board.DEFAULT_HEIGHT):
                columns.append(board.get_cell_value(row, column))
            for r in range(board.DEFAULT_HEIGHT - 3):
                connect = columns[r:r + board.num_to_connect]
                reward += self.assess_reward(connect)

        # reward for diagonal
        for r in range(board.DEFAULT_HEIGHT - 3):
            for c in range(board.DEFAULT_WIDTH - 3):
                connect = [board.get_cell_value(r + 3 - i, c + i) for i in range(board.num_to_connect)]
                reward += self.assess_reward(connect)
        for r in range(board.DEFAULT_HEIGHT - 3):
            for c in range(board.DEFAULT_WIDTH - 3):
                connect = [board.get_cell_value(r + i, c + i) for i in range(board.num_to_connect)]
                reward += self.assess_reward(connect)
        
        return reward

    def assess_reward(self, connect):
        reward = 0
        # reward checking for opponent
        if connect.count(self.opponent_player) == 3 and connect.count(0) == 1:
            reward -= 20

        # reward checking for student agent
        if connect.count(self.id) == 4:
            print("4 in diagonal")
            reward += 500
        elif connect.count(self.id) == 3 and connect.count(0) == 1:
            print("3 in diagonal")
            reward += 25
        elif connect.count(self.id) == 2 and connect.count(0) == 2:
            print("2 in diagonal")
            reward += 10
        return reward

    def evaluateBoardState(self, board):
        return self.reward_next_move(board)
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """