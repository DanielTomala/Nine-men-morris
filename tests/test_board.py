from source.board import FIELD_IDS, Board
from source.coordinates import Coordinates
from source.enums import PawnsNumber, Player, Position, PositionSquare


def test_add_pawn():
    board = Board()
    field = board.fields()[0]
    board.add_pawn(field, Player.ONE)
    assert field.player() == Player.ONE


def test_add_pawn_field_already_occupied():
    board = Board()
    field = board.fields()[0]
    board.add_pawn(field, Player.ONE)
    board.add_pawn(field, Player.TWO)
    assert field.player() == Player.ONE


def test_remove_pawn():
    board = Board()
    field = board.fields()[0]
    board.add_pawn(field, Player.ONE)
    assert field.player() == Player.ONE
    board.remove_pawn(field)
    assert field.player() is None


def test_move_pawn():
    board = Board()
    field_1 = board.fields()[0]
    field_2 = board.fields()[1]
    board.add_pawn(field_1, Player.ONE)
    assert field_1.player() == Player.ONE
    board.move_pawn(field_1, field_2, Player.ONE)
    assert field_1.player() is None
    assert field_2.player() == Player.ONE


def test_move_pawn_field_occupied():
    board = Board()
    field_1 = board.fields()[0]
    field_2 = board.fields()[1]
    board.add_pawn(field_1, Player.ONE)
    board.add_pawn(field_2, Player.TWO)
    assert field_1.player() == Player.ONE
    assert field_2.player() == Player.TWO
    board.move_pawn(field_1, field_2, Player.ONE)
    assert field_1.player() == Player.ONE
    assert field_2.player() == Player.TWO


def test_move_pawn_no_connection():
    board = Board()
    field_1 = board.fields()[0]
    field_2 = board.fields()[2]
    board.add_pawn(field_1, Player.ONE)
    assert field_1.player() == Player.ONE
    board.move_pawn(field_1, field_2, Player.ONE)
    assert field_1.player() == Player.ONE


def test_is_field_free():
    board = Board()
    field_A = board.field_by_id("A")
    field_A.set_player(Player.ONE)
    field_R = board.field_by_id("R")
    field_R.set_player(Player.TWO)
    assert not board.is_field_free(field_A)
    assert not board.is_field_free(field_R)
    assert board.is_field_free(board.field_by_id("B"))
    assert board.is_field_free(board.field_by_id("Z"))
    assert board.is_field_free(board.field_by_id("T"))

    board.remove_pawn(field_A)
    board.remove_pawn(field_R)
    assert board.is_field_free(field_A)
    assert board.is_field_free(field_R)


def test_field_by_coordinates():
    board = Board()
    coord = Coordinates(PositionSquare.OUTER, Position.TOP, Position.LEFT)
    field = board.field_by_coordinates(coord)
    assert field == board.fields()[0]


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


def test_players_pawns_number():
    board = Board()
    field_1 = board.fields()[0]
    field_2 = board.fields()[1]
    field_3 = board.fields()[5]
    field_1.set_player(Player.ONE)
    field_2.set_player(Player.TWO)
    field_3.set_player(Player.ONE)
    assert board.player_pawns_number(Player.ONE) == 2
    assert board.player_pawns_number(Player.TWO) == 1


def test_all_player_fields():
    board = Board()
    assert board.all_player_fields(Player.ONE) == []
    assert board.all_player_fields(Player.TWO) == []
    field_A = board.field_by_id("A")
    field_A.set_player(Player.ONE)
    field_B = board.field_by_id("B")
    field_B.set_player(Player.ONE)
    field_J = board.field_by_id("J")
    field_J.set_player(Player.ONE)
    field_P = board.field_by_id("P")
    field_P.set_player(Player.ONE)
    field_R = board.field_by_id("R")
    field_R.set_player(Player.ONE)
    field_Y = board.field_by_id("Y")
    field_Y.set_player(Player.ONE)

    assert board.all_player_fields(Player.ONE) == [
        field_A, field_B, field_J, field_P, field_R, field_Y]

    field_C = board.field_by_id("C")
    field_C.set_player(Player.TWO)
    field_D = board.field_by_id("D")
    field_D.set_player(Player.TWO)
    field_U = board.field_by_id("U")
    field_U.set_player(Player.TWO)
    field_Z = board.field_by_id("Z")
    field_Z.set_player(Player.TWO)

    assert board.all_player_fields(Player.TWO) == [
        field_C, field_D, field_U, field_Z]


def test_all_free_fields():
    board = Board(PawnsNumber.SIX)
    for id in ["A", "B", "C", "E", "F", "I", "J", "K", "M", "N", "P"]:
        field = board.field_by_id(id)
        field.set_player(Player.ONE)

    field_D = board.field_by_id("D")
    field_G = board.field_by_id("G")
    field_H = board.field_by_id("H")
    field_L = board.field_by_id("L")
    field_O = board.field_by_id("O")

    assert board.all_free_fields() == [
        field_D, field_G, field_H, field_L, field_O]


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

    assert board.possible_moves(field_A) == []
    assert board.possible_moves(field_B) == ["C", "E"]
    assert not board.possible_moves(field_B) == ["E", "C"]
    assert board.possible_moves(field_J) == []
    assert board.possible_moves(field_K) == ["D", "L", "T"]
    assert board.possible_moves(field_N) == ["F", "M", "O", "W"]
    assert board.possible_moves(field_R) == ["P", "S", "U"]
    assert board.possible_moves(field_X) == ["Y"]


def test_create_three_pawns_board():
    board = Board(PawnsNumber.THREE)
    board_fields = board._create_fields_three_pawns()

    assert board_fields[0].id() == FIELD_IDS[0]
    assert board_fields[0].coordinates().square() == PositionSquare.MIDDLE
    assert board_fields[0].coordinates(
    ).position_top_middle_bottom() == Position.TOP
    assert board_fields[0].coordinates(
    ).position_left_center_right() == Position.LEFT

    assert board_fields[4].id() == FIELD_IDS[4]
    assert board_fields[4].coordinates().square() == PositionSquare.MIDDLE
    assert board_fields[4].coordinates(
    ).position_top_middle_bottom() == Position.MIDDLE
    assert board_fields[4].coordinates(
    ).position_left_center_right() == Position.CENTER

    assert board_fields[7].id() == FIELD_IDS[7]
    assert board_fields[7].coordinates().square() == PositionSquare.MIDDLE
    assert board_fields[7].coordinates(
    ).position_top_middle_bottom() == Position.BOTTOM
    assert board_fields[7].coordinates(
    ).position_left_center_right() == Position.CENTER


def test_create_six_pawns_board():
    board = Board(PawnsNumber.SIX)
    board_fields = board._create_fields_six_pawns()

    assert board_fields[0].id() == FIELD_IDS[0]
    assert board_fields[0].coordinates().square() == PositionSquare.OUTER
    assert board_fields[0].coordinates(
    ).position_top_middle_bottom() == Position.TOP
    assert board_fields[0].coordinates(
    ).position_left_center_right() == Position.LEFT

    assert board_fields[4].id() == FIELD_IDS[4]
    assert board_fields[4].coordinates().square() == PositionSquare.INNER
    assert board_fields[4].coordinates(
    ).position_top_middle_bottom() == Position.TOP
    assert board_fields[4].coordinates(
    ).position_left_center_right() == Position.CENTER

    assert board_fields[12].id() == FIELD_IDS[12]
    assert board_fields[12].coordinates().square() == PositionSquare.INNER
    assert board_fields[12].coordinates(
    ).position_top_middle_bottom() == Position.BOTTOM
    assert board_fields[12].coordinates(
    ).position_left_center_right() == Position.RIGHT


def test_create_nine_or_twelve_pawns_board():
    board = Board()
    board_fields = board._create_fields_nine_or_twelve_pawns()
    assert board_fields[0].id() == FIELD_IDS[0]
    assert board_fields[0].coordinates().square() == PositionSquare.OUTER
    assert board_fields[0].coordinates(
    ).position_top_middle_bottom() == Position.TOP
    assert board_fields[0].coordinates(
    ).position_left_center_right() == Position.LEFT

    assert board_fields[5].id() == FIELD_IDS[5]
    assert board_fields[5].coordinates().square() == PositionSquare.MIDDLE
    assert board_fields[5].coordinates(
    ).position_top_middle_bottom() == Position.TOP
    assert board_fields[5].coordinates(
    ).position_left_center_right() == Position.RIGHT

    assert board_fields[11].id() == FIELD_IDS[11]
    assert board_fields[11].coordinates().square() == PositionSquare.INNER
    assert board_fields[11].coordinates(
    ).position_top_middle_bottom() == Position.MIDDLE
    assert board_fields[11].coordinates(
    ).position_left_center_right() == Position.LEFT

    assert board_fields[12].id() == FIELD_IDS[12]
    assert board_fields[12].coordinates().square() == PositionSquare.INNER
    assert board_fields[12].coordinates(
    ).position_top_middle_bottom() == Position.MIDDLE
    assert board_fields[12].coordinates(
    ).position_left_center_right() == Position.RIGHT

    assert board_fields[18].id() == FIELD_IDS[18]
    assert board_fields[18].coordinates().square() == PositionSquare.MIDDLE
    assert board_fields[18].coordinates(
    ).position_top_middle_bottom() == Position.BOTTOM
    assert board_fields[18].coordinates(
    ).position_left_center_right() == Position.LEFT


def test_set_connections_three_pawns():
    board = Board(PawnsNumber.THREE)

    field_A = board.field_by_id("A")
    assert field_A.connections() == ["B", "D", "E"]

    field_E = board.field_by_id("E")
    assert field_E.connections() == ["A", "B", "C", "D", "F", "G", "H", "I"]

    field_G = board.field_by_id("G")
    assert field_G.connections() == ["D", "E", "H"]


def test_set_connections_six_pawns():
    board = Board(PawnsNumber.SIX)

    field_C = board.field_by_id("C")
    assert field_C.connections() == ["B", "J"]

    field_I = board.field_by_id("I")
    assert field_I.connections() == ["F", "J", "M"]

    field_P = board.field_by_id("P")
    assert field_P.connections() == ["J", "O"]


def test_set_connections_nine_pawns():
    board = Board(PawnsNumber.NINE)

    field_A = board.field_by_id("A")
    assert field_A.connections() == ["B", "J"]

    field_E = board.field_by_id("E")
    assert field_E.connections() == ["B", "D", "F", "H"]

    field_R = board.field_by_id("R")
    assert field_R.connections() == ["P", "S", "U"]


def test_set_connections_twelve_pawns():
    board = Board(PawnsNumber.TWELVE)

    field_G = board.field_by_id("G")
    assert field_G.connections() == ["D", "H", "L"]

    field_M = board.field_by_id("M")
    assert field_M.connections() == ["I", "N", "S"]

    field_U = board.field_by_id("U")
    assert field_U.connections() == ["R", "T", "W", "Y"]
