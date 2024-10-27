```python
import pytest
from unittest.mock import patch
from tic_tac_toe import TicTacToe

@pytest.fixture
def new_game():
    return TicTacToe()

def test_set_player_symbols(new_game):
    assert new_game.set_player_symbols('X', 'O') == True
    assert new_game.set_player_symbols('X', 'X') == False

def test_validate_move(new_game):
    assert new_game.validate_move(5) == (True, "Valid move")
    assert new_game.validate_move(10) == (False, "Move must be between 0 and 8")
    assert new_game.validate_move(4) == (False, "Square already occupied")

def test_make_move(new_game):
    assert new_game.make_move(0) == (True, "Move successful")
    assert new_game.make_move(4) == (True, "Move successful")
    assert new_game.make_move(8) == (True, "Player X wins!")

def test_undo_move(new_game):
    new_game.make_move(0)
    assert new_game.undo_move() == (True, "Last move undone")
    assert new_game.undo_move() == (False, "No moves to undo")

def test_check_winner(new_game):
    new_game.board = ['X', 'O', ' ', 'O', 'X', ' ', 'X', 'O', 'X']
    assert new_game.check_winner(0) == True
    assert new_game.check_winner(4) == True
    assert new_game.check_winner(8) == True
    assert new_game.check_winner(2) == False

def test_available_moves(new_game):
    new_game.board = ['X', 'O', ' ', 'O', 'X', ' ', 'X', 'O', 'X']
    assert new_game.available_moves() == [2, 5]

def test_is_board_full(new_game):
    new_game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    assert new_game.is_board_full() == True

@patch('builtins.input', side_effect=['X', 'O'])
def test_play_game(mock_input):
    play_game()

def test_save_and_load_game(new_game, tmp_path):
    new_game.save_game(tmp_path / "test_save.json")
    new_game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    new_game.load_game(tmp_path / "test_save.json")
    assert new_game.board == ['X', 'O', ' ', 'O', 'X', ' ', 'X', 'O', 'X']
```