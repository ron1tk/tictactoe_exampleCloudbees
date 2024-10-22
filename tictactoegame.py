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
            return True, "Player {} wins!".format(self.current_player)
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True, "Move successful"

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

def play_game():
    game = TicTacToe()
    while True:
        game.print_board()
        square = input("Turn for {}. Move on which space? (0-{}) ".format(game.current_player, game.board_size*game.board_size - 1))
        try:
            square = int(square)
            success, msg = game.make_move(square)
            print(msg)
            if success:
                if msg.startswith("Player"):
                    print("Game Over")
                    break
                elif game.is_board_full():
                    print("It's a tie!")
                    break
        except ValueError:
            print("Please enter a number.")
    
    game.print_board()

if __name__ == '__main__':
    play_game()
