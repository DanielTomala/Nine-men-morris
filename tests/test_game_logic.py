import random

from ..source.board import Board
from ..source.enums import PawnsNumber, Player
from ..source.game_logic import (is_any_possible_move, check_mill,
                                 draw_starting_player, possible_moves)


def test_get_starting_player(monkeypatch):
    def mock_randint(s, e):
        return 1
    monkeypatch.setattr(random, "randint", mock_randint)
    player = draw_starting_player()
    assert player == Player.ONE


def test_check_mill_three_pawns():
    board_1 = Board(PawnsNumber.THREE)
    field_A = board_1.field_by_id("A")
    field_B = board_1.field_by_id("B")
    field_C = board_1.field_by_id("C")

    field_A.set_player(Player.ONE)
    field_B.set_player(Player.ONE)
    field_C.set_player(Player.ONE)

    assert check_mill(board_1, field_A) == (Player.ONE, 1)
    assert check_mill(board_1, field_B) == (Player.ONE, 1)
    assert check_mill(board_1, field_C) == (Player.ONE, 1)

    field_D = board_1.field_by_id("D")
    field_G = board_1.field_by_id("G")

    field_D.set_player(Player.ONE)
    field_G.set_player(Player.ONE)

    assert check_mill(board_1, field_A) == (Player.ONE, 2)
    assert check_mill(board_1, field_D) == (Player.ONE, 1)
    assert check_mill(board_1, field_G) == (Player.ONE, 1)

    board_2 = Board(PawnsNumber.THREE)
    field_C = board_2.field_by_id("C")
    field_E = board_2.field_by_id("E")
    field_G = board_2.field_by_id("G")

    field_C.set_player(Player.TWO)
    field_E.set_player(Player.TWO)
    field_G.set_player(Player.TWO)

    assert check_mill(board_2, field_C) == (Player.TWO, 1)
    assert check_mill(board_2, field_E) == (Player.TWO, 1)
    assert check_mill(board_2, field_G) == (Player.TWO, 1)

    field_A = board_2.field_by_id("A")
    field_I = board_2.field_by_id("I")

    field_A.set_player(Player.TWO)
    field_I.set_player(Player.TWO)

    assert check_mill(board_2, field_A) == (Player.TWO, 1)
    assert check_mill(board_2, field_E) == (Player.TWO, 2)
    assert check_mill(board_2, field_I) == (Player.TWO, 1)

    board_3 = Board(PawnsNumber.THREE)
    field_B = board_3.field_by_id("B")
    field_E = board_3.field_by_id("E")
    field_H = board_3.field_by_id("H")

    field_B.set_player(Player.ONE)
    field_E.set_player(Player.ONE)
    field_H.set_player(Player.ONE)

    assert check_mill(board_3, field_B) == (Player.TWO, 1)
    assert check_mill(board_3, field_E) == (Player.TWO, 1)
    assert check_mill(board_3, field_H) == (Player.TWO, 1)

    board_4 = Board(PawnsNumber.THREE)
    field_D = board_4.field_by_id("D")
    field_E = board_4.field_by_id("E")
    field_F = board_4.field_by_id("F")

    field_D.set_player(Player.ONE)
    field_E.set_player(Player.ONE)
    field_F.set_player(Player.ONE)

    assert check_mill(board_4, field_D) == (Player.TWO, 1)
    assert check_mill(board_4, field_E) == (Player.TWO, 1)
    assert check_mill(board_4, field_F) == (Player.TWO, 1)


def test_check_mill_nine_pawns():
    board = Board(PawnsNumber.NINE)
    field_A = board.field_by_id("A")
    field_B = board.field_by_id("B")
    field_C = board.field_by_id("C")
    field_A.set_player(Player.ONE)
    field_B.set_player(Player.ONE)

    assert check_mill(board, field_A)[0] is None
    assert check_mill(board, field_B)[0] is None

    field_C.set_player(Player.ONE)
    assert check_mill(board, field_A)[0] == Player.ONE
    assert check_mill(board, field_B)[0] == Player.ONE
    assert check_mill(board, field_C)[0] == Player.ONE

    field_J = board.field_by_id("J")
    field_X = board.field_by_id("X")
    field_J.set_player(Player.ONE)

    assert check_mill(board, field_J)[0] is None

    field_X.set_player(Player.ONE)
    assert check_mill(board, field_J)[0] == Player.ONE
    assert check_mill(board, field_X)[0] == Player.ONE

    field_D = board.field_by_id("D")
    field_K = board.field_by_id("K")
    field_T = board.field_by_id("T")
    field_D.set_player(Player.TWO)
    field_K.set_player(Player.TWO)

    assert check_mill(board, field_D)[0] is None
    assert check_mill(board, field_K)[0] is None

    field_T.set_player(Player.TWO)
    assert check_mill(board, field_D)[0] == Player.TWO
    assert check_mill(board, field_K)[0] == Player.TWO
    assert check_mill(board, field_T)[0] == Player.TWO

    field_U = board.field_by_id("U")
    field_W = board.field_by_id("W")
    field_U.set_player(Player.TWO)

    assert check_mill(board, field_U)[0] is None

    field_W.set_player(Player.TWO)
    assert check_mill(board, field_U)[0] == Player.TWO
    assert check_mill(board, field_W)[0] == Player.TWO

    field_I = board.field_by_id("I")
    field_M = board.field_by_id("M")
    field_S = board.field_by_id("S")
    field_I.set_player(Player.ONE)
    field_M.set_player(Player.ONE)

    assert check_mill(board, field_I)[0] is None
    assert check_mill(board, field_M)[0] is None

    field_S.set_player(Player.ONE)
    assert check_mill(board, field_I)[0] == Player.ONE
    assert check_mill(board, field_M)[0] == Player.ONE
    assert check_mill(board, field_S)[0] == Player.ONE

    field_N = board.field_by_id("N")
    field_O = board.field_by_id("O")
    field_N.set_player(Player.ONE)

    assert check_mill(board, field_N)[0] is None

    field_O.set_player(Player.ONE)
    assert check_mill(board, field_N)[0] == Player.ONE
    assert check_mill(board, field_O)[0] == Player.ONE

    field_G = board.field_by_id("G")
    field_H = board.field_by_id("H")
    field_G.set_player(Player.ONE)

    assert check_mill(board, field_G)[0] is None

    field_H.set_player(Player.ONE)
    assert check_mill(board, field_G)[0] == Player.ONE
    assert check_mill(board, field_H)[0] == Player.ONE

    field_E = board.field_by_id("E")
    field_E.set_player(Player.ONE)
    assert check_mill(board, field_E)[0] == Player.ONE


def test_check_mill_twelve_pawns():
    board = Board(PawnsNumber.TWELVE)
    field_A = board.field_by_id("A")
    field_D = board.field_by_id("D")
    field_G = board.field_by_id("G")

    field_A.set_player(Player.ONE)
    field_D.set_player(Player.ONE)
    field_G.set_player(Player.ONE)

    assert check_mill(board, field_A) == (Player.ONE, 1)
    assert check_mill(board, field_D) == (Player.ONE, 1)
    assert check_mill(board, field_G) == (Player.ONE, 1)

    field_C = board.field_by_id("C")
    field_F = board.field_by_id("F")
    field_I = board.field_by_id("I")

    field_C.set_player(Player.ONE)
    field_F.set_player(Player.ONE)
    field_I.set_player(Player.ONE)

    assert check_mill(board, field_C) == (Player.ONE, 1)
    assert check_mill(board, field_F) == (Player.ONE, 1)
    assert check_mill(board, field_I) == (Player.ONE, 1)

    field_P = board.field_by_id("P")
    field_T = board.field_by_id("T")
    field_X = board.field_by_id("X")

    field_P.set_player(Player.TWO)
    field_T.set_player(Player.TWO)
    field_X.set_player(Player.TWO)

    assert check_mill(board, field_P) == (Player.TWO, 1)
    assert check_mill(board, field_T) == (Player.TWO, 1)
    assert check_mill(board, field_X) == (Player.TWO, 1)

    field_S = board.field_by_id("S")
    field_W = board.field_by_id("W")
    field_Z = board.field_by_id("Z")

    field_S.set_player(Player.TWO)
    field_W.set_player(Player.TWO)
    field_Z.set_player(Player.TWO)

    assert check_mill(board, field_S) == (Player.TWO, 1)
    assert check_mill(board, field_W) == (Player.TWO, 1)
    assert check_mill(board, field_Z) == (Player.TWO, 1)


def test_check_mill_multiple_mills():
    board = Board(PawnsNumber.TWELVE)
    field_A = board.field_by_id("A")
    field_D = board.field_by_id("D")
    field_G = board.field_by_id("G")
    field_E = board.field_by_id("E")
    field_F = board.field_by_id("F")
    field_K = board.field_by_id("K")
    field_T = board.field_by_id("T")

    field_A.set_player(Player.ONE)
    field_D.set_player(Player.ONE)
    field_G.set_player(Player.ONE)
    field_E.set_player(Player.ONE)
    field_F.set_player(Player.ONE)
    field_K.set_player(Player.ONE)
    field_T.set_player(Player.ONE)

    assert check_mill(board, field_D) == (Player.ONE, 3)

    field_C = board.field_by_id("C")
    field_M = board.field_by_id("M")
    field_N = board.field_by_id("N")
    field_O = board.field_by_id("O")
    field_Z = board.field_by_id("Z")

    field_C.set_player(Player.TWO)
    field_M.set_player(Player.TWO)
    field_N.set_player(Player.TWO)
    field_O.set_player(Player.TWO)
    field_Z.set_player(Player.TWO)

    assert check_mill(board, field_O) == (Player.TWO, 2)


def test_possible_moves():
    board = Board(PawnsNumber.NINE)
    field_A = board.field_by_id("A")
    field_A.set_player(Player.ONE)
    field_B = board.field_by_id("B")
    field_B.set_player(Player.ONE)
    field_J = board.field_by_id("J")
    field_J.set_player(Player.TWO)
    field_K = board.field_by_id("K")
    field_K.set_player(Player.TWO)
    field_N = board.field_by_id("N")
    field_N.set_player(Player.ONE)
    field_R = board.field_by_id("R")
    field_R.set_player(Player.ONE)
    field_X = board.field_by_id("X")
    field_X.set_player(Player.TWO)

    assert possible_moves(board, field_A) == []
    assert possible_moves(board, field_B) == ["C", "E"]
    assert not possible_moves(board, field_B) == ["E", "C"]
    assert possible_moves(board, field_J) == []
    assert possible_moves(board, field_K) == ["D", "L", "T"]
    assert possible_moves(board, field_N) == ["F", "M", "O", "W"]
    assert possible_moves(board, field_R) == ["P", "S", "U"]
    assert possible_moves(board, field_X) == ["Y"]


def test_check_is_any_possible_move():
    board_1 = Board(PawnsNumber.NINE)
    board_1.field_by_id("A").set_player(Player.ONE)
    board_1.field_by_id("B").set_player(Player.TWO)
    board_1.field_by_id("J").set_player(Player.TWO)

    assert not is_any_possible_move(board_1, Player.ONE)
    assert is_any_possible_move(board_1, Player.TWO)

    board_1.field_by_id("C").set_player(Player.ONE)

    assert is_any_possible_move(board_1, Player.ONE)
    assert is_any_possible_move(board_1, Player.TWO)

    board_1.field_by_id("E").set_player(Player.ONE)
    board_1.field_by_id("K").set_player(Player.ONE)
    board_1.field_by_id("X").set_player(Player.ONE)

    assert is_any_possible_move(board_1, Player.ONE)
    assert not is_any_possible_move(board_1, Player.TWO)

    board_2 = Board(PawnsNumber.NINE)
    board_2.field_by_id("K").set_player(Player.ONE)
    board_2.field_by_id("D").set_player(Player.TWO)
    board_2.field_by_id("L").set_player(Player.TWO)
    board_2.field_by_id("T").set_player(Player.TWO)

    assert is_any_possible_move(board_2, Player.ONE)

    board_2.field_by_id("J").set_player(Player.TWO)

    assert not is_any_possible_move(board_2, Player.ONE)


def test_is_game_still_played():
    pass
