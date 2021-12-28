from typing import List

from .enums import Player
from .coordinates import Coordinates
from . import pawn


class Field:
    def __init__(self, id, coordinates: "Coordinates",
                 connections: List["Field"] = None,
                 # isOccupied: bool = False,
                 # currentPawn: "pawn.Pawn" = None,
                 player: Player = None) -> None:
        self._id = id
        self._coordiantes = coordinates
        self._connections = connections
        # self._isOccupied = isOccupied
        # self._currentPawn = currentPawn
        self._player = player

    def id(self):
        return self._id

    def coordiantes(self):
        return self._coordiantes

    def connections(self):
        return self._connections

    # def isOccupied(self):
    #     return self._isOccupied

    # def currentPawn(self):
    #     return self._currentPawn

    def player(self):
        return self._player

    def set_connections(self, connections: List["Field"]):
        self._connections = connections

    def set_player(self, player: Player):
        self._player = player

    # def set_is_occupied(self, isOccupied: bool):
    #     self._isOccupied = isOccupied

    # def set_current_pawn(self, pawn):
    #     self._currentPawn = pawn
