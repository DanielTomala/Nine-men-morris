import random

from source.board import Board
from source.enums import PawnsNumber, Player
from source.game_logic import (check_mill, draw_starting_player,
                               is_any_possible_move)


def test_draw_starting_player(monkeypatch):
    board = Board()

    def mock_randint(s, e):
        return 1
    monkeypatch.setattr(random, "randint", mock_randint)
    draw_starting_player(board)
    assert board.starting_player() == Player.ONE


def test_is_game_still_played():
    pass


def test_is_any_possible_move():
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


def test_check_mill_three_pawns():
    board_1 = Board(PawnsNumber.THREE)
    field_A = board_1.field_by_id("A")
    field_B = board_1.field_by_id("B")

    field_A.set_player(Player.ONE)
    field_B.set_player(Player.ONE)

    assert check_mill(board_1, field_A) == (None, 0)
    assert check_mill(board_1, field_B) == (None, 0)

    field_C = board_1.field_by_id("C")
    field_C.set_player(Player.ONE)

    assert check_mill(board_1, field_A) == (Player.ONE, 1)
    assert check_mill(board_1, field_B) == (Player.ONE, 1)
    assert check_mill(board_1, field_C) == (Player.ONE, 1)

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

    board_3 = Board(PawnsNumber.THREE)
    field_B = board_3.field_by_id("B")
    field_E = board_3.field_by_id("E")
    field_H = board_3.field_by_id("H")

    field_B.set_player(Player.ONE)
    field_E.set_player(Player.ONE)
    field_H.set_player(Player.ONE)

    assert check_mill(board_3, field_B) == (Player.ONE, 1)
    assert check_mill(board_3, field_E) == (Player.ONE, 1)
    assert check_mill(board_3, field_H) == (Player.ONE, 1)

    board_4 = Board(PawnsNumber.THREE)
    field_D = board_4.field_by_id("D")
    field_E = board_4.field_by_id("E")
    field_F = board_4.field_by_id("F")

    field_D.set_player(Player.ONE)
    field_E.set_player(Player.ONE)
    field_F.set_player(Player.ONE)

    assert check_mill(board_4, field_D) == (Player.ONE, 1)
    assert check_mill(board_4, field_E) == (Player.ONE, 1)
    assert check_mill(board_4, field_F) == (Player.ONE, 1)


def test_check_mill_nine_pawns():
    board = Board(PawnsNumber.NINE)
    field_A = board.field_by_id("A")
    field_B = board.field_by_id("B")
    field_C = board.field_by_id("C")
    field_A.set_player(Player.ONE)
    field_B.set_player(Player.ONE)

    assert check_mill(board, field_A) == (None, 0)
    assert check_mill(board, field_B) == (None, 0)

    field_C.set_player(Player.ONE)
    assert check_mill(board, field_A) == (Player.ONE, 1)
    assert check_mill(board, field_B) == (Player.ONE, 1)
    assert check_mill(board, field_C) == (Player.ONE, 1)

    field_J = board.field_by_id("J")
    field_X = board.field_by_id("X")
    field_J.set_player(Player.ONE)

    assert check_mill(board, field_J) == (None, 0)

    field_X.set_player(Player.ONE)
    assert check_mill(board, field_J) == (Player.ONE, 1)
    assert check_mill(board, field_X) == (Player.ONE, 1)

    field_D = board.field_by_id("D")
    field_K = board.field_by_id("K")
    field_T = board.field_by_id("T")
    field_D.set_player(Player.TWO)
    field_K.set_player(Player.TWO)

    assert check_mill(board, field_D) == (None, 0)
    assert check_mill(board, field_K) == (None, 0)

    field_T.set_player(Player.TWO)
    assert check_mill(board, field_D) == (Player.TWO, 1)
    assert check_mill(board, field_K) == (Player.TWO, 1)
    assert check_mill(board, field_T) == (Player.TWO, 1)

    field_U = board.field_by_id("U")
    field_W = board.field_by_id("W")
    field_U.set_player(Player.TWO)

    assert check_mill(board, field_U) == (None, 0)

    field_W.set_player(Player.TWO)
    assert check_mill(board, field_U) == (Player.TWO, 1)
    assert check_mill(board, field_W) == (Player.TWO, 1)

    field_I = board.field_by_id("I")
    field_M = board.field_by_id("M")
    field_S = board.field_by_id("S")
    field_I.set_player(Player.ONE)
    field_M.set_player(Player.ONE)

    assert check_mill(board, field_I) == (None, 0)
    assert check_mill(board, field_M) == (None, 0)

    field_S.set_player(Player.ONE)
    assert check_mill(board, field_I) == (Player.ONE, 1)
    assert check_mill(board, field_M) == (Player.ONE, 1)
    assert check_mill(board, field_S) == (Player.ONE, 1)

    field_N = board.field_by_id("N")
    field_O = board.field_by_id("O")
    field_N.set_player(Player.ONE)

    assert check_mill(board, field_N) == (None, 0)

    field_O.set_player(Player.ONE)
    assert check_mill(board, field_N) == (Player.ONE, 1)
    assert check_mill(board, field_O) == (Player.ONE, 1)

    field_G = board.field_by_id("G")
    field_H = board.field_by_id("H")
    field_G.set_player(Player.ONE)

    assert check_mill(board, field_G) == (None, 0)

    field_H.set_player(Player.ONE)
    assert check_mill(board, field_G) == (Player.ONE, 1)
    assert check_mill(board, field_H) == (Player.ONE, 1)

    field_E = board.field_by_id("E")
    field_E.set_player(Player.ONE)
    assert check_mill(board, field_E) == (Player.ONE, 1)


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
