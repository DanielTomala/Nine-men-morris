from typing import List
from source.coordinates import Coordinates
import source.pawn



class Field:
    def __init__(self, coordinates: "Coordinates", connections: List["Field"] = None, isOccupied: bool = False, currentPawn: source.pawn.Pawn = None) -> None:
        self._coordiantes = coordinates
        self._connections = connections
        self._isOccupied = isOccupied
        self._currentPawn = currentPawn

    def coordiantes(self):
        return self._coordiantes

    def connections(self):
        return self._connections

    def isOccupied(self):
        return self._isOccupied

    def currentPawn(self):
        return self._currentPawn

    def set_connections(self, connections: List["Field"]):
        self._connections = connections

    def set_is_occupied(self, isOccupied: bool):
        self._isOccupied = isOccupied

    def set_current_pawn(self, pawn):
        self._currentPawn = pawn
