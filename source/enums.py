from enum import Enum


class BoardSize(Enum):
    NINE = 9
    THREE = 3
    SIX = 6
    TWELVE = 12


class ConnectionDirection(Enum):
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3


class PositionSquare(Enum):
    OUTER = 1
    MIDDLE = 2
    INNER = 3


class Position(Enum):
    TOP = 1
    MIDDLE = 2
    BOTTOM = 3
    LEFT = 4
    CENTER = 5
    RIGHT = 6
