from pytest import raises
from source.coordinates import Coordinates
from source.enums import Position, PositionSquare


def test_constructor_exception():
    with raises(ValueError):
        Coordinates(PositionSquare.INNER, Position.RIGHT, Position.CENTER)


def test_constructor_exception_2():
    with raises(ValueError):
        Coordinates(PositionSquare.INNER, Position.TOP, Position.BOTTOM)


def test_getters():
    coordinates = Coordinates(PositionSquare.MIDDLE,
                              Position.TOP, Position.LEFT)
    assert coordinates.square() == PositionSquare.MIDDLE
    assert coordinates.position_top_middle_bottom() == Position.TOP
    assert coordinates.position_left_center_right() == Position.LEFT


def test_get_coordinates():
    coordinates = Coordinates(PositionSquare.MIDDLE,
                              Position.TOP, Position.LEFT)
    assert coordinates.get_all_coordinates() == (
        PositionSquare.MIDDLE, Position.TOP, Position.LEFT)
