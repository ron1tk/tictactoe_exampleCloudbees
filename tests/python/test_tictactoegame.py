import sys
import os

# Adjust the path to ensure Python can find the module tictactoegame
# This goes two levels up from the current directory, reaching the root of the project
sys.path.insert(0, os.path.abspath('../../'))

import pytest
from unittest.mock import patch
from tictactoegame import TicTacToe  

@pytest.fixture
def game():
    return TicTacToe()

def test_set_player_symbols():
    game = TicTacToe()
    assert game.set_player_symbols('X', 'O') == True
    assert game.set_player_symbols('X', 'X') == False

def test_validate_move():
    game = TicTacToe()
    assert game.validate_move(5) == (True, "Valid move")
    assert game.validate_move(-1) == (False, "Move must be between 0 and 8")

def test_make_move():
    game = TicTacToe()
    assert game.make_move(4) == (True, "Move successful")
    assert game.make_move(4) == (False, "Square already occupied")

def test_undo_move():
    game = TicTacToe()
    game.make_move(4)
    assert game.undo_move() == (True, "Last move undone")
    assert game.undo_move() == (False, "No moves to undo")

def test_check_winner():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', ' ', 'O', 'X', ' ', ' ', 'X']
    assert game.check_winner(8) == True
    assert game.check_winner(3) == False

def test_available_moves():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', ' ', 'O', 'X', ' ', ' ', 'X']
    assert game.available_moves() == [3, 6, 7]

def test_is_board_full():
    game = TicTacToe()
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X']
    assert game.is_board_full() == True
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', ' ']
    assert game.is_board_full() == False

def test_reset_game():
    game = TicTacToe()
    game.make_move(4)
    game.reset_game()
    assert game.board == [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

def test_reset_scores():
    game = TicTacToe()
    game.scores = {'X': 2, 'O': 1, 'Draws': 0}
    game.reset_scores()
    assert game.scores == {'X': 0, 'O': 0, 'Draws': 0}

@patch('random.choice')
def test_suggest_move(mock_choice):
    mock_choice.return_value = 3
    game = TicTacToe()
    game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', ' ']
    assert game.suggest_move() == 3

@patch('json.dump')
def test_save_game(mock_dump):
    game = TicTacToe()
    game.save_game("test_save.json")
    mock_dump.assert_called()

@patch('json.load')
def test_load_game(mock_load):
    game = TicTacToe()
    game.load_game("test_load.json")
    mock_load.assert_called()