import pytest
from unittest.mock import patch
from tic_tac_toe import TicTacToe, play_game

@pytest.fixture
def new_game():
    return TicTacToe()

def test_set_player_symbols_valid(new_game):
    assert new_game.set_player_symbols('X', 'O') == True

def test_set_player_symbols_invalid(new_game):
    assert new_game.set_player_symbols('X', 'X') == False

def test_validate_move_valid(new_game):
    assert new_game.validate_move(0) == (True, "Valid move")

def test_validate_move_invalid(new_game):
    assert new_game.validate_move(10) == (False, "Move must be between 0 and 8")

def test_make_move_success(new_game):
    new_game.current_player = 'X'
    assert new_game.make_move(0) == (True, "Move successful")

def test_make_move_win(new_game):
    new_game.current_player = 'X'
    new_game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
    assert new_game.make_move(6) == (True, "Player X wins!")

def test_undo_move_empty(new_game):
    assert new_game.undo_move() == (False, "No moves to undo.")

def test_undo_move_success(new_game):
    new_game.make_move(0)
    assert new_game.undo_move() == (True, "Last move undone.")

def test_check_winner_horizontal(new_game):
    new_game.current_player = 'X'
    new_game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
    assert new_game.check_winner(2) == True

@patch('random.choice', return_value=4)
def test_suggest_move(mock_choice, new_game):
    assert new_game.suggest_move() == 4
    mock_choice.assert_called()

def test_save_game(new_game):
    with patch('builtins.open', create=True) as mock_open:
        new_game.save_game()
        mock_open.assert_called_once_with("tictactoe_save.json", "w")

def test_load_game_not_found(new_game):
    with patch('builtins.open', side_effect=FileNotFoundError):
        new_game.load_game()
        assert new_game.board == [' ' for _ in range(9)]

def test_load_game_found(new_game):
    game_state = {
        "board": ['X', 'O', 'X', ' ', 'O', ' ', ' ', 'X', 'O'],
        "scores": {'X': 1, 'O': 2, 'Draws': 3},
        "current_player": 'O',
        "move_history": [(0, 'X'), (1, 'O')],
        "player_symbols": {'X': 'A', 'O': 'B'}
    }
    with patch('builtins.open', create=True) as mock_open:
        with patch('json.load', return_value=game_state):
            new_game.load_game()
            assert new_game.board == game_state["board"]
            assert new_game.scores == game_state["scores"]
            assert new_game.current_player == game_state["current_player"]
            assert new_game.move_history == game_state["move_history"]
            assert new_game.player_symbols == game_state["player_symbols"]

def test_replay_game_empty_history(new_game):
    with patch('builtins.print') as mock_print:
        new_game.replay_game()
        mock_print.assert_called_with("No game to replay.")

def test_replay_game_with_moves(new_game):
    new_game.make_move(0)
    new_game.make_move(1)
    with patch('builtins.print') as mock_print:
        new_game.replay_game()
        assert mock_print.call_count == 11

```