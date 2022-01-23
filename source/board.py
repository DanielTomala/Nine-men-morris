from typing import List
from .coordinates import Coordinates
from .enums import BotLvl, PawnsNumber, Player, Position as pos, PositionSquare as pos_sq
from .field import Field

FIELD_IDS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
             "L", "M", "N", "O", "P", "R", "S", "T", "U", "W", "X", "Y", "Z"]


class Board:
    def __init__(self, pawns_number: PawnsNumber = PawnsNumber.NINE, bot: BotLvl = BotLvl.OFF, delay: int = 0) -> None:
        self._fields = self._get_fields_for_pawns_number(pawns_number)
        self.set_proper_connections(pawns_number)
        self._pawns_number = pawns_number
        self._starting_player = None
        self._bot = bot
        self._delay = delay

    def fields(self):
        return self._fields

    def pawns_number(self):
        return self._pawns_number

    def starting_player(self):
        return self._starting_player

    def set_starting_player(self, player: Player):
        self._starting_player = player

    def bot(self):
        return self._bot

    def delay(self):
        return self._delay

    """
    After pawn is added, it is checked if mill occured
    """

    def add_pawn(self, field: Field, player: Player) -> None:
        if self.is_field_free(field):
            field.set_player(player)

    def remove_pawn(self, field: Field) -> None:
        if field.player():
            field.set_player(None)

    """
    After pawn is moved, it is checked if mill occured
    """
    # Check if new field has connection with previous one
    # TODO check connections

    def move_pawn(self, current_field: Field, new_field: Field, player: Player) -> None:
        if new_field.player() is None and new_field.id() in current_field.connections():
            current_field.set_player(None)
            new_field.set_player(player)

    def is_field_free(self, field: Field) -> bool:
        return_value = True if field.player() is None else False
        return return_value

    def field_by_positions(self, positionSquare: pos_sq, positionTMB: pos, positionLCR: pos) -> Field:
        for field in self._fields:
            if field.coordiantes().get_all_coordinates() == (positionSquare, positionTMB, positionLCR):
                return field

    def player_pawns_number(self, player) -> int:
        player_pawns_no = 0
        for field in self._fields:
            if field.player() == player:
                player_pawns_no += 1
        return player_pawns_no

    def field_by_id(self, id) -> Field:
        id = id.upper()
        for field in self._fields:
            if field.id() == id:
                return field

    def get_all_player_fields(self, player: Player) -> List[Field]:
        fields_to_return = []
        for field in self._fields:
            if field.player() == player:
                fields_to_return.append(field)
        return fields_to_return

    def get_all_free_fields(self):
        free_fields = []
        for field in self._fields:
            if field.player() is None:
                free_fields.append(field)
        return free_fields

    def _get_fields_for_pawns_number(self, pawns_number: PawnsNumber):
        if pawns_number == PawnsNumber.NINE:
            return self._create_fields_nine_or_twelve_pawns()
        elif pawns_number == PawnsNumber.THREE:
            return self._create_fields_three_pawns()
        elif pawns_number == PawnsNumber.SIX:
            return self._create_fields_six_pawns()
        elif pawns_number == PawnsNumber.TWELVE:
            return self._create_fields_nine_or_twelve_pawns()

    def _create_fields_nine_or_twelve_pawns(self) -> List[Field]:
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

    def _create_fields_six_pawns(self) -> List[Field]:
        fields_list = []
        id_index = 0
        for square in [pos_sq.OUTER, pos_sq.INNER]:
            for position_lcr in [pos.LEFT, pos.CENTER, pos.RIGHT]:
                fields_list.append(Field(FIELD_IDS[id_index], Coordinates(
                    square, pos.TOP, position_lcr)))
                id_index += 1
        for square in [pos_sq.OUTER, pos_sq.INNER]:
            fields_list.append(Field(FIELD_IDS[id_index], Coordinates(
                square, pos.MIDDLE, pos.LEFT)))
            id_index += 1
        for square in [pos_sq.INNER, pos_sq.OUTER]:
            fields_list.append(Field(FIELD_IDS[id_index], Coordinates(
                square, pos.MIDDLE, pos.RIGHT)))
            id_index += 1
        for square in [pos_sq.INNER, pos_sq.OUTER]:
            for position_lcr in [pos.LEFT, pos.CENTER, pos.RIGHT]:
                fields_list.append(Field(FIELD_IDS[id_index], Coordinates(
                    square, pos.BOTTOM, position_lcr)))
                id_index += 1
        return fields_list

    def _create_fields_three_pawns(self) -> List[Field]:
        fields_list = []
        id_index = 0

        for position_tmb in [pos.TOP, pos.MIDDLE, pos.BOTTOM]:
            for position_lcr in [pos.LEFT, pos.CENTER, pos.RIGHT]:
                fields_list.append(Field(FIELD_IDS[id_index], Coordinates(
                    pos_sq.MIDDLE, position_tmb, position_lcr)))
                id_index += 1
        return fields_list

    def set_proper_connections(self, pawns_number):
        if pawns_number == PawnsNumber.NINE:
            self._set_connections_nine_pawns()
        elif pawns_number == PawnsNumber.THREE:
            self._set_connections_three_pawns()
        elif pawns_number == PawnsNumber.SIX:
            self._set_connections_six_pawns()
        elif pawns_number == PawnsNumber.TWELVE:
            self._set_connections_twelve_pawns()

    def _set_connections_nine_pawns(self):
        self.field_by_id("A").set_connections(["B", "J"])
        self.field_by_id("B").set_connections(["A", "C", "E"])
        self.field_by_id("C").set_connections(["B", "O"])
        self.field_by_id("D").set_connections(["E", "K"])
        self.field_by_id("E").set_connections(["B", "D", "F", "H"])
        self.field_by_id("F").set_connections(["E", "N"])
        self.field_by_id("G").set_connections(["H", "L"])
        self.field_by_id("H").set_connections(["E", "G", "I"])
        self.field_by_id("I").set_connections(["H", "M"])
        self.field_by_id("J").set_connections(["A", "K", "X"])
        self.field_by_id("K").set_connections(["D", "J", "L", "T"])
        self.field_by_id("L").set_connections(["G", "K", "P"])
        self.field_by_id("M").set_connections(["I", "N", "S"])
        self.field_by_id("N").set_connections(["F", "M", "O", "W"])
        self.field_by_id("O").set_connections(["C", "N", "Z"])
        self.field_by_id("P").set_connections(["L", "R"])
        self.field_by_id("R").set_connections(["P", "S", "U"])
        self.field_by_id("S").set_connections(["M", "R"])
        self.field_by_id("T").set_connections(["K", "U"])
        self.field_by_id("U").set_connections(["R", "T", "W", "Y"])
        self.field_by_id("W").set_connections(["N", "U"])
        self.field_by_id("X").set_connections(["J", "Y"])
        self.field_by_id("Y").set_connections(["U", "X", "Z"])
        self.field_by_id("Z").set_connections(["O", "Y"])

# Może by to wczytać z pliku
    def _set_connections_three_pawns(self):
        self.field_by_id("A").set_connections(["B", "D", "E"])
        self.field_by_id("B").set_connections(["A", "C", "E"])
        self.field_by_id("C").set_connections(["B", "F", "E"])
        self.field_by_id("D").set_connections(["A", "E", "G"])
        self.field_by_id("E").set_connections(
            ["A", "B", "C", "D", "F", "G", "H", "I"])
        self.field_by_id("F").set_connections(["C", "E", "I"])
        self.field_by_id("G").set_connections(["D", "E", "H"])
        self.field_by_id("H").set_connections(["E", "G", "I"])
        self.field_by_id("I").set_connections(["E", "F", "H"])

    # A---B---C
    # | ⟍ | ⟋ |
    # D---E---F
    # | ⟋ | ⟍ |
    # G---H---I
    def _set_connections_six_pawns(self):
        self.field_by_id("A").set_connections(["B", "G"])
        self.field_by_id("B").set_connections(["A", "C", "E"])
        self.field_by_id("C").set_connections(["B", "J"])
        self.field_by_id("D").set_connections(["E", "H"])
        self.field_by_id("E").set_connections(["B", "D", "F"])
        self.field_by_id("F").set_connections(["E", "I"])
        self.field_by_id("G").set_connections(["A", "H", "N"])
        self.field_by_id("H").set_connections(["D", "G", "K"])
        self.field_by_id("I").set_connections(["F", "J", "M"])
        self.field_by_id("J").set_connections(["C", "I", "P"])
        self.field_by_id("K").set_connections(["H", "L"])
        self.field_by_id("L").set_connections(["K", "M", "O"])
        self.field_by_id("M").set_connections(["I", "L"])
        self.field_by_id("N").set_connections(["G", "O"])
        self.field_by_id("O").set_connections(["L", "N", "P"])
        self.field_by_id("P").set_connections(["J", "O"])

    # A---------B---------C
    # |         |         |
    # |    D----E----F    |
    # |    |         |    |
    # G----H         I----J
    # |    |         |    |
    # |    K----L----M    |
    # |         |         |
    # N---------O---------P

    def _set_connections_twelve_pawns(self):
        self.field_by_id("A").set_connections(["B", "D", "J"])
        self.field_by_id("B").set_connections(["A", "C", "E"])
        self.field_by_id("C").set_connections(["B", "F", "O"])
        self.field_by_id("D").set_connections(["A", "E", "G", "K"])
        self.field_by_id("E").set_connections(["B", "D", "F", "H"])
        self.field_by_id("F").set_connections(["C", "E", "I", "N"])
        self.field_by_id("G").set_connections(["D", "H", "L"])
        self.field_by_id("H").set_connections(["E", "G", "I"])
        self.field_by_id("I").set_connections(["F", "H", "M"])
        self.field_by_id("J").set_connections(["A", "K", "X"])
        self.field_by_id("K").set_connections(["D", "J", "L", "T"])
        self.field_by_id("L").set_connections(["G", "K", "P"])
        self.field_by_id("M").set_connections(["I", "N", "S"])
        self.field_by_id("N").set_connections(["F", "M", "O", "W"])
        self.field_by_id("O").set_connections(["C", "N", "Z"])
        self.field_by_id("P").set_connections(["L", "R", "T"])
        self.field_by_id("R").set_connections(["P", "S", "U"])
        self.field_by_id("S").set_connections(["M", "R", "W"])
        self.field_by_id("T").set_connections(["K", "P", "U", "X"])
        self.field_by_id("U").set_connections(["R", "T", "W", "Y"])
        self.field_by_id("W").set_connections(["N", "S", "U", "Z"])
        self.field_by_id("X").set_connections(["J", "T", "Y"])
        self.field_by_id("Y").set_connections(["U", "X", "Z"])
        self.field_by_id("Z").set_connections(["O", "W", "Y"])

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
