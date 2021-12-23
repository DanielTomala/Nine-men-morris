from ..source.enums import Player, Position, PositionSquare
from ..source.board import Board


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


def test_find_field_with_given_positions():
    board = Board()
    field = board.find_field_with_given_positions(
        PositionSquare.INNER, Position.TOP, Position.LEFT)
    assert field == board.fields()[0]
