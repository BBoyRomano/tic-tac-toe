from typing import List


class Board:
    """Class representing the Tic-Tac-Toe board."""

    def __init__(self) -> None:
        self.board: List[List[str]] = [[" " for _ in range(3)] for _ in range(3)]

    def display(self) -> None:
        """Display the current state of the board with borders."""
        horizontal_line = "+---" * 3 + "+"
        print(horizontal_line)
        for row in self.board:
            print(f"| {' | '.join(row)} |")
            print(horizontal_line)

    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if the move is valid (within bounds and not occupied)."""
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == " "

    def place_mark(self, row: int, col: int, mark: str) -> None:
        """Place a mark on the board."""
        if not self.is_valid_move(row, col):
            raise ValueError("Invalid move: The spot is taken or out of bounds.")
        self.board[row][col] = mark

    def make_temporary_move(self, row: int, col: int, mark: str) -> None:
        """Temporarily place a mark (for AI calculations)."""
        self.board[row][col] = mark

    def undo_move(self, row: int, col: int) -> None:
        """Undo a move (for AI calculations)."""
        self.board[row][col] = " "

    def check_winner(self, mark: str) -> bool:
        """Check if the given mark has won the game."""
        winning_combinations = [
            [(0, 0), (0, 1), (0, 2)],  # Top row
            [(1, 0), (1, 1), (1, 2)],  # Middle row
            [(2, 0), (2, 1), (2, 2)],  # Bottom row
            [(0, 0), (1, 0), (2, 0)],  # Left column
            [(0, 1), (1, 1), (2, 1)],  # Middle column
            [(0, 2), (1, 2), (2, 2)],  # Right column
            [(0, 0), (1, 1), (2, 2)],  # Diagonal top-left to bottom-right
            [(0, 2), (1, 1), (2, 0)]   # Diagonal top-right to bottom-left
        ]
        return any(all(self.board[r][c] == mark for r, c in combo) for combo in winning_combinations)

    def is_draw(self) -> bool:
        """Check if the game is a draw (no empty spaces)."""
        return all(self.board[row][col] != " " for row in range(3) for col in range(3))
