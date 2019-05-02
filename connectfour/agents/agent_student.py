# s3595854 - Japan Patel
from connectfour.agents.computer_player import RandomAgent
import random
import math


class StudentAgent(RandomAgent):

    opponent_id = 2
    opponent_moves = []

    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 3

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            A tuple of two integers, (row, col)
        """
        # assigns id to the opponent player
        if(self.id != 1):
            self.opponent_id = 1

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append(move)
            vals.append(self.dfMiniMax(next_state, 1, -math.inf, math.inf))
        best_move = moves[vals.index(max(vals))]

        # return best row and column
        return best_move

    # Goal return column with maximized scores of all possible next states
    def dfMiniMax(self, board, depth, alpha, beta):
        # Terminal state check
        if depth == self.MaxDepth:
            if board.winner() == self.id or board.winner() == self.opponent_id:
                terminal_reward = self.calculate_winner_reward(board)
                return terminal_reward
            else:
                return self.evaluateBoardState(board)

        moves = []
        if depth % 2 == 1:
            # Minimising player
            min_vals = []
            for move in board.valid_moves():
                next_state = board.next_state(self.id % 2 + 1, move[1])
                moves.append(move)
                min_vals.append(self.dfMiniMax(next_state, depth + 1, alpha, beta))
                new_reward = min(min_vals)
                beta = min(beta, new_reward)
                if alpha >= beta:
                    break
            return new_reward
        else:
            # maximising player
            max_vals = []
            for move in board.valid_moves():
                next_state = board.next_state(self.id, move[1])
                moves.append(move)
                max_vals.append(self.dfMiniMax(next_state, depth + 1, alpha, beta))
                new_reward = max(max_vals)
                alpha = max(alpha, new_reward)
                if alpha >= beta:
                    break
            return new_reward

    def evaluateBoardState(self, board):
        """
        Evaluates board for the current state of the board
        and reward the state on moves
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            reward in int
        """

        reward = 0
        reward += self.calculate_horizontal_move_reward(board)
        reward += self.calculate_vertical_move_reward(board)
        reward += self.calculate_diagonal_move_reward(board)

        reward += self.calculate_center_column_reward(board)

        return reward

    def calculate_winner_reward(self, board):
        """
        Rewards very high number to the player
        on winning or a very low number on
        opponent player's wining
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            reward in int
        """
        if board.winner() == self.id:
            return 10000
        elif board.winner() == self.opponent_id:
            return -10000

    def calculate_horizontal_move_reward(self, board):
        """
        Gets horizontal calculated reward based on player's move
        and opponent move
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            reward in int
        """
        horizontal_reward = 0
        for column in range(board.DEFAULT_WIDTH):
            columns = []
            for row in range(board.DEFAULT_HEIGHT):
                columns.append(board.get_cell_value(row, column))
            for r in range(board.DEFAULT_HEIGHT - board.num_to_connect + 1):
                player_moves = columns[r:r + board.num_to_connect]
                horizontal_reward += self.assess_reward(player_moves)
        return horizontal_reward

    def calculate_vertical_move_reward(self, board):
        """
        Gets vertical calculated reward based on player's move
        and opponent move
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            reward in int
        """
        vertical_reward = 0
        for row in range(board.DEFAULT_HEIGHT):
            rows = []
            for column in range(board.DEFAULT_WIDTH):
                rows.append(board.get_cell_value(row, column))
            for c in range(board.DEFAULT_WIDTH - board.num_to_connect + 1):
                player_moves = rows[c:c + board.num_to_connect]
                vertical_reward += self.assess_reward(player_moves)
        return vertical_reward

    def calculate_diagonal_move_reward(self, board):
        """
        Gets diagonal calculated reward based on player's move
        and opponent move
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            reward in int
        """
        diagonal_reward = 0
        for r in range(board.DEFAULT_HEIGHT - board.num_to_connect + 1):
            for c in range(board.DEFAULT_WIDTH - board.num_to_connect + 1):
                player_moves = [board.get_cell_value(
                            r + board.num_to_connect - 1 - i, c + i
                            ) for i in range(board.num_to_connect)]
                diagonal_reward += self.assess_reward(player_moves)

        for r in range(board.DEFAULT_HEIGHT - board.num_to_connect + 1):
            for c in range(board.DEFAULT_WIDTH - board.num_to_connect + 1):
                player_moves = [board.get_cell_value(
                            r + i, c + i
                            ) for i in range(board.num_to_connect)]
                diagonal_reward += self.assess_reward(player_moves)

        return diagonal_reward

    def calculate_center_column_reward(self, board):
        """
        Gets reward based on player's move in center
        Args:
            board: An instance of `Board` that is the current state of the board.
        Returns:
            reward in int
        """
        center_column_reward = 0
        center_column = math.floor(board.DEFAULT_WIDTH / 2)
        center_rows = []

        for row in range(board.DEFAULT_HEIGHT):
            center_rows.append(board.get_cell_value(row, center_column))
        agent_piece_count = center_rows.count(self.id)
        center_column_reward += agent_piece_count * 2

        return center_column_reward

    def assess_reward(self, player_moves):
        """
        Based on how close the player is to win,
        this function assigns a reward to that move
        Args:
            player_moves: all player moves for specific type (i.e. horizontal, vertical, diagonal).
        Returns:
            reward in int
        """
        reward = 0
        # reward checking for opponent to make sure that player is not losing
        if player_moves.count(self.opponent_id) == 3 and player_moves.count(0) == 1:
            reward -= 20

        # reward checking for student agent
        if player_moves.count(self.id) == 3 and player_moves.count(0) == 1:
            reward += 10
        elif player_moves.count(self.id) == 2 and player_moves.count(0) == 2:
            reward += 4

        return reward
