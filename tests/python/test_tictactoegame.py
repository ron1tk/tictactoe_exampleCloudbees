import pytest
from unittest.mock import patch
from tictactoe import TicTacToe

@pytest.fixture
def game():
    return TicTacToe()

def test_set_player_symbols():
    game = TicTacToe()
    assert game.set_player_symbols('X', 'O') == True
    assert game.set_player_symbols('X', 'X') == False

def test_validate_move():
    game = TicTacToe()
    assert game.validate_move(0) == (True, "Valid move")
    assert game.validate_move(3) == (True, "Valid move")
    assert game.validate_move(9) == (False, "Move must be between 0 and 8")
    assert game.validate_move(5) == (True, "Valid move")
    assert game.validate_move(4) == (False, "Square already occupied")

@patch('tictactoe.TicTacToe.check_winner', return_value=True)
def test_make_move_winner(mock_check_winner):
    game = TicTacToe()
    assert game.make_move(0) == (True, "Player X wins!")

def test_make_move_no_winner():
    game = TicTacToe()
    assert game.make_move(0) == (True, "Move successful")
    assert game.make_move(1) == (True, "Move successful")
    assert game.make_move(3) == (True, "Move successful")
    assert game.make_move(4) == (True, "Move successful")
    assert game.make_move(6) == (False, "Square already occupied")

def test_undo_move():
    game = TicTacToe()
    game.make_move(0)
    assert game.undo_move() == (True, "Last move undone")
    assert game.undo_move() == (False, "No moves to undo")

def test_check_winner():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', ' ', 'X', 'O', 'O', ' ', 'X']
    assert game.check_winner(0) == True
    assert game.check_winner(1) == False
    assert game.check_winner(4) == True
    assert game.check_winner(8) == True
    assert game.check_winner(2) == False

def test_available_moves():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', ' ', 'X', 'O', 'O', ' ', 'X']
    assert game.available_moves() == [3, 7]

def test_is_board_full():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    assert game.is_board_full() == True

def test_reset_game():
    game = TicTacToe()
    game.make_move(0)
    game.reset_game()
    assert game.board == [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    assert game.current_winner == None

def test_suggest_move():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', ' ', 'X', 'O', 'O', ' ', 'X']
    with patch('random.choice', return_value=6):
        assert game.suggest_move() == 6

def test_save_game(tmp_path):
    game = TicTacToe()
    filename = tmp_path / "test_save.json"
    game.save_game(filename)
    assert filename.is_file()

def test_load_game(tmp_path):
    game = TicTacToe()
    filename = tmp_path / "test_load.json"
    game.save_game(filename)
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    game.current_player = 'O'
    game.scores = {'X': 1, 'O': 2, 'Draws': 0}
    game.move_history = [(0, 'X'), (1, 'O'), (3, 'X')]
    game.player_symbols = {'X': 'A', 'O': 'B'}
    game.load_game(filename)
    assert game.board == ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    assert game.current_player == 'O'
    assert game.scores == {'X': 1, 'O': 2, 'Draws': 0}
    assert game.move_history == [(0, 'X'), (1, 'O'), (3, 'X')]
    assert game.player_symbols == {'X': 'A', 'O': 'B'}