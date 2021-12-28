from typing import List

from .enums import Player
from .coordinates import Coordinates
from . import pawn


class Field:
    def __init__(self, id, coordinates: "Coordinates",
                 #  connections: List["Field"] = None,
                 player: Player = None) -> None:
        self._id = id
        self._coordiantes = coordinates
        # self._connections = connections
        self._player = player

    def id(self):
        return self._id

    def coordiantes(self):
        return self._coordiantes

    # def connections(self):
    #     return self._connections

    def player(self):
        return self._player

    # def set_connections(self, connections: List["Field"]):
    #     self._connections = connections

    def set_player(self, player: Player):
        self._player = player
