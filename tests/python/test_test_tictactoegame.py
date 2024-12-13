```python
import pytest
from unittest.mock import patch
from tic_tac_toe import TicTacToe

@pytest.fixture
def tic_tac_toe():
    return TicTacToe()

def test_print_board(capsys, tic_tac_toe):
    tic_tac_toe.print_board()
    captured = capsys.readouterr()
    assert captured.out

def test_validate_move(tic_tac_toe):
    assert tic_tac_toe.validate_move(0) == (True, "Valid move")
    assert tic_tac_toe.validate_move(10) == (True, "Valid move")
    assert tic_tac_toe.validate_move(-1) == (False, "Move must be between 0 and 8")
    assert tic_tac_toe.validate_move(5) == (False, "Square already occupied")

def test_make_move(tic_tac_toe):
    tic_tac_toe.make_move(0)
    assert tic_tac_toe.current_player == 'O'
    assert tic_tac_toe.board[0] == 'X'

@patch('tic_tac_toe.TicTacToe.check_winner', return_value=True)
def test_check_winner(mock_check_winner, tic_tac_toe):
    assert tic_tac_toe.check_winner(0)

def test_available_moves(tic_tac_toe):
    tic_tac_toe.board = ['X', 'O', ' ', ' ', 'X', 'O', 'O', 'X', 'O']
    assert tic_tac_toe.available_moves() == [2, 3]

def test_is_board_full(tic_tac_toe):
    tic_tac_toe.board = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O']
    assert tic_tac_toe.is_board_full()

def test_reset_game(tic_tac_toe):
    tic_tac_toe.reset_game()
    assert tic_tac_toe.board == [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

def test_print_scores(capsys, tic_tac_toe):
    tic_tac_toe.print_scores()
    captured = capsys.readouterr()
    assert captured.out
```  