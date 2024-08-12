from game import TicTacToeGame
from players import HumanPlayer, RandomAI, StrategicAI, OptimalAI

def main() -> None:
    """Main function to start the game."""
    # Create players
    player1 = HumanPlayer("X")
    player2 = OptimalAI("O")

    # Initialize and play the game
    game = TicTacToeGame(player1, player2)
    game.play()

if __name__ == "__main__":
    main()
