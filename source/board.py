from typing import List

from source.point import Point


class Board:
    def __init__(self, points: List[Point]) -> None:
        pass

    """
    After pawn is added, it is checked if mill occured
    """
    def add_pawn():
        pass

    def remove_pawn():
        pass

    """
    Checks if last move created a mill
    """
    def check_mill():
        pass

    """
    After pawn is moved, it is checked if mill occured
    """
    def move_pawn():
        pass
# o--------------o--------------o 
# |              |              |
# |    o---------o---------o    |
# |    |         |         |    |
# |    |    o----o----o    |    |
# |    |    |         |    |    |
# o----o----o         o----o----o
# |    |    |         |    |    |
# |    |    o----o----o    |    |
# |    |         |         |    |
# |    o---------o---------o    |
# |              |              |
# o--------------o--------------o

# A--------------B--------------C
# |              |              |
# |    I---------J---------K    |
# |    |         |         |    |
# |    |    R----S----T    |    |
# |    |    |         |    |    |
# D----L----U         W----M----E
# |    |    |         |    |    |
# |    |    X----Y----Z    |    |
# |    |         |         |    |
# |    N---------O---------P    |
# |              |              |
# F--------------G--------------H
