```python
import pytest
from unittest.mock import patch
from tic_tac_toe import TicTacToe

@pytest.fixture
def game():
    return TicTacToe()

def test_set_player_symbols():
    game = TicTacToe()
    assert game.set_player_symbols('X', 'O') == True
    assert game.player_symbols['X'] == 'X'
    assert game.player_symbols['O'] == 'O'

def test_set_player_symbols_same_symbols():
    game = TicTacToe()
    assert game.set_player_symbols('X', 'X') == False

def test_validate_move():
    game = TicTacToe()
    assert game.validate_move(-1) == (False, "Move must be between 0 and 8")
    assert game.validate_move(5) == (True, "Valid move")
    game.board[5] = 'X'
    assert game.validate_move(5) == (False, "Square already occupied")

def test_make_move():
    game = TicTacToe()
    game.make_move(4)
    assert game.board[4] == 'X'
    assert game.current_player == 'O'

def test_undo_move():
    game = TicTacToe()
    game.make_move(4)
    success, _ = game.undo_move()
    assert success == True
    assert game.board[4] == ' '
    assert game.current_player == 'X'

def test_check_winner():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', ' ', ' ', ' ']
    assert game.check_winner(4) == True
    game.board = ['X', 'O', 'O', 'X', 'X', 'O', ' ', ' ', ' ']
    assert game.check_winner(2) == False

def test_available_moves():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    assert game.available_moves() == []

def test_is_board_full():
    game = TicTacToe()
    assert game.is_board_full() == False
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    assert game.is_board_full() == True

def test_reset_game():
    game = TicTacToe()
    game.make_move(4)
    game.reset_game()
    assert game.board == [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    assert game.current_player == 'X'

def test_suggest_move():
    game = TicTacToe()
    with patch('random.choice') as mock_random_choice:
        mock_random_choice.return_value = 5
        assert game.suggest_move() == 5

def test_save_game(tmp_path):
    game = TicTacToe()
    game.save_game(str(tmp_path / "test_save.json"))
    assert (tmp_path / "test_save.json").exists()

def test_load_game(tmp_path):
    game = TicTacToe()
    game.save_game(str(tmp_path / "test_load.json"))
    game.load_game(str(tmp_path / "test_load.json"))
    assert game.board == [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    assert game.current_player == 'X'
```
