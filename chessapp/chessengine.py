import chess
import random
class ChessGame:
    def __init__(self, mode='1v1'):
        """
        Initialize a new ChessGame instance.

        Parameters:
        mode (str): The game mode. It can be either '1v1' (for two players) or 'AI' (for one player against AI).
                    Default is '1v1'.

        Attributes:
        board (chess.Board): The chess board.
        current_turn (str): The current player's turn. It can be either 'white' or 'black'.
        mode (str): The game mode.

        Returns:
        None
        """
        self.board = chess.Board()
        self.current_turn = 'white'
        self.mode = mode

    def reset_board(self):
        """
        Reset the chess board to its initial state and set the current turn to white.

        Parameters:
        None

        Returns:
        None

        This method clears the current chess board and resets the game state.
        It also sets the current turn to white, indicating that it's the white player's turn to make a move.
        """
        self.board.reset()
        self.current_turn = 'white'


    def make_move(self, move_uci):
        """
        Attempts to make a move on the chess board based on the given move in UCI format.

        Parameters:
        move_uci (str): The move to be made in UCI format (e.g., 'e2e4').

        Returns:
        bool: True if the move is valid and made successfully, False otherwise.
              If an exception occurs during the move attempt, the error message will be printed,
              and the function will return False.

        This function first attempts to convert the given move_uci string into a chess.Move object.
        It then checks if the move is a legal move on the current chess board.
        If the move is legal, it is pushed onto the board and the current turn is switched.
        If the move is not legal, an error message is printed, and the function returns False.
        If an exception occurs during the move attempt, the error message is printed,
        and the function returns False.
        """
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'
                return True
            else:
                print("Invalid move. Please try again.")
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def display_board(self):
        """
        Display the current state of the chess board.

        Parameters:
        None

        Returns:
        None

        This function prints the current state of the chess board to the console.
        It uses the built-in print function to display the board, which is stored as a string in the `self.board` attribute.
        """
        print(self.board)


    def is_check(self):
        """
        Check if the current player is in check.

        Parameters:
        None

        Returns:
        bool: True if the current player is in check, False otherwise.
              The `self.board.is_check()` method is used to determine if the current player is in check.
              This method returns True if the current player's king is under attack by an opponent's piece,
              and False otherwise.
        """
        return self.board.is_check()


    def is_checkmate(self):
        return self.board.is_checkmate()

    def is_stalemate(self):
        return self.board.is_stalemate()

    def is_game_over(self):
        return self.board.is_game_over()

    def get_legal_moves(self):
        return [move.uci() for move in self.board.legal_moves]

    def ai_move(self):
        # Very basic AI move (random choice)
        legal_moves = self.get_legal_moves()
        if legal_moves:
            return random.choice(legal_moves)
        return None

def main():
    mode = input("Choose game mode (1v1/AI): ").strip().lower()
    if mode not in ['1v1', 'ai']:
        print("Invalid mode selected. Defaulting to 1v1.")
        mode = '1v1'
    
    game = ChessGame(mode)

    print("Welcome to Chess!")
    while not game.is_game_over():
        game.display_board()
        print(f"{game.current_turn.capitalize()}'s turn")

        if game.current_turn == 'white' or mode == '1v1':
            move = input("Enter your move (e.g., e2e4): ")
        else:
            move = game.ai_move()
            if move:
                print(f"AI move: {move}")
            else:
                print("No legal moves available.")
                continue

        if game.make_move(move):
            if game.is_checkmate():
                game.display_board()
                print(f"Checkmate! {game.current_turn.capitalize()} wins!")
                break
            elif game.is_stalemate():
                game.display_board()
                print("Stalemate!")
                break
        else:
            print("Please try again.")

    print("Game over")
    game.display_board()

if __name__ == "__main__":
    main()
