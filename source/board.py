from typing import List
from .coordinates import Coordinates
from .enums import PawnsNumber, Player, Position as pos, PositionSquare as pos_sq
from .field import Field

FIELD_IDS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
             "L", "M", "N", "O", "P", "R", "S", "T", "U", "W", "X", "Y", "Z"]


class Board:
    def __init__(self, pawns_number: PawnsNumber = PawnsNumber.NINE) -> None:
        self._fields = self._create_nine_pawns_board()
        self._pawns_number = pawns_number

    def fields(self):
        return self._fields

    def pawns_number(self):
        return self._pawns_number

    """
    After pawn is added, it is checked if mill occured
    """

    def add_pawn(self, field: Field, player: Player):
        if field.player() is None:
            field.set_player(player)
        self.check_mill()

    def remove_pawn(self, field: Field):
        if field.player():
            field.set_player(None)

    """
    Checks if last move created a mill
    """

    def check_mill(self):
        pass

    """
    After pawn is moved, it is checked if mill occured
    """
    # Check if new field has connection with previous one
    # TODO check connections

    def move_pawn(self, current_field: Field, new_field: Field, player: Player):
        if new_field.player() is None and self.check_is_connection_beetween_fields_nine_pawns(current_field, new_field):
            current_field.set_player(None)
            new_field.set_player(player)
        self.check_mill()

    def find_field_with_given_positions(self, positionSquare: pos_sq, positionTMB: pos, positionLCR: pos) -> Field:
        for field in self._fields:
            if field.coordiantes().get_all_coordinates() == (positionSquare, positionTMB, positionLCR):
                return field

    def player_pawns_number(self, player):
        player_pawns_no = 0
        for field in self._fields:
            if field.player() == player:
                player_pawns_no += 1
        return player_pawns_no

    def get_field_by_id(self, id) -> Field:
        for field in self._fields:
            if field.id() == id:
                return field

    def check_is_connection_beetween_fields_nine_pawns(self, current_field: Field, new_field: Field) -> bool:
        current_position_tmb = current_field.coordiantes().position_top_middle_bottom()
        current_position_lcr = current_field.coordiantes().position_left_center_right()
        current_position_square = current_field.coordiantes().square()
        new_position_tmb = new_field.coordiantes().position_top_middle_bottom()
        new_position_lcr = new_field.coordiantes().position_left_center_right()
        new_position_square = new_field.coordiantes().square()

        if current_position_square == new_position_square:
            if current_position_tmb == new_position_tmb:
                if new_position_lcr.value in [current_position_lcr.value + 1, current_position_lcr.value - 1]:
                    return True

            elif current_position_lcr == new_position_lcr:
                if new_position_tmb.value in [current_position_tmb.value + 1, current_position_tmb.value - 1]:
                    return True
        else:
            if (current_position_lcr == pos.CENTER and new_position_lcr == pos.CENTER):
                if current_position_tmb == new_position_tmb:
                    if new_position_square.value in [current_position_square.value + 1, current_position_square.value - 1]:
                        return True
            elif (current_position_tmb == pos.MIDDLE and current_position_tmb == pos.MIDDLE):
                if current_position_lcr == new_position_lcr:
                    if new_position_square.value in [current_position_square.value + 1, current_position_square.value - 1]:
                        return True

        return False

    def _create_nine_pawns_board(self) -> List[Field]:
        fields_list = []
        id_index = 0
        for square in pos_sq:
            for position_lcr in [pos.LEFT, pos.CENTER, pos.RIGHT]:
                fields_list.append(Field(FIELD_IDS[id_index], Coordinates(
                    square, pos.TOP, position_lcr)))
                id_index += 1
        for square in pos_sq:
            fields_list.append(Field(FIELD_IDS[id_index], Coordinates(
                square, pos.MIDDLE, pos.LEFT)))
            id_index += 1
        for square in reversed(pos_sq):
            fields_list.append(Field(FIELD_IDS[id_index], Coordinates(
                square, pos.MIDDLE, pos.RIGHT)))
            id_index += 1
        for square in reversed(pos_sq):
            for position_lcr in [pos.LEFT, pos.CENTER, pos.RIGHT]:
                fields_list.append(Field(FIELD_IDS[id_index], Coordinates(
                    square, pos.BOTTOM, position_lcr)))
                id_index += 1
        return fields_list

    # def _test_map_generator(self):
    #     A = Field("A", Coordinates(pos_sq.INNER, pos.TOP, pos.LEFT))
    #     B = Field("B", Coordinates(pos_sq.INNER, pos.TOP, pos.CENTER))
    #     C = Field("C", Coordinates(pos_sq.INNER, pos.TOP, pos.RIGHT))
    #     D = Field("D", Coordinates(pos_sq.INNER, pos.MIDDLE, pos.LEFT))
    #     E = Field("E", Coordinates(pos_sq.INNER, pos.MIDDLE, pos.RIGHT))
    #     F = Field("F", Coordinates(pos_sq.INNER, pos.BOTTOM, pos.LEFT))
    #     G = Field("G", Coordinates(pos_sq.INNER, pos.BOTTOM, pos.CENTER))
    #     H = Field("H", Coordinates(pos_sq.INNER, pos.BOTTOM, pos.RIGHT))

    #     A.set_connections([B, D])
    #     B.set_connections([A, C])
    #     C.set_connections([B, E])
    #     D.set_connections([A, F])
    #     E.set_connections([C, H])
    #     F.set_connections([D, G])
    #     G.set_connections([F, H])
    #     H.set_connections([G, E])

    #     return [A, B, C, D, E, F, G, H]
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
        # |    D---------E---------F    |
        # |    |         |         |    |
        # |    |    G----H----I    |    |
        # |    |    |         |    |    |
        # J----K----L         M----N----O
        # |    |    |         |    |    |
        # |    |    P----R----S    |    |
        # |    |         |         |    |
        # |    T---------U---------W    |
        # |              |              |
        # X--------------Y--------------Z
