from typing import List

from pyrsistent import field

from .consts import CONNECTIONS_NINE, CONNECTIONS_SIX, CONNECTIONS_THREE, CONNECTIONS_TWELVE, FIELD_IDS, POS_LCR_LIST, POS_SQ_OI_LIST, POS_TMB_LIST

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

    def fields(self) -> List[Field]:
        return self._fields

    def pawns_number(self) -> PawnsNumber:
        return self._pawns_number

    def bot(self) -> BotLvl:
        return self._bot

    def delay(self) -> int:
        return self._delay

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

        # self.field_by_id("A").set_connections(["B", "D", "E"])
        # self.field_by_id("B").set_connections(["A", "C", "E"])
        # self.field_by_id("C").set_connections(["B", "F", "E"])
        # self.field_by_id("D").set_connections(["A", "E", "G"])
        # self.field_by_id("E").set_connections(
        #     ["A", "B", "C", "D", "F", "G", "H", "I"])
        # self.field_by_id("F").set_connections(["C", "E", "I"])
        # self.field_by_id("G").set_connections(["D", "E", "H"])
        # self.field_by_id("H").set_connections(["E", "G", "I"])
        # self.field_by_id("I").set_connections(["E", "F", "H"])

        for field_id, connections in zip(CONNECTIONS_THREE.keys(), CONNECTIONS_THREE.values()):
            self.field_by_id(field_id).set_connections(connections)

    def _set_connections_six_pawns(self) -> None:
        """Set connections between fields at six pawns board"""

        # self.field_by_id("A").set_connections(["B", "G"])
        # self.field_by_id("B").set_connections(["A", "C", "E"])
        # self.field_by_id("C").set_connections(["B", "J"])
        # self.field_by_id("D").set_connections(["E", "H"])
        # self.field_by_id("E").set_connections(["B", "D", "F"])
        # self.field_by_id("F").set_connections(["E", "I"])
        # self.field_by_id("G").set_connections(["A", "H", "N"])
        # self.field_by_id("H").set_connections(["D", "G", "K"])
        # self.field_by_id("I").set_connections(["F", "J", "M"])
        # self.field_by_id("J").set_connections(["C", "I", "P"])
        # self.field_by_id("K").set_connections(["H", "L"])
        # self.field_by_id("L").set_connections(["K", "M", "O"])
        # self.field_by_id("M").set_connections(["I", "L"])
        # self.field_by_id("N").set_connections(["G", "O"])
        # self.field_by_id("O").set_connections(["L", "N", "P"])
        # self.field_by_id("P").set_connections(["J", "O"])
        for field_id, connections in zip(CONNECTIONS_SIX.keys(), CONNECTIONS_SIX.values()):
            self.field_by_id(field_id).set_connections(connections)

    def _set_connections_nine_pawns(self) -> None:
        """Set connections between fields at nine pawns board"""

        # self.field_by_id("A").set_connections(["B", "J"])
        # self.field_by_id("B").set_connections(["A", "C", "E"])
        # self.field_by_id("C").set_connections(["B", "O"])
        # self.field_by_id("D").set_connections(["E", "K"])
        # self.field_by_id("E").set_connections(["B", "D", "F", "H"])
        # self.field_by_id("F").set_connections(["E", "N"])
        # self.field_by_id("G").set_connections(["H", "L"])
        # self.field_by_id("H").set_connections(["E", "G", "I"])
        # self.field_by_id("I").set_connections(["H", "M"])
        # self.field_by_id("J").set_connections(["A", "K", "X"])
        # self.field_by_id("K").set_connections(["D", "J", "L", "T"])
        # self.field_by_id("L").set_connections(["G", "K", "P"])
        # self.field_by_id("M").set_connections(["I", "N", "S"])
        # self.field_by_id("N").set_connections(["F", "M", "O", "W"])
        # self.field_by_id("O").set_connections(["C", "N", "Z"])
        # self.field_by_id("P").set_connections(["L", "R"])
        # self.field_by_id("R").set_connections(["P", "S", "U"])
        # self.field_by_id("S").set_connections(["M", "R"])
        # self.field_by_id("T").set_connections(["K", "U"])
        # self.field_by_id("U").set_connections(["R", "T", "W", "Y"])
        # self.field_by_id("W").set_connections(["N", "U"])
        # self.field_by_id("X").set_connections(["J", "Y"])
        # self.field_by_id("Y").set_connections(["U", "X", "Z"])
        # self.field_by_id("Z").set_connections(["O", "Y"])

        for field_id, connections in zip(CONNECTIONS_NINE.keys(), CONNECTIONS_NINE.values()):
            self.field_by_id(field_id).set_connections(connections)

    def _set_connections_twelve_pawns(self) -> None:
        """Set connections between fields at twelve pawns board"""

        # self.field_by_id("A").set_connections(["B", "D", "J"])
        # self.field_by_id("B").set_connections(["A", "C", "E"])
        # self.field_by_id("C").set_connections(["B", "F", "O"])
        # self.field_by_id("D").set_connections(["A", "E", "G", "K"])
        # self.field_by_id("E").set_connections(["B", "D", "F", "H"])
        # self.field_by_id("F").set_connections(["C", "E", "I", "N"])
        # self.field_by_id("G").set_connections(["D", "H", "L"])
        # self.field_by_id("H").set_connections(["E", "G", "I"])
        # self.field_by_id("I").set_connections(["F", "H", "M"])
        # self.field_by_id("J").set_connections(["A", "K", "X"])
        # self.field_by_id("K").set_connections(["D", "J", "L", "T"])
        # self.field_by_id("L").set_connections(["G", "K", "P"])
        # self.field_by_id("M").set_connections(["I", "N", "S"])
        # self.field_by_id("N").set_connections(["F", "M", "O", "W"])
        # self.field_by_id("O").set_connections(["C", "N", "Z"])
        # self.field_by_id("P").set_connections(["L", "R", "T"])
        # self.field_by_id("R").set_connections(["P", "S", "U"])
        # self.field_by_id("S").set_connections(["M", "R", "W"])
        # self.field_by_id("T").set_connections(["K", "P", "U", "X"])
        # self.field_by_id("U").set_connections(["R", "T", "W", "Y"])
        # self.field_by_id("W").set_connections(["N", "S", "U", "Z"])
        # self.field_by_id("X").set_connections(["J", "T", "Y"])
        # self.field_by_id("Y").set_connections(["U", "X", "Z"])
        # self.field_by_id("Z").set_connections(["O", "W", "Y"])
        for field_id, connections in zip(CONNECTIONS_TWELVE.keys(), CONNECTIONS_TWELVE.values()):
            self.field_by_id(field_id).set_connections(connections)

# Może by to wczytać z pliku

    # A---B---C
    # | ⟍ | ⟋ |
    # D---E---F
    # | ⟋ | ⟍ |
    # G---H---I

    # A---------B---------C
    # |         |         |
    # |    D----E----F    |
    # |    |         |    |
    # G----H         I----J
    # |    |         |    |
    # |    K----L----M    |
    # |         |         |
    # N---------O---------P

    # A--------------B--------------C
    # | \            |           /  |
    # |    D---------E---------F    |
    # |    | \       |      /  |    |
    # |    |    G----H----I    |    |
    # |    |    |         |    |    |
    # J----K----L         M----N----O
    # |    |    |         |    |    |
    # |    |    P----R----S    |    |
    # |    | /       |       \ |    |
    # |    T---------U---------W    |
    # | /            |            \ |
    # X--------------Y--------------Z

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

    # o---o---o
    # | ⟍ | ⟋ |
    # o---o---o
    # | ⟋ | ⟍ |
    # o---o---o

    # o---------o---------o
    # |         |         |
    # |    o----o----o    |
    # |    |         |    |
    # o----o         o----o
    # |    |         |    |
    # |    o----o----o    |
    # |         |         |
    # o---------o---------o

    # o--------------o--------------o
    # | \            |           /  |
    # |    o---------o---------o    |
    # |    | \       |      /  |    |
    # |    |    o----o----o    |    |
    # |    |    |         |    |    |
    # o----o----o         o----o----o
    # |    |    |         |    |    |
    # |    |    o----o----o    |    |
    # |    | /       |       \ |    |
    # |    o---------o---------o    |
    # | /            |            \ |
    # o--------------o--------------o
