from .enums import Position, PositionSquare


class Coordinates:
    def __init__(self, square: "PositionSquare", positionTopMiddleBottom: "Position", positionLeftCenterRight: "Position") -> None:
        self._square = square
        if not positionTopMiddleBottom in [Position.TOP, Position.MIDDLE, Position.BOTTOM]:
            raise ValueError(
                "Second position parameter sholud be TOP, MIDDLE or BOTTOM")
        self._positionTopMiddleBottom = positionTopMiddleBottom
        if not positionLeftCenterRight in [Position.LEFT, Position.CENTER, Position.RIGHT]:
            raise ValueError(
                "Third position parameter should be LEFT, CENTER or RIGHT")
        self._positionLeftCenterRight = positionLeftCenterRight

    def square(self):
        return self._square

    def position_top_middle_bottom(self):
        return self._positionTopMiddleBottom

    def position_left_center_right(self):
        return self._positionLeftCenterRight

    def get_all_coordinates(self):
        return (self._square, self._positionTopMiddleBottom, self._positionLeftCenterRight)
