from typing import List

from .board import Board
from .consts import PLAYER_SYMBOL, PLAYER_TO_STR, POS_LCR_LIST, POS_SQ_OI_LIST, POS_TMB_LIST
from .coordinates import Coordinates
from .enums import PawnsNumber, Player
from .enums import Position as pos
from .enums import PositionSquare as pos_sq


def print_board(board: Board):
    rows_separator_six = {pos_sq.OUTER: _print_outer_six,
                         pos_sq.INNER: _print_inner_six}
    rows_separator_nine = {(pos_sq.OUTER, pos.TOP): _print_outer_nine,
                          (pos_sq.OUTER, pos.BOTTOM): _print_outer_nine,
                          (pos_sq.MIDDLE, pos.TOP): _print_middle_nine,
                          (pos_sq.MIDDLE, pos.BOTTOM): _print_middle_nine,
                          (pos_sq.INNER, pos.TOP): _print_inner,
                          (pos_sq.INNER, pos.BOTTOM): _print_inner}
    rows_separator_twelve = {(pos_sq.OUTER, pos.TOP): _print_outer_twelve_top,
                            (pos_sq.OUTER, pos.BOTTOM): _print_outer_twelve_bottom,
                            (pos_sq.MIDDLE, pos.TOP): _print_middle_twelve_top,
                            (pos_sq.MIDDLE, pos.BOTTOM): _print_middle_twelve_bottom,
                            (pos_sq.INNER, pos.TOP): _print_inner,
                            (pos_sq.INNER, pos.BOTTOM): _print_inner}

    columns_separator_six = {pos_sq.OUTER: {pos.LEFT: "",
                                            pos.CENTER: 9*"-",
                                            pos.RIGHT: 9*"-"},
                             pos_sq.INNER: {pos.LEFT: "|" + 4*" ",
                                            pos.CENTER: 4*"-",
                                            pos.RIGHT: 4*"-"}}
    columns_separator_nine = {pos_sq.OUTER: {pos.LEFT: "",
                                             pos.CENTER: 14*"-",
                                             pos.RIGHT: 14*"-"},
                              pos_sq.MIDDLE: {pos.LEFT: "|" + 4*" ",
                                              pos.CENTER:  9*"-",
                                              pos.RIGHT: 9*"-"},
                              pos_sq.INNER: {pos.LEFT: "|" + 4*" " + "|" + 4*" ",
                                             pos.CENTER: 4*"-",
                                             pos.RIGHT: 4*"-"}}
    print_dic_3_six = {pos_sq.OUTER: "",
                       pos_sq.MIDDLE: 4*" " + "|",
                       pos_sq.INNER: 4*" " + "|"}

    print_dic_3 = {pos_sq.OUTER: "",
                   pos_sq.MIDDLE: 4*" " + "|",
                   pos_sq.INNER: 2*(4*" " + "|")}

    print_dict_1_three = {pos.LEFT: "---",
                          pos.CENTER: "---",
                          pos.RIGHT: ""}
    print_dict_2_three = {pos.TOP: "| \\ | / |\n",
                          pos.MIDDLE: "| / | \\ |\n",
                          pos.BOTTOM: ""}

    if board.pawns_number() == PawnsNumber.NINE:
        _print_board_nine_or_twelve(
            board, rows_separator_nine, columns_separator_nine, print_dic_3)
    elif board.pawns_number() == PawnsNumber.THREE:
        _print_board_three(board, print_dict_1_three, print_dict_2_three)
    elif board.pawns_number() == PawnsNumber.SIX:
        _print_board_six(board, rows_separator_six,
                         columns_separator_six, print_dic_3_six)
    elif board.pawns_number() == PawnsNumber.TWELVE:
        _print_board_nine_or_twelve(
            board, rows_separator_twelve, columns_separator_nine, print_dic_3)


def _print_board_three(board: Board, print_dict_1_three, print_dict_2_three):
    board_str = ""
    for position_tmb in POS_TMB_LIST:
        for position_lcr in POS_LCR_LIST:
            coord = Coordinates(pos_sq.MIDDLE, position_tmb, position_lcr)
            field = board.field_by_positions(coord)
            board_str += PLAYER_SYMBOL[field.player()]
            board_str += print_dict_1_three[position_lcr]
        board_str += "\n"
        board_str += print_dict_2_three[position_tmb]
    print(board_str)


def _print_board_six(board: Board, print_dict_1_six,  print_dic_2, print_dic_3):
    board_str = ""
    # TOP
    board_str += _get_top_or_bottom_part_of_board_six(board, pos.TOP, print_dict_1_six,
                                                      print_dic_2, print_dic_3)
    # MIDDLE
    board_str += _get_middle_part_of_board_six(board)
    # BOTTOM
    board_str += _get_top_or_bottom_part_of_board_six(board, pos.BOTTOM, print_dict_1_six,
                                                      print_dic_2, print_dic_3)
    print(board_str)


def _print_board_nine_or_twelve(board: Board, print_dic, print_dic_2, print_dic_3):
    board_str = ""
    # TOP
    board_str += _get_top_or_bottom_part_of_board(board, pos.TOP, print_dic,
                                                  print_dic_2, print_dic_3)
    # MIDDLE
    board_str += _get_middle_part_of_board(board)
    # BOTTOM
    board_str += _get_top_or_bottom_part_of_board(board, pos.BOTTOM, print_dic,
                                                  print_dic_2, print_dic_3)

    print(board_str)


def _get_middle_part_of_board_six(board: Board):
    board_str = ""
    for position_square in [pos_sq.OUTER, pos_sq.INNER]:
        coord = Coordinates(position_square, pos.MIDDLE, pos.LEFT)
        field = board.field_by_positions(coord)
        board_str += PLAYER_SYMBOL[field.player()]
        board_str += 4 * \
            "-" if position_square == pos_sq.OUTER else ""
    board_str += 9 * " "
    for position_square in reversed(POS_SQ_OI_LIST):
        coord = Coordinates(position_square, pos.MIDDLE, pos.RIGHT)
        field = board.field_by_positions(coord)
        board_str += PLAYER_SYMBOL[field.player()]
        board_str += 4 * \
            "-" if position_square == pos_sq.INNER else ""
    board_str += 9 * " "
    board_str += "\n"
    return board_str


def _get_top_or_bottom_part_of_board_six(board: Board, position_given, print_dic, print_dic_2, print_dic_3):
    board_str = ""
    positions_list = POS_SQ_OI_LIST
    if position_given == pos.BOTTOM:
        positions_list.reverse()
    for position_square in positions_list:
        if position_given == pos.BOTTOM:
            board_str += print_dic[position_square]()
            board_str += "\n"
        for position in POS_LCR_LIST:
            coord = Coordinates(position_square, position_given, position)
            field = board.field_by_positions(coord)
            board_str += print_dic_2[position_square][position]
            board_str += PLAYER_SYMBOL[field.player()]
        board_str += print_dic_3[position_square]
        board_str += "\n"
        if position_given == pos.TOP:
            board_str += print_dic[position_square]()
            board_str += "\n"
    return board_str


def _get_middle_part_of_board(board: Board):
    board_str = ""
    for position_square in pos_sq:
        coord = Coordinates(position_square, pos.MIDDLE, pos.LEFT)
        field = board.field_by_positions(coord)
        board_str += PLAYER_SYMBOL[field.player()]
        board_str += 4 * \
            "-" if position_square in [pos_sq.OUTER,
                                       pos_sq.MIDDLE] else ""
    board_str += 9 * " "
    for position_square in reversed(pos_sq):
        coord = Coordinates(position_square, pos.MIDDLE, pos.RIGHT)
        field = board.field_by_positions(coord)
        board_str += PLAYER_SYMBOL[field.player()]
        board_str += 4 * \
            "-" if position_square in [pos_sq.INNER,
                                       pos_sq.MIDDLE] else ""
    board_str += 9 * " "
    board_str += "\n"
    return board_str


def _get_top_or_bottom_part_of_board(board: Board, position_given, print_dic, print_dic_2, print_dic_3):
    board_str = ""
    positions_list = [pos_sq.OUTER, pos_sq.MIDDLE, pos_sq.INNER]
    if position_given == pos.BOTTOM:
        positions_list.reverse()
    for position_square in positions_list:
        if position_given == pos.BOTTOM:
            board_str += print_dic[(position_square, position_given)]()
            board_str += "\n"
        for position in POS_LCR_LIST:
            coord = Coordinates(position_square, position_given, position)
            field = board.field_by_positions(coord)
            board_str += print_dic_2[position_square][position]
            board_str += PLAYER_SYMBOL[field.player()]
        board_str += print_dic_3[position_square]
        board_str += "\n"
        if position_given == pos.TOP:
            board_str += print_dic[(position_square, position_given)]()
            board_str += "\n"
    return board_str


def _print_outer_nine():
    return"|              |              |"


def _print_outer_six():
    return"|         |         |"


def _print_outer_twelve_top():
    return"| \\            |            / |"


def _print_outer_twelve_bottom():
    return"| /            |            \\ |"


def _print_middle_nine():
    return"|    |         |         |    |"


def _print_middle_twelve_top():
    return"|    | \\       |       / |    |"


def _print_middle_twelve_bottom():
    return"|    | /       |       \\ |    |"


def _print_inner_six():
    return "|    |         |    |"


def _print_inner():
    return"|    |    |         |    |    |"


def print_welcome():
    print("\t\t-------------------------")
    print("\t\tWELCOME IN THE MILL GAME!")
    print("\t\t-------------------------")


def print_starting_player(player):
    print(f"Player {PLAYER_TO_STR[player]} will start the game")
    print_blank_lines(1)


def print_before_move(player):
    # Dodać możliwość podania nazw graczy przed rozgrywką
    # Paski na długość tekstu
    print("\t\t-----------------")
    print(f"\t\tPlayer's {PLAYER_TO_STR[player].capitalize()} turn")
    # TODO
    print(f"\t\tYour symbol is {PLAYER_SYMBOL[player]}")
    print("\t\t----------------- ")
    print_blank_lines(1)


def print_before_move_bot():
    # Dodać możliwość podania nazw graczy przed rozgrywką
    print("\t\t----------")
    print("\t\tBot's turn")
    print("\t\t----------")
    print_blank_lines(1)


def print_pawns_left(board: Board, player: Player, pawns_in_hand):
    print(
        f"Pawns left in hand: {pawns_in_hand* PLAYER_SYMBOL[player]}: {pawns_in_hand}")
    print(
        f"Pawns on field: {board.player_pawns_number(player)*PLAYER_SYMBOL[player]}: {board.player_pawns_number(player)}")
    print_blank_lines(1)

    # Pawns Left: ### : 3
    # Pawns Already set: ###### : 6


def print_last_set(field_id):
    print(f"Last pawn was set at field {field_id}")


def print_last_move(old_field_id, new_field_id):
    print(f"Last move was from field {old_field_id} to {new_field_id}")


def print_last_remove(field_id):
    print(f"Last pawn was removed from field {field_id}")


def print_possible_moves(fields: List[str]):
    print(f"You can move to fields with id's: {fields}")
    print_blank_lines(1)


def print_blank_lines(how_many):
    print((how_many - 1) * "\n")


def print_field_occupied():
    print("This field is already occupied. Try again.")
    print_blank_lines(1)


def print_improper_id():
    print("Improper field id. Try again.")
    print_blank_lines(1)


def print_no_pawn():
    print("There is no pawn at this field. Try again.")
    print_blank_lines(1)


def print_not_your_pawn():
    print("This pawn doesn't belong to you. Try again")
    print_blank_lines(1)


def print_mill_occurred(mill_num: int):
    print(
        f"You have {mill_num} mill(s), now you can remove yours opponent {mill_num} pawn(s)!")
    print_blank_lines(1)


def print_bot_mill_occurred(mill_num):
    print(f"Bot has {mill_num} mill(s)")
    print_blank_lines(1)


def print_transition_to_moving_phase():
    print("All pawns are set, let's move to the next phase of the game!")
    print_blank_lines(1)


def print_remove_own_pawn():
    print("You cannot remove your own pawn")
    print_blank_lines(1)


def print_instruction():
    pass


def print_choose_pawns_number():
    print("You can choose from four modes of mill game.")
    print("Each player can have:")
    print("[1] Nine pawns (classic mode),")
    print("[2] Three pawns,")
    print("[3] Six pawns,")
    print("[4] Twelve pawns.")


def print_choose_against_who():
    print("You can also choose against who do you want to play:")
    print("[1] One player against bot")
    print("[2] Two players against each other")


def print_winner(winner):
    print(f"The Winner is player {PLAYER_TO_STR[winner]}")
