from enum import Enum


class PawnsNumber(Enum):
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
    LEFT = 11
    CENTER = 12
    RIGHT = 13


class Player(Enum):
    FIRST = 1
    SECOND = 2
