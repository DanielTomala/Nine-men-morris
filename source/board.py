from typing import List
from .coordinates import Coordinates
from .enums import BoardSize, Position, PositionSquare
from .field import Field
from .pawn import Pawn


class Board:
    def __init__(self, size: BoardSize = BoardSize.NINE) -> None:
        self._fields = self.test_map_generator()
        self._size = size

    def fields(self):
        return self._fields

    def size(self):
        return self._size

    """
    After pawn is added, it is checked if mill occured
    """

    def add_pawn(self, field: Field, pawn: Pawn):
        if not field.currentPawn():
            field.set_current_pawn(pawn)
            field.set_is_occupied(True)
            pawn.set_current_field(field)
        self.check_mill()

    def remove_pawn(self, field: Field):
        if field.currentPawn():
            field.set_current_pawn(None)
            field.set_is_occupied(False)

    """
    Checks if last move created a mill
    """

    def check_mill(self):
        pass

    """
    After pawn is moved, it is checked if mill occured
    """
    # Check if new field has connection with previous one

    def move_pawn(self, newField: Field, pawn: Pawn):
        if not newField.isOccupied() and newField in pawn.current_field().connections():
            pawn.current_field().set_is_occupied(False)
            pawn.current_field().set_current_pawn(None)
            pawn.set_current_field(newField)
            newField.set_current_pawn(pawn)
            newField.set_is_occupied(True)
        self.check_mill()

    def find_field_with_given_positions(self, positionSquare: PositionSquare, positionTMB: Position, positionLCR: Position) -> Field:
        for field in self._fields:
            if field.coordiantes().get_coordinates() == (positionSquare, positionTMB, positionLCR):
                return field

    def create_nine_pawns_board() -> List[Field]:
        pass

    def test_map_generator(self):
        A = Field(Coordinates(PositionSquare.INNER,
                              Position.TOP, Position.LEFT))
        B = Field(Coordinates(PositionSquare.INNER,
                              Position.TOP, Position.CENTER))
        C = Field(Coordinates(PositionSquare.INNER,
                              Position.TOP, Position.RIGHT))
        D = Field(Coordinates(PositionSquare.INNER,
                              Position.MIDDLE, Position.LEFT))
        E = Field(Coordinates(PositionSquare.INNER,
                              Position.MIDDLE, Position.RIGHT))
        F = Field(Coordinates(PositionSquare.INNER,
                              Position.BOTTOM, Position.LEFT))
        G = Field(Coordinates(PositionSquare.INNER,
                              Position.BOTTOM, Position.CENTER))
        H = Field(Coordinates(PositionSquare.INNER,
                              Position.BOTTOM, Position.RIGHT))

        A.set_connections([B, D])
        B.set_connections([A, C])
        C.set_connections([B, E])
        D.set_connections([A, F])
        E.set_connections([C, H])
        F.set_connections([D, G])
        G.set_connections([F, H])
        H.set_connections([G, E])

        return [A, B, C, D, E, F, G, H]
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
