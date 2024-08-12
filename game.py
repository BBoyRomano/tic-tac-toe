from typing import List, Optional
from board import Board
from players import Player


class TicTacToeGame:
    """Class managing the Tic-Tac-Toe game logic."""

    def __init__(self, player1: Player, player2: Player) -> None:
        self.board: Board = Board()
        self.players: List[Player] = [player1, player2]
        self.current_player: Player = self.players[0]
        self.winner: Optional[str] = None

    def display(self) -> None:
        """Display the board and game status."""
        self.board.display()
        if self.winner:
            if self.winner == "Draw":
                print("The game is a draw!")
            else:
                print(f"Player {self.winner} wins!")

    def switch_player(self) -> None:
        """Switch the current player."""
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def play(self) -> None:
        """Main game loop."""
        print("Welcome to Tic-Tac-Toe!")
        while self.winner is None:
            self.display()
            try:
                row, col = self.current_player.make_move(self.board)
                self.board.place_mark(row, col, self.current_player.mark)
                if self.board.check_winner(self.current_player.mark):
                    self.winner = self.current_player.mark
                elif self.board.is_draw():
                    self.winner = "Draw"
                self.switch_player()
            except ValueError as e:
                print(e)
        self.display()
        print("Game Over. Thanks for playing!")
