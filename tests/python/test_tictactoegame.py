```python
import pytest
from unittest.mock import patch
from tictactoe import TicTacToe

@pytest.fixture
def game():
    return TicTacToe()

def test_initialization(game):
    assert len(game.board) == 9
    assert game.current_winner is None
    assert len(game.move_history) == 0
    assert game.current_player == 'X'

def test_validate_move(game):
    assert game.validate_move(0) == (True, "Valid move")
    assert game.validate_move(9) == (False, "Move must be between 0 and 8")
    game.board[3] = 'X'
    assert game.validate_move(3) == (False, "Square already occupied")

def test_make_move(game):
    assert game.make_move(0) == (True, "Move successful")
    assert game.make_move(0) == (False, "Square already occupied")
    assert game.make_move(1) == (True, "Move successful")
    assert game.make_move(4) == (True, "Move successful")
    assert game.make_move(8) == (True, "Player X wins!")

def test_undo_move(game):
    game.make_move(0)
    assert game.undo_move() == (True, "Last move undone")
    assert game.undo_move() == (False, "No moves to undo")

@patch('random.choice', return_value=0)
def test_suggest_move(mock_random_choice, game):
    assert game.suggest_move() == 0

def test_check_winner(game):
    game.board = ['X', 'X', 'X', 'O', 'O', ' ', ' ', ' ', ' ']
    assert game.check_winner(2) == True
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    assert game.check_winner(0) == True
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    assert game.check_winner(4) == True

def test_available_moves(game):
    game.board = ['X', 'O', ' ', 'O', 'X', 'O', 'X', 'O', 'X']
    assert game.available_moves() == [2]

def test_is_board_full(game):
    assert game.is_board_full() == False
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    assert game.is_board_full() == True

def test_reset_game(game):
    game.make_move(0)
    game.reset_game()
    assert game.board == [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

def test_reset_scores(game):
    game.scores = {'X': 2, 'O': 1, 'Draws': 1}
    game.reset_scores()
    assert game.scores == {'X': 0, 'O': 0, 'Draws': 0}

def test_save_game(game, tmp_path):
    filename = tmp_path / "test_save.json"
    game.save_game(filename)
    assert filename.is_file()

def test_load_game(game, tmp_path):
    filename = tmp_path / "test_load.json"
    game.save_game(filename)
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    game.scores = {'X': 2, 'O': 1, 'Draws': 1}
    game.current_player = 'O'
    game.move_history = [(0, 'X'), (1, 'O'), (2, 'X')]
    game.load_game(filename)
    assert game.board == [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    assert game.scores == {'X': 0, 'O': 0, 'Draws': 0}
    assert game.current_player == 'X'
    assert game.move_history == []

def test_play_game(monkeypatch, capsys):
    user_inputs = ['0', '-1', '1', '-2', '-3', '-4', '-5']
    monkeypatch.setattr('builtins.input', lambda _: user_inputs.pop(0))
    play_game_output = """Game Over\n| X | X | X |\n| O | O | X |\n| X | O | O |\nScores: X - 1, O - 0, Draws - 0\n"""
    play_game()
    captured = capsys.readouterr()
    assert captured.out == play_game_output
```