from typing import List
from source.coordinates import Coordinates
from source.pawn import Pawn
from source.point import Point


class Point:
    def __init__(self, coordinates: Coordinates, connections: List[Point], isOccupied: bool = False, currentPawn: Pawn = None) -> None:
        pass
