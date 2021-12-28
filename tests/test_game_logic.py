import random
from ..source.enums import Player
from ..source.game_logic import get_starting_player


def test_get_starting_player(monkeypatch):
    def mock_randint(s, e):
        return 1
    monkeypatch.setattr(random, "randint", mock_randint)
    player = get_starting_player()
    assert player == Player.FIRST
