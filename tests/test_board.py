from ..source.enums import Player, Position, PositionSquare
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
    field1 = board.fields()[0]
    field2 = board.fields()[1]
    board.add_pawn(field1, Player.FIRST)
    assert field1.player() == Player.FIRST
    board.move_pawn(field1, field2, Player.FIRST)
    assert field1.player() is None
    assert field2.player() == Player.FIRST


def test_move_pawn_field_occupied():
    board = Board()
    field1 = board.fields()[0]
    field2 = board.fields()[1]
    board.add_pawn(field1, Player.FIRST)
    board.add_pawn(field2, Player.SECOND)
    assert field1.player() == Player.FIRST
    assert field2.player() == Player.SECOND
    board.move_pawn(field1, field2, Player.FIRST)
    assert field1.player() == Player.FIRST
    assert field2.player() == Player.SECOND


def test_move_pawn_no_connection():
    board = Board()
    field1 = board.fields()[0]
    field2 = board.fields()[2]
    board.add_pawn(field1, Player.FIRST)
    assert field1.player() == Player.FIRST
    board.move_pawn(field1, field2, Player.FIRST)
    assert field1.player() == Player.FIRST


def test_players_pawns_number():
    board = Board()
    field1 = board.fields()[0]
    field2 = board.fields()[1]
    field3 = board.fields()[5]
    field1.set_player(Player.FIRST)
    field2.set_player(Player.SECOND)
    field3.set_player(Player.FIRST)
    assert board.players_pawns_number() == (2, 1)


def test_find_field_with_given_positions():
    board = Board()
    field = board.find_field_with_given_positions(
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


def test_get_field_by_id():
    board = Board()
    field1 = board.get_field_by_id("A")
    field2 = board.get_field_by_id("Z")
    field3 = board.get_field_by_id("L")
    field4 = board.get_field_by_id("T")
    assert field1 == board.fields()[0]
    assert field2 == board.fields()[-1]
    assert field3 == board.fields()[11]
    assert field4 == board.fields()[18]


def test_check_is_connection_beetween_fields_nine_pawns():
    board = Board()
    field_A = board.get_field_by_id("A")
    field_C = board.get_field_by_id("C")
    field_D = board.get_field_by_id("D")
    field_E = board.get_field_by_id("E")
    field_H = board.get_field_by_id("H")
    field_J = board.get_field_by_id("J")
    field_L = board.get_field_by_id("L")
    field_M = board.get_field_by_id("M")
    field_N = board.get_field_by_id("N")
    field_O = board.get_field_by_id("O")
    field_R = board.get_field_by_id("R")
    field_S = board.get_field_by_id("S")
    field_Z = board.get_field_by_id("Z")
    assert board.check_is_connection_beetween_fields_nine_pawns(field_A, field_J)
    assert board.check_is_connection_beetween_fields_nine_pawns(field_J, field_A)
    assert board.check_is_connection_beetween_fields_nine_pawns(field_D, field_E)
    assert board.check_is_connection_beetween_fields_nine_pawns(field_H, field_E)
    assert board.check_is_connection_beetween_fields_nine_pawns(field_N, field_M)
    assert board.check_is_connection_beetween_fields_nine_pawns(field_O, field_C)
    assert board.check_is_connection_beetween_fields_nine_pawns(field_O, field_N)
    assert board.check_is_connection_beetween_fields_nine_pawns(field_S, field_M)
    assert board.check_is_connection_beetween_fields_nine_pawns(field_Z, field_O)
    assert not board.check_is_connection_beetween_fields_nine_pawns(field_A, field_C)
    assert not board.check_is_connection_beetween_fields_nine_pawns(field_A, field_Z)
    assert not board.check_is_connection_beetween_fields_nine_pawns(field_A, field_D)
    assert not board.check_is_connection_beetween_fields_nine_pawns(field_D, field_H)
    assert not board.check_is_connection_beetween_fields_nine_pawns(field_E, field_M)
    assert not board.check_is_connection_beetween_fields_nine_pawns(field_R, field_E)
    assert not board.check_is_connection_beetween_fields_nine_pawns(field_L, field_M)
    assert not board.check_is_connection_beetween_fields_nine_pawns(field_M, field_O)
    assert not board.check_is_connection_beetween_fields_nine_pawns(field_N, field_L)
