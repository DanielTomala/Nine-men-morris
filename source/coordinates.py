from source.enums import Position, PositionSquare


class Coordinates:
    def __init__(self, square: "PositionSquare", positionTopMiddleBottom: "Position", positionLeftCenterRight: "Position") -> None:
        self._square = square
        self._positionTopMiddleBottom = positionTopMiddleBottom
        self._positionLeftCenterRight = positionLeftCenterRight

    def square(self):
        return self._square

    def position_top_middle_bottom(self):
        return self._positionTopMiddleBottom

    def position_left_center_right(self):
        return self.position_left_center_right
