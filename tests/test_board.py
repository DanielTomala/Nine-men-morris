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


def test_field_by_positions():
    board = Board()
    field = board.field_by_positions(
        PositionSquare.OUTER, Position.TOP, Position.LEFT)
    assert field == board.fields()[0]


def test_create_nine_pawns_board():
    board = Board()
    board_fields = board._create_nine_twelve_pawns_board()
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


def test_is_field_free():
    board = Board()
    field_A = board.field_by_id("A")
    field_A.set_player(Player.FIRST)
    field_R = board.field_by_id("R")
    field_R.set_player(Player.SECOND)
    assert not board.is_field_free(field_A)
    assert not board.is_field_free(field_R)
    assert board.is_field_free(board.field_by_id("B"))
    assert board.is_field_free(board.field_by_id("Z"))
    assert board.is_field_free(board.field_by_id("T"))

    board.remove_pawn(field_A)
    board.remove_pawn(field_R)
    assert board.is_field_free(field_A)
    assert board.is_field_free(field_R)


def test_get_all_player_fields():
    board = Board()
    assert board.get_all_player_fields(Player.FIRST) == []
    assert board.get_all_player_fields(Player.SECOND) == []
    field_A = board.field_by_id("A")
    field_A.set_player(Player.FIRST)
    field_B = board.field_by_id("B")
    field_B.set_player(Player.FIRST)
    field_J = board.field_by_id("J")
    field_J.set_player(Player.FIRST)
    field_P = board.field_by_id("P")
    field_P.set_player(Player.FIRST)
    field_R = board.field_by_id("R")
    field_R.set_player(Player.FIRST)
    field_Y = board.field_by_id("Y")
    field_Y.set_player(Player.FIRST)

    assert board.get_all_player_fields(Player.FIRST) == [
        field_A, field_B, field_J, field_P, field_R, field_Y]

    field_C = board.field_by_id("C")
    field_C.set_player(Player.SECOND)
    field_D = board.field_by_id("D")
    field_D.set_player(Player.SECOND)
    field_U = board.field_by_id("U")
    field_U.set_player(Player.SECOND)
    field_Z = board.field_by_id("Z")
    field_Z.set_player(Player.SECOND)

    assert board.get_all_player_fields(Player.SECOND) == [
        field_C, field_D, field_U, field_Z]


def test_get_all_free_fields():
    pass