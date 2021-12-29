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
            self.check_mill(field)

    def remove_pawn(self, field: Field):
        if field.player():
            field.set_player(None)

    """
    After pawn is moved, it is checked if mill occured
    """
    # Check if new field has connection with previous one
    # TODO check connections

    def move_pawn(self, current_field: Field, new_field: Field, player: Player):
        if new_field.player() is None and self.check_is_connection_beetween_fields_nine_pawns(current_field, new_field):
            current_field.set_player(None)
            new_field.set_player(player)
        self.check_mill(new_field)

    """
    Checks if last move created a mill
    """

    def check_mill(self, field: Field):
        if field.coordiantes().position_top_middle_bottom() == pos.MIDDLE or field.coordiantes().position_left_center_right() == pos.CENTER:
            fields_to_check = []
            for square in pos_sq:
                found_field = self.field_by_positions(square, field.coordiantes(
                ).position_top_middle_bottom(), field.coordiantes().position_left_center_right())
                fields_to_check.append(found_field)
                if all([field.player() == check_field.player() for check_field in fields_to_check]):
                    return field.player()
        if field.coordiantes().position_left_center_right() in [pos.LEFT, pos.RIGHT]:
            fields_to_check=[]
            for position in [pos.TOP, pos.MIDDLE, pos.BOTTOM]:
                found_field=self.field_by_positions(field.coordiantes().square(
                ), position, field.coordiantes().position_left_center_right())
                fields_to_check.append(found_field)
                if all([field.player() == check_field.player() for check_field in fields_to_check]):
                    return field.player()
        if field.coordiantes().position_top_middle_bottom() in [pos.TOP, pos.BOTTOM]:
            fields_to_check=[]
            for position in [pos.LEFT, pos.CENTER, pos.RIGHT]:
                found_field=self.field_by_positions(field.coordiantes().square(
                ), field.coordiantes().position_top_middle_bottom(), position)
                fields_to_check.append(found_field)
                if all([field.player() == check_field.player() for check_field in fields_to_check]):
                    return field.player()

    def field_by_positions(self, positionSquare: pos_sq, positionTMB: pos, positionLCR: pos) -> Field:
        for field in self._fields:
            if field.coordiantes().get_all_coordinates() == (positionSquare, positionTMB, positionLCR):
                return field

    def player_pawns_number(self, player) -> int:
        player_pawns_no=0
        for field in self._fields:
            if field.player() == player:
                player_pawns_no += 1
        return player_pawns_no

    def field_by_id(self, id) -> Field:
        for field in self._fields:
            if field.id() == id:
                return field

    def check_is_connection_beetween_fields_nine_pawns(self, current_field: Field, new_field: Field) -> bool:
        current_position_tmb=current_field.coordiantes().position_top_middle_bottom()
        current_position_lcr=current_field.coordiantes().position_left_center_right()
        current_position_square=current_field.coordiantes().square()
        new_position_tmb=new_field.coordiantes().position_top_middle_bottom()
        new_position_lcr=new_field.coordiantes().position_left_center_right()
        new_position_square=new_field.coordiantes().square()

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
        fields_list=[]
        id_index=0
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
