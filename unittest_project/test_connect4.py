"""
Unit tests for Connect4 -- assigned units: switch_player() and is_full()
Run with:  pytest -v test_connect4.py
"""
import pytest
from main import Connect4


@pytest.fixture
def game():
    """A fresh Connect4 game for every test."""
    return Connect4()


def fill_board(game, symbols=("X", "O")):
    """Fill every cell, alternating symbols by column so no helper depends on drop_chip."""
    for r in range(game.ROWS):
        for c in range(game.COLS):
            game.board[r][c] = symbols[c % 2]


# --------------------------------------------------------------------------
# switch_player()
# --------------------------------------------------------------------------
class TestSwitchPlayer:
    def test_initial_player_is_x(self, game):
        assert game.current_player == 'X'

    def test_switch_x_to_o(self, game):
        game.switch_player()
        assert game.current_player == 'O'

    def test_switch_o_to_x(self, game):
        game.current_player = 'O'
        game.switch_player()
        assert game.current_player == 'X'

    def test_double_switch_returns_to_original(self, game):
        game.switch_player()
        game.switch_player()
        assert game.current_player == 'X'

    @pytest.mark.parametrize("switches, expected", [
        (1, 'O'), (2, 'X'), (3, 'O'), (10, 'X'), (11, 'O'),
    ])
    def test_multiple_switches_alternate(self, game, switches, expected):
        for _ in range(switches):
            game.switch_player()
        assert game.current_player == expected

    def test_switch_does_not_modify_board(self, game):
        game.board[5][0] = 'X'
        before = [row[:] for row in game.board]
        game.switch_player()
        assert game.board == before

    def test_current_player_is_always_valid_symbol(self, game):
        for _ in range(7):
            game.switch_player()
            assert game.current_player in ('X', 'O')

    def test_unexpected_player_value_defaults_to_x(self, game):
        """Edge case: any value other than 'X' becomes 'X' (documented behavior)."""
        game.current_player = '?'
        game.switch_player()
        assert game.current_player == 'X'


# --------------------------------------------------------------------------
# is_full()
# --------------------------------------------------------------------------
class TestIsFull:
    def test_empty_board_is_not_full(self, game):
        assert game.is_full() is False

    def test_completely_full_board_is_full(self, game):
        fill_board(game)
        assert game.is_full() is True

    def test_one_empty_cell_in_top_row_is_not_full(self, game):
        fill_board(game)
        game.board[0][3] = ' '
        assert game.is_full() is False

    @pytest.mark.parametrize("col", range(7))
    def test_each_top_row_column_empty_is_not_full(self, game, col):
        fill_board(game)
        game.board[0][col] = ' '
        assert game.is_full() is False

    def test_partially_filled_board_is_not_full(self, game):
        for r in range(3, 6):
            for c in range(game.COLS):
                game.board[r][c] = 'X'
        assert game.is_full() is False

    def test_all_columns_filled_except_one_is_not_full(self, game):
        for c in range(6):
            for _ in range(game.ROWS):
                game.drop_chip(c + 1)
                game.switch_player()
        assert game.is_full() is False

    def test_filling_all_columns_with_drop_chip_is_full(self, game):
        for c in range(1, game.COLS + 1):
            for _ in range(game.ROWS):
                assert game.drop_chip(c) is True
                game.switch_player()
        assert game.is_full() is True

    def test_no_more_chips_can_be_dropped_when_full(self, game):
        for c in range(1, game.COLS + 1):
            for _ in range(game.ROWS):
                game.drop_chip(c)
                game.switch_player()
        assert game.is_full()
        for c in range(1, game.COLS + 1):
            assert game.drop_chip(c) is False

    def test_is_full_does_not_modify_board(self, game):
        fill_board(game)
        before = [row[:] for row in game.board]
        game.is_full()
        assert game.board == before

    def test_is_full_only_inspects_top_row(self, game):
        """Documents implementation detail: only row 0 is checked.
        An (impossible-in-play) board with a full top row but empty lower
        cells is reported as full."""
        game.board[0] = ['X'] * game.COLS
        assert game.is_full() is True

    def test_full_after_final_move_with_alternating_players(self, game):
        """Both helpers working together across a whole game's worth of moves."""
        moves = 0
        for c in range(1, game.COLS + 1):
            for _ in range(game.ROWS):
                game.drop_chip(c)
                game.switch_player()
                moves += 1
        assert moves == 42
        assert game.current_player == 'X'   # even number of switches
        assert game.is_full()


"""
PROJECT DOCUMENTATION - PART 2: UNIT TESTING RESULTS
--------------------------------------------------------------------------
BUGS / ISSUES / OBSERVATIONS
--------------------------------------------------------------------------
No failing tests and no functional bugs in switch_player() or is_full().
Observations:

  a) is_full() only checks row 0 (the top row). This is correct for normal
     play because chips stack from the bottom, so a full top row implies a
     full board. However, if the board were edited directly (e.g. in tests),
     a full top row with empty cells below would still be reported as full.
     Not a bug in real gameplay; documented by test_is_full_only_inspects_top_row.

  b) switch_player() treats any value other than 'X' as "not X" and sets the
     player to 'X'. Fine for a game that only uses 'X' and 'O', but it does
     not validate current_player.

  c) Game-loop order: check_win() runs before is_full(), so a winning move
     that fills the last cell is correctly reported as a win, not a tie.

  d) (Outside assigned units) print_board() draws a separator of 15 dashes
     and column labels, which line up with the 7-column board, but the
     ANSI color codes will not render in some IDE consoles.
==========================================================================
"""