import pytest
from unittest.mock import patch
from tic_tac_toe import TicTacToe

@pytest.fixture
def new_game():
    return TicTacToe()

def test_set_player_symbols():
    game = TicTacToe()
    assert game.set_player_symbols('X', 'O') == True
    assert game.set_player_symbols('X', 'X') == False

def test_validate_move():
    game = TicTacToe()
    assert game.validate_move(-1) == (False, "Move must be between 0 and 8")
    assert game.validate_move(0) == (True, "Valid move")
    assert game.validate_move(4) == (False, "Square already occupied")

def test_make_move():
    game = TicTacToe()
    assert game.make_move(4) == (True, "Move successful")
    assert game.make_move(4) == (False, "Square already occupied")
    assert game.make_move(0) == (True, "Player X wins!")

def test_undo_move():
    game = TicTacToe()
    game.make_move(4)
    assert game.undo_move() == (True, "Last move undone")
    assert game.undo_move() == (False, "No moves to undo")

def test_check_winner():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'O']
    assert game.check_winner(0) == True
    assert game.check_winner(4) == True
    assert game.check_winner(8) == False

def test_available_moves():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', ' ']
    assert game.available_moves() == [8]

def test_is_board_full():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    assert game.is_board_full() == True

@patch('random.choice')
def test_suggest_move(mock_random_choice):
    mock_random_choice.return_value = 4
    game = TicTacToe()
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', ' ']
    assert game.suggest_move() == 4

def test_reset_game():
    game = TicTacToe()
    game.make_move(4)
    game.reset_game()
    assert game.board == [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

def test_reset_scores():
    game = TicTacToe()
    game.scores = {'X': 3, 'O': 2, 'Draws': 1}
    game.reset_scores()
    assert game.scores == {'X': 0, 'O': 0, 'Draws': 0}

def test_save_game(tmp_path):
    game = TicTacToe()
    filename = tmp_path / "test_save.json"
    game.save_game(filename)
    assert filename.is_file()

def test_load_game(tmp_path):
    game = TicTacToe()
    filename = tmp_path / "test_load.json"
    game.save_game(filename)
    game.board = ['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O']
    game.load_game(filename)
    assert game.board == ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'O']