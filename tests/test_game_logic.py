import random
from turtle import pos

from ..source.board import Board
from ..source.enums import PawnsNumber, Player
from ..source.game_logic import check_is_any_possible_move, check_mill, get_starting_player, possible_moves


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

    assert check_mill(board, field_A)[0] is None
    assert check_mill(board, field_B)[0] is None

    field_C.set_player(Player.FIRST)
    assert check_mill(board, field_A)[0] == Player.FIRST
    assert check_mill(board, field_B)[0] == Player.FIRST
    assert check_mill(board, field_C)[0] == Player.FIRST

    field_J = board.field_by_id("J")
    field_X = board.field_by_id("X")
    field_J.set_player(Player.FIRST)

    assert check_mill(board, field_J)[0] is None

    field_X.set_player(Player.FIRST)
    assert check_mill(board, field_J)[0] == Player.FIRST
    assert check_mill(board, field_X)[0] == Player.FIRST

    field_D = board.field_by_id("D")
    field_K = board.field_by_id("K")
    field_T = board.field_by_id("T")
    field_D.set_player(Player.SECOND)
    field_K.set_player(Player.SECOND)

    assert check_mill(board, field_D)[0] is None
    assert check_mill(board, field_K)[0] is None

    field_T.set_player(Player.SECOND)
    assert check_mill(board, field_D)[0] == Player.SECOND
    assert check_mill(board, field_K)[0] == Player.SECOND
    assert check_mill(board, field_T)[0] == Player.SECOND

    field_U = board.field_by_id("U")
    field_W = board.field_by_id("W")
    field_U.set_player(Player.SECOND)

    assert check_mill(board, field_U)[0] is None

    field_W.set_player(Player.SECOND)
    assert check_mill(board, field_U)[0] == Player.SECOND
    assert check_mill(board, field_W)[0] == Player.SECOND

    field_I = board.field_by_id("I")
    field_M = board.field_by_id("M")
    field_S = board.field_by_id("S")
    field_I.set_player(Player.FIRST)
    field_M.set_player(Player.FIRST)

    assert check_mill(board, field_I)[0] is None
    assert check_mill(board, field_M)[0] is None

    field_S.set_player(Player.FIRST)
    assert check_mill(board, field_I)[0] == Player.FIRST
    assert check_mill(board, field_M)[0] == Player.FIRST
    assert check_mill(board, field_S)[0] == Player.FIRST

    field_N = board.field_by_id("N")
    field_O = board.field_by_id("O")
    field_N.set_player(Player.FIRST)

    assert check_mill(board, field_N)[0] is None

    field_O.set_player(Player.FIRST)
    assert check_mill(board, field_N)[0] == Player.FIRST
    assert check_mill(board, field_O)[0] == Player.FIRST

    field_G = board.field_by_id("G")
    field_H = board.field_by_id("H")
    field_G.set_player(Player.FIRST)

    assert check_mill(board, field_G)[0] is None

    field_H.set_player(Player.FIRST)
    assert check_mill(board, field_G)[0] == Player.FIRST
    assert check_mill(board, field_H)[0] == Player.FIRST

    field_E = board.field_by_id("E")
    field_E.set_player(Player.FIRST)
    assert check_mill(board, field_E)[0] == Player.FIRST


def test_possible_moves():
    board = Board(PawnsNumber.NINE)
    field_A = board.field_by_id("A")
    field_A.set_player(Player.FIRST)
    field_B = board.field_by_id("B")
    field_B.set_player(Player.FIRST)
    field_J = board.field_by_id("J")
    field_J.set_player(Player.SECOND)
    field_K = board.field_by_id("K")
    field_K.set_player(Player.SECOND)
    field_N = board.field_by_id("N")
    field_N.set_player(Player.FIRST)
    field_R = board.field_by_id("R")
    field_R.set_player(Player.FIRST)
    field_X = board.field_by_id("X")
    field_X.set_player(Player.SECOND)

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
    board_1.field_by_id("A").set_player(Player.FIRST)
    board_1.field_by_id("B").set_player(Player.SECOND)
    board_1.field_by_id("J").set_player(Player.SECOND)

    assert not check_is_any_possible_move(board_1, Player.FIRST)
    assert check_is_any_possible_move(board_1, Player.SECOND)

    board_1.field_by_id("C").set_player(Player.FIRST)

    assert check_is_any_possible_move(board_1, Player.FIRST)
    assert check_is_any_possible_move(board_1, Player.SECOND)

    board_1.field_by_id("E").set_player(Player.FIRST)
    board_1.field_by_id("K").set_player(Player.FIRST)
    board_1.field_by_id("X").set_player(Player.FIRST)

    assert check_is_any_possible_move(board_1, Player.FIRST)
    assert not check_is_any_possible_move(board_1, Player.SECOND)

    board_2 =  Board(PawnsNumber.NINE)
    board_2.field_by_id("K").set_player(Player.FIRST)
    board_2.field_by_id("D").set_player(Player.SECOND)
    board_2.field_by_id("L").set_player(Player.SECOND)
    board_2.field_by_id("T").set_player(Player.SECOND)

    assert check_is_any_possible_move(board_2, Player.FIRST)

    board_2.field_by_id("J").set_player(Player.SECOND)

    assert not check_is_any_possible_move(board_2, Player.FIRST)



def test_is_game_still_played():
    pass
