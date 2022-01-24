from .enums import Position, PositionSquare


class Coordinates:
    def __init__(self, square: "PositionSquare", positionTopMiddleBottom: "Position", positionLeftCenterRight: "Position") -> None:
        self._square = square
        if positionTopMiddleBottom not in [Position.TOP, Position.MIDDLE, Position.BOTTOM]:
            raise ValueError(
                "Second position parameter sholud be TOP, MIDDLE or BOTTOM")
        self._positionTopMiddleBottom = positionTopMiddleBottom
        if positionLeftCenterRight not in [Position.LEFT, Position.CENTER, Position.RIGHT]:
            raise ValueError(
                "Third position parameter should be LEFT, CENTER or RIGHT")
        self._positionLeftCenterRight = positionLeftCenterRight

    def square(self) -> PositionSquare:
        return self._square

    def position_top_middle_bottom(self) -> Position:
        return self._positionTopMiddleBottom

    def position_left_center_right(self) -> Position:
        return self._positionLeftCenterRight

    # Chyba nigdzie nie jest używane
    def get_all_coordinates(self):
        return (self._square, self._positionTopMiddleBottom, self._positionLeftCenterRight)

    def __eq__(self, other) -> bool:
        return (self._square, self._positionTopMiddleBottom, self._positionLeftCenterRight) == (other._square, other._positionTopMiddleBottom, other._positionLeftCenterRight)
