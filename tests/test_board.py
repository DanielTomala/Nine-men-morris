from source.board import Board
from source.pawn import Pawn


def test_add_pawn():
    board = Board()
    pawn = Pawn()
    field = board.fields()[0]
    board.add_pawn(field, pawn)
    assert field.currentPawn() == pawn
    assert field.isOccupied()
    assert pawn.current_field() == field


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
