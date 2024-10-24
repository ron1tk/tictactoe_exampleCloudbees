import random
import json

class TicTacToe:
    def __init__(self, board_size=3):
        self.board_size = board_size
        self.board = [' ' for _ in range(board_size * board_size)]
        self.current_winner = None
        self.move_history = []
        self.scores = {'X': 0, 'O': 0, 'Draws': 0}
        self.current_player = 'X'

    def print_board(self):
        for row in range(self.board_size):
            print('| ' + ' | '.join(self.board[row*self.board_size:(row+1)*self.board_size]) + ' |')

    def validate_move(self, square):
        if not 0 <= square < self.board_size * self.board_size:
            return False, "Move must be between 0 and {}".format(self.board_size * self.board_size - 1)
        if self.board[square] != ' ':
            return False, "Square already occupied"
        return True, "Valid move"

    def make_move(self, square):
        valid, message = self.validate_move(square)
        if not valid:
            return False, message
        self.board[square] = self.current_player
        self.move_history.append((square, self.current_player))
        if self.check_winner(square):
            self.current_winner = self.current_player
            self.scores[self.current_player] += 1  # Update score for the winner
            return True, "Player {} wins!".format(self.current_player)
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True, "Move successful"

    def undo_move(self):
        """Undo the last move made, if any."""
        if not self.move_history:
            return False, "No moves to undo."
        last_move, last_player = self.move_history.pop()
        self.board[last_move] = ' '
        self.current_player = last_player
        return True, "Last move undone."

    def check_winner(self, square):
        row_ind = square // self.board_size
        col_ind = square % self.board_size
        row = self.board[row_ind*self.board_size:(row_ind+1)*self.board_size]
        col = [self.board[col_ind+i*self.board_size] for i in range(self.board_size)]

        def check_line(line):
            return all(spot == self.current_player for spot in line)

        if check_line(row) or check_line(col):
            return True
        if square % (self.board_size + 1) == 0:  # Check diagonal
            if check_line([self.board[i] for i in range(0, self.board_size*self.board_size, self.board_size+1)]):
                return True
        if square % (self.board_size - 1) == 0:  # Check anti-diagonal
            if check_line([self.board[i] for i in range(self.board_size-1, self.board_size*self.board_size-1, self.board_size-1)]):
                return True
        return False

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == ' ']

    def is_board_full(self):
        return ' ' not in self.board

    def reset_game(self):
        self.board = [' ' for _ in range(self.board_size * self.board_size)]
        self.current_winner = None
        self.move_history = []
        self.current_player = 'X'
        print("Game has been reset!")

    def print_scores(self):
        print(f"Scores: X - {self.scores['X']}, O - {self.scores['O']}, Draws - {self.scores['Draws']}")

    def reset_scores(self):
        """Reset the scores for both players."""
        self.scores = {'X': 0, 'O': 0, 'Draws': 0}
        print("Scores have been reset!")

    def suggest_move(self):
        """Suggest a random available move for the current player."""
        moves = self.available_moves()
        if moves:
            suggestion = random.choice(moves)
            print(f"Suggested move for {self.current_player}: {suggestion}")
            return suggestion
        return None

    def save_game(self, filename="tictactoe_save.json"):
        """Save the current game state to a file."""
        game_state = {
            "board": self.board,
            "scores": self.scores,
            "current_player": self.current_player,
            "move_history": self.move_history
        }
        with open(filename, "w") as f:
            json.dump(game_state, f)
        print(f"Game saved to {filename}.")

    def load_game(self, filename="tictactoe_save.json"):
        """Load the game state from a file."""
        try:
            with open(filename, "r") as f:
                game_state = json.load(f)
                self.board = game_state["board"]
                self.scores = game_state["scores"]
                self.current_player = game_state["current_player"]
                self.move_history = game_state["move_history"]
            print(f"Game loaded from {filename}.")
        except FileNotFoundError:
            print(f"No saved game found at {filename}.")

def play_game():
    game = TicTacToe()
    print("Welcome to Tic Tac Toe!")
    print("Enter -1 at any time to reset the game.")
    print("Enter -2 to undo the last move.")
    print("Enter -3 to get a move suggestion.")
    print("Enter -4 to save the game.")
    print("Enter -5 to load a saved game.")
    while True:
        game.print_board()
        try:
            square = int(input(f"Turn for {game.current_player}. Move on which space? (0-{game.board_size*game.board_size - 1}): "))
            if square == -1:  # Check if the reset command is entered
                game.reset_game()
                continue
            elif square == -2:  # Undo last move
                success, msg = game.undo_move()
                print(msg)
                continue
            elif square == -3:  # Suggest a move
                game.suggest_move()
                continue
            elif square == -4:  # Save the game
                game.save_game()
                continue
            elif square == -5:  # Load a saved game
                game.load_game()
                continue
            success, msg = game.make_move(square)
            print(msg)
            if success:
                if msg.startswith("Player"):
                    print("Game Over")
                    game.print_board()  # Show the final board
                    game.print_scores()  # Print scores after game ends
                    break
                elif game.is_board_full():
                    print("It's a tie!")
                    game.scores['Draws'] += 1  # Update score for a draw
                    game.print_board()  # Show the final board
                    game.print_scores()  # Print scores after game ends
                    break
        except ValueError:
            print("Please enter a valid number.")

if __name__ == '__main__':
    play_game()
