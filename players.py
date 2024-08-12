import random
from typing import Tuple, Optional
from board import Board


class Player:
    """Abstract base class for a player."""

    def __init__(self, mark: str) -> None:
        self.mark: str = mark

    def make_move(self, board: Board) -> Tuple[int, int]:
        """Abstract method for making a move."""
        raise NotImplementedError("Subclasses must implement this method.")


class HumanPlayer(Player):
    """Class for a human player."""

    def make_move(self, board: Board) -> Tuple[int, int]:
        """Prompt the human player for a move."""
        while True:
            try:
                row, col = map(int, input(f"Player {self.mark}, enter row and column (0-2) separated by space: ").split())
                if board.is_valid_move(row, col):
                    return row, col
                else:
                    print("Invalid move. The spot is taken or out of bounds. Try again.")
            except ValueError:
                print("Invalid input. Please enter two numbers separated by space.")


class RandomAI(Player):
    """Class for an AI player that makes random moves."""

    def make_move(self, board: Board) -> Tuple[int, int]:
        """Make a random move."""
        available_moves = [(r, c) for r in range(3) for c in range(3) if board.is_valid_move(r, c)]
        return random.choice(available_moves)


class StrategicAI(Player):
    """Class for an AI player that makes strategic moves."""

    def make_move(self, board: Board) -> Tuple[int, int]:
        """Make a move based on a basic strategy to win or block."""
        for r in range(3):
            for c in range(3):
                if board.is_valid_move(r, c):
                    # Check if AI can win with this move
                    board.make_temporary_move(r, c, self.mark)
                    if board.check_winner(self.mark):
                        board.undo_move(r, c)
                        return r, c
                    board.undo_move(r, c)

                    # Check if opponent can win with this move
                    opponent_mark = "X" if self.mark == "O" else "O"
                    board.make_temporary_move(r, c, opponent_mark)
                    if board.check_winner(opponent_mark):
                        board.undo_move(r, c)
                        return r, c
                    board.undo_move(r, c)

        # If no immediate win or block, return a random move
        return RandomAI(self.mark).make_move(board)


class OptimalAI(Player):
    """Class for an AI player that makes optimal moves using Minimax with Alpha-Beta Pruning."""

    def make_move(self, board: Board) -> Tuple[int, int]:
        """Make a move based on Minimax with Alpha-Beta Pruning."""
        best_move, _ = self.minimax(board, True, float('-inf'), float('inf'))
        if best_move is None:
            raise RuntimeError("No valid move found.")
        return best_move

    def minimax(self, board: Board, is_maximizing: bool, alpha: float, beta: float) -> Tuple[Optional[Tuple[int, int]], float]:
        """Perform Minimax algorithm with Alpha-Beta Pruning."""
        if board.check_winner(self.mark):
            return None, 1
        elif board.check_winner("X" if self.mark == "O" else "O"):
            return None, -1
        elif board.is_draw():
            return None, 0

        best_move = None
        if is_maximizing:
            best_score = float('-inf')
            for r in range(3):
                for c in range(3):
                    if board.is_valid_move(r, c):
                        board.place_mark(r, c, self.mark)
                        _, score = self.minimax(board, False, alpha, beta)
                        board.undo_move(r, c)
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_move, best_score
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if board.is_valid_move(r, c):
                        board.place_mark(r, c, "X" if self.mark == "O" else "O")
                        _, score = self.minimax(board, True, alpha, beta)
                        board.undo_move(r, c)
                        if score < best_score:
                            best_score = score
                            best_move = (r, c)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_move, best_score
