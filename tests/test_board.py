from ..source.pawn import Pawn
from ..source.enums import Position, PositionSquare
from ..source.board import Board


def test_add_pawn():
    board = Board()
    pawn = Pawn()
    field = board.fields()[0]
    board.add_pawn(field, pawn)
    assert field.currentPawn() == pawn
    assert field.isOccupied()
    assert pawn.current_field() == field


def test_add_pawn_occupied():
    board = Board()
    pawn = Pawn()
    pawn1 = Pawn()
    field = board.fields()[0]
    board.add_pawn(field, pawn1)
    board.add_pawn(field, pawn)
    assert field.currentPawn() == pawn1
    assert field.isOccupied()
    assert pawn.current_field() == None
    assert pawn1.current_field() == field


def test_remove_pawn():
    board = Board()
    pawn = Pawn()
    field = board.fields()[0]
    board.add_pawn(field, pawn)
    assert field.currentPawn() == pawn
    board.remove_pawn(field)
    assert field.currentPawn() == None
    assert not field.isOccupied()


def test_move_pawn():
    board = Board()
    pawn = Pawn()
    field1 = board.fields()[0]
    field2 = board.fields()[1]
    board.add_pawn(field1, pawn)
    assert field1.currentPawn() == pawn
    board.move_pawn(field2, pawn)
    assert field1.currentPawn() == None
    assert not field1.isOccupied()
    assert field2.currentPawn() == pawn
    assert field2.isOccupied()


def test_move_pawn_field_occupied():
    board = Board()
    pawn1 = Pawn()
    pawn2 = Pawn()
    field1 = board.fields()[0]
    field2 = board.fields()[1]
    board.add_pawn(field1, pawn1)
    board.add_pawn(field2, pawn2)
    assert field1.currentPawn() == pawn1
    assert field2.currentPawn() == pawn2
    board.move_pawn(field2, pawn1)
    assert field1.currentPawn() == pawn1
    assert field2.currentPawn() == pawn2


def test_move_pawn_no_connection():
    board = Board()
    pawn = Pawn()
    field1 = board.fields()[0]
    field2 = board.fields()[2]
    board.add_pawn(field1, pawn)
    assert field1.currentPawn() == pawn
    board.move_pawn(field2, pawn)
    assert field1.currentPawn() == pawn


def test_find_field_with_given_positions():
    board = Board()
    field = board.find_field_with_given_positions(
        PositionSquare.INNER, Position.TOP, Position.LEFT)
    assert field == board.fields()[0]
