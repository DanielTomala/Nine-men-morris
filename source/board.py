from typing import List

from .consts import (CONNECTIONS_NINE, CONNECTIONS_SIX, CONNECTIONS_THREE,
                     CONNECTIONS_TWELVE, FIELD_IDS, POS_LCR_LIST,
                     POS_SQ_OI_LIST, POS_TMB_LIST)
from .coordinates import Coordinates
from .enums import BotLvl, PawnsNumber, Player
from .enums import Position as pos
from .enums import PositionSquare as pos_sq
from .field import Field


class Board:
    def __init__(self, pawns_number: PawnsNumber = PawnsNumber.NINE, bot: BotLvl = BotLvl.OFF, delay: int = 0) -> None:
        self._fields = self._get_board_fields(pawns_number)
        self._set_all_connections(pawns_number)
        self._pawns_number = pawns_number
        self._starting_player = None
        self._bot = bot
        self._delay = delay
        self._moves_without_mill = 0

    def fields(self) -> List[Field]:
        return self._fields

    def pawns_number(self) -> PawnsNumber:
        return self._pawns_number

    def bot(self) -> BotLvl:
        return self._bot

    def delay(self) -> int:
        return self._delay

    def moves_without_mill(self):
        return self._moves_without_mill

    def add_one_move_without_mill(self):
        self._moves_without_mill += 1

    def reset_moves_without_mill(self):
        self._moves_without_mill = 0

    def starting_player(self) -> Player:
        return self._starting_player

    def set_starting_player(self, player: Player) -> None:
        self._starting_player = player

    def add_pawn(self, field: Field, player: Player) -> None:
        """
        Method to add player's pawn at specific field.
        It checks if field is free before adding
        """

        if self.is_field_free(field):
            field.set_player(player)

    def remove_pawn(self, field: Field) -> None:
        """
        Method to remove player's pawn from specific field
        It checks if there is a pawn at this field
        """

        if field.player():
            field.set_player(None)

    # Check if new field has connection with previous one
    # TODO check connections

    def move_pawn(self, current_field: Field, new_field: Field, player: Player) -> None:
        """
        Method to move player's pawn from one field to another
        It checks if new field is free, and there's connection with old one
        """

        if new_field.player() is None and new_field.id() in current_field.connections():
            current_field.set_player(None)
            new_field.set_player(player)

    def is_field_free(self, field: Field) -> bool:
        return True if field.player() is None else False

    def field_by_positions(self, coordinates: Coordinates) -> Field:
        """Find and returns field by given coordinates"""
        for field in self._fields:
            if field.coordiantes() == coordinates:
                return field

    def field_by_id(self, id: str) -> Field:
        """Returns field by given id"""

        id = id.upper()
        return next((field for field in self._fields if field.id() == id), None)

    def player_pawns_number(self, player: Player) -> int:
        """Returns number of pawns on field for specific player"""

        return sum(1 for field in self._fields if field.player() == player)

    def get_all_player_fields(self, player: Player) -> List[Field]:
        """Returns list of fields occupied by given player's pawns """

        return [field for field in self._fields if field.player() == player]

    def get_all_free_fields(self) -> List[Field]:
        """Returns list of all fields without pawn"""

        return [field for field in self._fields if field.player() is None]

    def _get_board_fields(self, pawns_number: PawnsNumber) -> List[Field]:
        """
        Returns list of fields depending on the pawns number.
        Used to set fields when creating board instance
        """

        if pawns_number == PawnsNumber.NINE:
            return self._create_fields_nine_or_twelve_pawns()
        elif pawns_number == PawnsNumber.THREE:
            return self._create_fields_three_pawns()
        elif pawns_number == PawnsNumber.SIX:
            return self._create_fields_six_pawns()
        elif pawns_number == PawnsNumber.TWELVE:
            return self._create_fields_nine_or_twelve_pawns()

    def _create_fields_three_pawns(self) -> List[Field]:
        """Returns list of fields for three pawns board"""

        fields_list = []
        id_index = 0

        for position_tmb in POS_TMB_LIST:
            for position_lcr in POS_LCR_LIST:
                fields_list.append(Field(FIELD_IDS[id_index], Coordinates(
                    pos_sq.MIDDLE, position_tmb, position_lcr)))
                id_index += 1
        return fields_list

    def _create_fields_six_pawns(self) -> List[Field]:
        """Returns list of fields for six pawns board"""

        fields_list = []
        id_index = 0

        for square in POS_SQ_OI_LIST:
            for position_lcr in POS_LCR_LIST:
                coord = Coordinates(square, pos.TOP, position_lcr)
                fields_list.append(Field(FIELD_IDS[id_index], coord))
                id_index += 1

        for square in POS_SQ_OI_LIST:
            coord = Coordinates(square, pos.MIDDLE, pos.LEFT)
            fields_list.append(Field(FIELD_IDS[id_index], coord))
            id_index += 1

        for square in reversed(POS_SQ_OI_LIST):
            coord = Coordinates(square, pos.MIDDLE, pos.RIGHT)
            fields_list.append(Field(FIELD_IDS[id_index], coord))
            id_index += 1

        for square in reversed(POS_SQ_OI_LIST):
            for position_lcr in POS_LCR_LIST:
                coord = Coordinates(square, pos.BOTTOM, position_lcr)
                fields_list.append(Field(FIELD_IDS[id_index], coord))
                id_index += 1

        return fields_list

    def _create_fields_nine_or_twelve_pawns(self) -> List[Field]:
        """Returns list of fields for nine/twelve pawns board"""

        fields_list = []
        id_index = 0

        for square in pos_sq:
            for position_lcr in POS_LCR_LIST:
                coord = Coordinates(square, pos.TOP, position_lcr)
                fields_list.append(Field(FIELD_IDS[id_index], coord))
                id_index += 1

        for square in pos_sq:
            coord = Coordinates(square, pos.MIDDLE, pos.LEFT)
            fields_list.append(Field(FIELD_IDS[id_index], coord))
            id_index += 1

        for square in reversed(pos_sq):
            coord = Coordinates(square, pos.MIDDLE, pos.RIGHT)
            fields_list.append(Field(FIELD_IDS[id_index], coord))
            id_index += 1

        for square in reversed(pos_sq):
            for position_lcr in POS_LCR_LIST:
                coord = Coordinates(square, pos.BOTTOM, position_lcr)
                fields_list.append(Field(FIELD_IDS[id_index], coord))
                id_index += 1

        return fields_list

    def _set_all_connections(self, pawns_number) -> None:
        """
        Calls method to set fields depending on pawns number
        Used once at creating board instance
        """

        if pawns_number == PawnsNumber.NINE:
            self._set_connections_nine_pawns()
        elif pawns_number == PawnsNumber.THREE:
            self._set_connections_three_pawns()
        elif pawns_number == PawnsNumber.SIX:
            self._set_connections_six_pawns()
        elif pawns_number == PawnsNumber.TWELVE:
            self._set_connections_twelve_pawns()

    def _set_connections_three_pawns(self) -> None:
        """Set connections between fields at three pawns board"""

        for field_id, connections in zip(CONNECTIONS_THREE.keys(), CONNECTIONS_THREE.values()):
            self.field_by_id(field_id).set_connections(connections)

    def _set_connections_six_pawns(self) -> None:
        """Set connections between fields at six pawns board"""

        for field_id, connections in zip(CONNECTIONS_SIX.keys(), CONNECTIONS_SIX.values()):
            self.field_by_id(field_id).set_connections(connections)

    def _set_connections_nine_pawns(self) -> None:
        """Set connections between fields at nine pawns board"""

        for field_id, connections in zip(CONNECTIONS_NINE.keys(), CONNECTIONS_NINE.values()):
            self.field_by_id(field_id).set_connections(connections)

    def _set_connections_twelve_pawns(self) -> None:
        """Set connections between fields at twelve pawns board"""

        for field_id, connections in zip(CONNECTIONS_TWELVE.keys(), CONNECTIONS_TWELVE.values()):
            self.field_by_id(field_id).set_connections(connections)
