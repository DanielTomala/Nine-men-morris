from . import field
from .enums import Player


class Pawn:

    def __init__(self, currentField: "field.Field" = None, player: "Player" = None) -> None:
        self._currentField = currentField
        self._player = player

    def current_field(self):
        return self._currentField

    def player(self):
        return self._player

    def set_current_field(self, field: "field.Field"):
        self._currentField = field

    def set_player(self, player):
        self._player = player
