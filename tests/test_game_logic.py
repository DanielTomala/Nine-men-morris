import random

from ..source.board import Board
from ..source.enums import PawnsNumber, Player
from ..source.game_logic import check_mill, get_starting_player


def test_get_starting_player(monkeypatch):
    def mock_randint(s, e):
        return 1
    monkeypatch.setattr(random, "randint", mock_randint)
    player = get_starting_player()
    assert player == Player.FIRST


def test_check_mill():
    board = Board(PawnsNumber.NINE)
    field_A = board.field_by_id("A")
    field_B = board.field_by_id("B")
    field_C = board.field_by_id("C")
    field_A.set_player(Player.FIRST)
    field_B.set_player(Player.FIRST)

    assert check_mill(board, field_A) is None
    assert check_mill(board, field_B) is None

    field_C.set_player(Player.FIRST)
    assert check_mill(board, field_A) == Player.FIRST
    assert check_mill(board, field_B) == Player.FIRST
    assert check_mill(board, field_C) == Player.FIRST

    field_J = board.field_by_id("J")
    field_X = board.field_by_id("X")
    field_J.set_player(Player.FIRST)

    assert check_mill(board, field_J) is None

    field_X.set_player(Player.FIRST)
    assert check_mill(board, field_J) == Player.FIRST
    assert check_mill(board, field_X) == Player.FIRST

    field_D = board.field_by_id("D")
    field_K = board.field_by_id("K")
    field_T = board.field_by_id("T")
    field_D.set_player(Player.SECOND)
    field_K.set_player(Player.SECOND)

    assert check_mill(board, field_D) is None
    assert check_mill(board, field_K) is None

    field_T.set_player(Player.SECOND)
    assert check_mill(board, field_D) == Player.SECOND
    assert check_mill(board, field_K) == Player.SECOND
    assert check_mill(board, field_T) == Player.SECOND

    field_U = board.field_by_id("U")
    field_W = board.field_by_id("W")
    field_U.set_player(Player.SECOND)

    assert check_mill(board, field_U) is None

    field_W.set_player(Player.SECOND)
    assert check_mill(board, field_U) == Player.SECOND
    assert check_mill(board, field_W) == Player.SECOND

    field_I = board.field_by_id("I")
    field_M = board.field_by_id("M")
    field_S = board.field_by_id("S")
    field_I.set_player(Player.FIRST)
    field_M.set_player(Player.FIRST)

    assert check_mill(board, field_I) is None
    assert check_mill(board, field_M) is None

    field_S.set_player(Player.FIRST)
    assert check_mill(board, field_I) == Player.FIRST
    assert check_mill(board, field_M) == Player.FIRST
    assert check_mill(board, field_S) == Player.FIRST

    field_N = board.field_by_id("N")
    field_O = board.field_by_id("O")
    field_N.set_player(Player.FIRST)

    assert check_mill(board, field_N) is None

    field_O.set_player(Player.FIRST)
    assert check_mill(board, field_N) == Player.FIRST
    assert check_mill(board, field_O) == Player.FIRST

    field_G = board.field_by_id("G")
    field_H = board.field_by_id("H")
    field_G.set_player(Player.FIRST)

    assert check_mill(board, field_G) is None

    field_H.set_player(Player.FIRST)
    assert check_mill(board, field_G) == Player.FIRST
    assert check_mill(board, field_H) == Player.FIRST

    field_E = board.field_by_id("E")
    field_E.set_player(Player.FIRST)
    assert check_mill(board, field_E) == Player.FIRST
