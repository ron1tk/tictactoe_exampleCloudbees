from tictactoe import TicTacToe

def test_tic_tac_toe():
    game = TicTacToe()
    assert game.make_move(0, 'X') == True
    assert game.make_move(0, 'O') == False  # Invalid move, square already taken
    assert game.current_winner is None
    game.make_move(1, 'X')
    game.make_move(2, 'X')
    assert game.current_winner == 'X'  # X wins
