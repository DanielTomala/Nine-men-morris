from ..source.enums import PawnsNumber, Player, Position, PositionSquare
from ..source.board import Board, FIELD_IDS


def test_add_pawn():
    board = Board()
    field = board.fields()[0]
    board.add_pawn(field, Player.FIRST)
    assert field.player() == Player.FIRST


def test_add_pawn_field_already_occupied():
    board = Board()
    field = board.fields()[0]
    board.add_pawn(field, Player.FIRST)
    board.add_pawn(field, Player.SECOND)
    assert field.player() == Player.FIRST


def test_remove_pawn():
    board = Board()
    field = board.fields()[0]
    board.add_pawn(field, Player.FIRST)
    assert field.player() == Player.FIRST
    board.remove_pawn(field)
    assert field.player() is None


def test_move_pawn():
    board = Board()
    field_1 = board.fields()[0]
    field_2 = board.fields()[1]
    board.add_pawn(field_1, Player.FIRST)
    assert field_1.player() == Player.FIRST
    board.move_pawn(field_1, field_2, Player.FIRST)
    assert field_1.player() is None
    assert field_2.player() == Player.FIRST


def test_move_pawn_field_occupied():
    board = Board()
    field_1 = board.fields()[0]
    field_2 = board.fields()[1]
    board.add_pawn(field_1, Player.FIRST)
    board.add_pawn(field_2, Player.SECOND)
    assert field_1.player() == Player.FIRST
    assert field_2.player() == Player.SECOND
    board.move_pawn(field_1, field_2, Player.FIRST)
    assert field_1.player() == Player.FIRST
    assert field_2.player() == Player.SECOND


def test_move_pawn_no_connection():
    board = Board()
    field_1 = board.fields()[0]
    field_2 = board.fields()[2]
    board.add_pawn(field_1, Player.FIRST)
    assert field_1.player() == Player.FIRST
    board.move_pawn(field_1, field_2, Player.FIRST)
    assert field_1.player() == Player.FIRST


def test_check_mill():
    board = Board(PawnsNumber.NINE)
    field_A = board.field_by_id("A")
    field_B = board.field_by_id("B")
    field_C = board.field_by_id("C")
    field_A.set_player(Player.FIRST)
    field_B.set_player(Player.FIRST)
    field_C.set_player(Player.FIRST)
    assert board.check_mill(field_A) == Player.FIRST
    assert board.check_mill(field_B) == Player.FIRST
    assert board.check_mill(field_C) == Player.FIRST

    field_J = board.field_by_id("J")
    field_X = board.field_by_id("X")
    field_J.set_player(Player.FIRST)
    field_X.set_player(Player.FIRST)
    assert board.check_mill(field_J) == Player.FIRST
    assert board.check_mill(field_X) == Player.FIRST

    field_D = board.field_by_id("D")
    field_K = board.field_by_id("K")
    field_T = board.field_by_id("T")
    field_D.set_player(Player.SECOND)
    field_K.set_player(Player.SECOND)
    field_T.set_player(Player.SECOND)
    assert board.check_mill(field_D) == Player.SECOND
    assert board.check_mill(field_K) == Player.SECOND
    assert board.check_mill(field_T) == Player.SECOND

    field_U = board.field_by_id("U")
    field_W = board.field_by_id("W")
    field_U.set_player(Player.SECOND)
    field_W.set_player(Player.SECOND)
    assert board.check_mill(field_U) == Player.SECOND
    assert board.check_mill(field_W) == Player.SECOND

    field_I = board.field_by_id("I")
    field_M = board.field_by_id("M")
    field_S = board.field_by_id("S")
    field_I.set_player(Player.FIRST)
    field_M.set_player(Player.FIRST)
    field_S.set_player(Player.FIRST)
    assert board.check_mill(field_I) == Player.FIRST
    assert board.check_mill(field_M) == Player.FIRST
    assert board.check_mill(field_S) == Player.FIRST

    field_N = board.field_by_id("N")
    field_O = board.field_by_id("O")
    field_N.set_player(Player.FIRST)
    field_O.set_player(Player.FIRST)
    assert board.check_mill(field_N) == Player.FIRST
    assert board.check_mill(field_O) == Player.FIRST

    field_G = board.field_by_id("G")
    field_H = board.field_by_id("H")
    field_G.set_player(Player.FIRST)
    field_H.set_player(Player.FIRST)
    assert board.check_mill(field_G) == Player.FIRST
    assert board.check_mill(field_H) == Player.FIRST

    field_E = board.field_by_id("E")
    field_E.set_player(Player.FIRST)
    assert board.check_mill(field_E) == Player.FIRST


def test_players_pawns_number():
    board = Board()
    field_1 = board.fields()[0]
    field_2 = board.fields()[1]
    field_3 = board.fields()[5]
    field_1.set_player(Player.FIRST)
    field_2.set_player(Player.SECOND)
    field_3.set_player(Player.FIRST)
    assert board.player_pawns_number(Player.FIRST) == 2
    assert board.player_pawns_number(Player.SECOND) == 1


def test_field_by_given_positions():
    board = Board()
    field = board.field_by_positions(
        PositionSquare.OUTER, Position.TOP, Position.LEFT)
    assert field == board.fields()[0]


def test_create_nine_pawns_board():
    board = Board()
    board_fields = board._create_nine_pawns_board()
    assert board_fields[0].id() == FIELD_IDS[0]
    assert board_fields[0].coordiantes().square() == PositionSquare.OUTER
    assert board_fields[0].coordiantes(
    ).position_top_middle_bottom() == Position.TOP
    assert board_fields[0].coordiantes(
    ).position_left_center_right() == Position.LEFT

    assert board_fields[5].id() == FIELD_IDS[5]
    assert board_fields[5].coordiantes().square() == PositionSquare.MIDDLE
    assert board_fields[5].coordiantes(
    ).position_top_middle_bottom() == Position.TOP
    assert board_fields[5].coordiantes(
    ).position_left_center_right() == Position.RIGHT

    assert board_fields[11].id() == FIELD_IDS[11]
    assert board_fields[11].coordiantes().square() == PositionSquare.INNER
    assert board_fields[11].coordiantes(
    ).position_top_middle_bottom() == Position.MIDDLE
    assert board_fields[11].coordiantes(
    ).position_left_center_right() == Position.LEFT

    assert board_fields[12].id() == FIELD_IDS[12]
    assert board_fields[12].coordiantes().square() == PositionSquare.INNER
    assert board_fields[12].coordiantes(
    ).position_top_middle_bottom() == Position.MIDDLE
    assert board_fields[12].coordiantes(
    ).position_left_center_right() == Position.RIGHT

    assert board_fields[18].id() == FIELD_IDS[18]
    assert board_fields[18].coordiantes().square() == PositionSquare.MIDDLE
    assert board_fields[18].coordiantes(
    ).position_top_middle_bottom() == Position.BOTTOM
    assert board_fields[18].coordiantes(
    ).position_left_center_right() == Position.LEFT


def test_field_by_id():
    board = Board()
    field_1 = board.field_by_id("A")
    field_2 = board.field_by_id("Z")
    field_3 = board.field_by_id("L")
    field_4 = board.field_by_id("T")
    assert field_1 == board.fields()[0]
    assert field_2 == board.fields()[-1]
    assert field_3 == board.fields()[11]
    assert field_4 == board.fields()[18]


def test_check_is_connection_beetween_fields_nine_pawns():
    board = Board()
    field_A = board.field_by_id("A")
    field_C = board.field_by_id("C")
    field_D = board.field_by_id("D")
    field_E = board.field_by_id("E")
    field_H = board.field_by_id("H")
    field_J = board.field_by_id("J")
    field_L = board.field_by_id("L")
    field_M = board.field_by_id("M")
    field_N = board.field_by_id("N")
    field_O = board.field_by_id("O")
    field_R = board.field_by_id("R")
    field_S = board.field_by_id("S")
    field_Z = board.field_by_id("Z")
    assert board.check_is_connection_beetween_fields_nine_pawns(
        field_A, field_J)
    assert board.check_is_connection_beetween_fields_nine_pawns(
        field_J, field_A)
    assert board.check_is_connection_beetween_fields_nine_pawns(
        field_D, field_E)
    assert board.check_is_connection_beetween_fields_nine_pawns(
        field_H, field_E)
    assert board.check_is_connection_beetween_fields_nine_pawns(
        field_N, field_M)
    assert board.check_is_connection_beetween_fields_nine_pawns(
        field_O, field_C)
    assert board.check_is_connection_beetween_fields_nine_pawns(
        field_O, field_N)
    assert board.check_is_connection_beetween_fields_nine_pawns(
        field_S, field_M)
    assert board.check_is_connection_beetween_fields_nine_pawns(
        field_Z, field_O)
    assert not board.check_is_connection_beetween_fields_nine_pawns(
        field_A, field_C)
    assert not board.check_is_connection_beetween_fields_nine_pawns(
        field_A, field_Z)
    assert not board.check_is_connection_beetween_fields_nine_pawns(
        field_A, field_D)
    assert not board.check_is_connection_beetween_fields_nine_pawns(
        field_D, field_H)
    assert not board.check_is_connection_beetween_fields_nine_pawns(
        field_E, field_M)
    assert not board.check_is_connection_beetween_fields_nine_pawns(
        field_R, field_E)
    assert not board.check_is_connection_beetween_fields_nine_pawns(
        field_L, field_M)
    assert not board.check_is_connection_beetween_fields_nine_pawns(
        field_M, field_O)
    assert not board.check_is_connection_beetween_fields_nine_pawns(
        field_N, field_L)
