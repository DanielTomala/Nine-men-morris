from typing import List
from .board import Board
from .enums import Player, Position as pos, PositionSquare as pos_sq

OTHER_PLAYER = {Player.FIRST: Player.SECOND,
                Player.SECOND: Player.FIRST}
PLAYER_TO_STR = {Player.FIRST: "One", Player.SECOND: "Two"}
PLAYER_SYMBOL = {Player.FIRST: "$", Player.SECOND: "#"}


def print_board(board: Board):
    player_symbols = {Player.FIRST: "$", Player.SECOND: "#"}
    print_dic = {pos_sq.OUTER: print_outer,
                 pos_sq.MIDDLE: print_middle,
                 pos_sq.INNER: print_inner}
    print_dic_2 = {pos_sq.OUTER: {pos.LEFT: "",
                                  pos.CENTER: 14*"-",
                                  pos.RIGHT: 14*"-"},
                   pos_sq.MIDDLE: {pos.LEFT: "|" + 4*" ",
                                   pos.CENTER:  9*"-",
                                   pos.RIGHT: 9*"-"},
                   pos_sq.INNER: {pos.LEFT: "|" + 4*" " + "|" + 4*" ",
                                  pos.CENTER: 4*"-",
                                  pos.RIGHT: 4*"-"}}
    print_dic_3 = {pos_sq.OUTER: "",
                   pos_sq.MIDDLE: 4*" " + "|",
                   pos_sq.INNER: 2*(4*" " + "|")}
    board_str = ""
    # TOP
    board_str += get_top_or_bottom_part_of_board(board, pos.TOP, print_dic,
                                                 print_dic_2, print_dic_3, player_symbols)
    # MIDDLE
    board_str += get_middle_part_of_board(board, player_symbols)
    # BOTTOM
    board_str += get_top_or_bottom_part_of_board(board, pos.BOTTOM, print_dic,
                                                 print_dic_2, print_dic_3, player_symbols)

    print(board_str)


def get_middle_part_of_board(board: Board, player_symbols):
    board_str = ""
    for position_square in pos_sq:
        field = board.field_by_positions(
            position_square, pos.MIDDLE, pos.LEFT)
        # board_str += field.id()
        board_str += player_symbols[field.player()
                                    ] if field.player() else "o"
        board_str += 4 * \
            "-" if position_square in [pos_sq.OUTER,
                                       pos_sq.MIDDLE] else ""
    board_str += 9 * " "
    for position_square in reversed(pos_sq):
        field = board.field_by_positions(
            position_square, pos.MIDDLE, pos.RIGHT)
        # board_str += field.id()
        board_str += player_symbols[field.player()
                                    ] if field.player() else "o"
        board_str += 4 * \
            "-" if position_square in [pos_sq.INNER,
                                       pos_sq.MIDDLE] else ""
    board_str += 9 * " "
    board_str += "\n"
    return board_str


def get_top_or_bottom_part_of_board(board: Board, position_given, print_dic, print_dic_2, print_dic_3, player_symbols):
    board_str = ""
    positions_list = [pos_sq.OUTER, pos_sq.MIDDLE, pos_sq.INNER]
    if position_given == pos.BOTTOM:
        positions_list.reverse()
    for position_square in positions_list:
        if position_given == pos.BOTTOM:
            board_str += print_dic[position_square]()
            board_str += "\n"
        for position in [pos.LEFT, pos.CENTER, pos.RIGHT]:
            field = board.field_by_positions(
                position_square, position_given, position)
            # Print will difer if field will be empty or there will be different pawns
            board_str += print_dic_2[position_square][position]
            # board_str += field.id()
            board_str += player_symbols[field.player()
                                        ] if field.player() else "o"
        board_str += print_dic_3[position_square]
        board_str += "\n"
        if position_given == pos.TOP:
            board_str += print_dic[position_square]()
            board_str += "\n"
    return board_str


def print_outer():
    return"|              |              |"


def print_middle():
    return"|    |         |         |    |"


def print_inner():
    return"|    |    |         |    |    |"


def print_welcome():
    print("\t\t-------------------------")
    print("\t\tWELCOME IN THE MILL GAME!")
    print("\t\t-------------------------")


def print_starting_player(player):
    print(f"Player number {PLAYER_TO_STR[player]} will start the game")
    print_blank_lines(1)


def print_before_move(player):
    # Dodać możliwość podania nazw graczy przed rozgrywką
    print("-------------------------------------------")
    print(f"Player's number {PLAYER_TO_STR[player].capitalize()} turn")
    # TODO
    print(f"Your symbol is {PLAYER_SYMBOL[player]}")
    print("-------------------------------------------")
    print_blank_lines(1)


def print_pawns_left(board: Board, player: Player, pawns_in_hand):
    print(
        f"Pawns left in hand: {pawns_in_hand* PLAYER_SYMBOL[player]}: {pawns_in_hand}")
    print(
        f"Pawns on field: {board.player_pawns_number(player)*PLAYER_SYMBOL[player]}: {board.player_pawns_number(player)}")
    print_blank_lines(1)

    # Pawns Left: ### : 3
    # Pawns Already set: ###### : 6


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
