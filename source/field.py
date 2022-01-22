from typing import List
from .enums import Player
from .coordinates import Coordinates


class Field:
    def __init__(self, id, coordinates: "Coordinates",
                 player: Player = None) -> None:
        self._id = id
        self._coordiantes = coordinates
        self._player = player
        self._connections = None

    def id(self):
        return self._id

    def coordiantes(self):
        return self._coordiantes

    def player(self):
        return self._player

    def set_player(self, player: Player):
        self._player = player

    def connections(self):
        return self._connections

    def set_connections(self, fields_ids: List[str]):
        self._connections = fields_ids
