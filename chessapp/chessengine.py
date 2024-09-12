import chess
import random
class ChessGame:
    def __init__(self, mode='1v1'):
        self.board = chess.Board()
        self.current_turn = 'white'
        self.mode = mode

    def reset_board(self):
        self.board.reset()
        self.current_turn = 'white'

    def make_move(self, move_uci):
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
        print(self.board)

    def is_check(self):
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
