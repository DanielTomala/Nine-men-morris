from .board import Board
from .enums import Player, Position as pos, PositionSquare as pos_sq
from itertools import cycle
from .pawn import Pawn


def main():
    print_welcome()
    choose_mode()
    print_board()


def choose_mode():
    print_choose_mode()


def print_board():
    board = Board()
    board.fields()[0].set_current_pawn(Pawn(player=Player.FIRST))
    board.fields()[1].set_current_pawn(Pawn(player=Player.SECOND))
    player_symbols = {Player.FIRST: "X", Player.SECOND: "Y"}
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


# OUTER -> TOP -> LEFT CENTER RIGHT
# MIDDLE -> TOP -> LEFT CENTER RIGHT
# INNER -> TOP -> LEFT CENTER RIGHT
# OUTER MIDDLE LEFT -> MIDDLE MIDDLE LEFT -> INNER MIDDLE LEFT -> INNER MIDDLE RIGHT -> MIDDLE MIDDLE RIGHT -> OUTER MIDDLE RIGHT
# INNER -> BOTTOM -> LEFT CENTER RIGHT
# MIDDLE -> BOTTOM -> LEFT CENTER RIGHT
# OUTTER -> BOTTOM -> LEFT CENTER RIGHT
def get_middle_part_of_board(board, player_symbols):
    board_str = ""
    for position in [pos.LEFT,  pos.RIGHT]:
        for position_square in [pos_sq.OUTER, pos_sq.MIDDLE, pos_sq.INNER]:
            field = board.find_field_with_given_positions(
                position_square, pos.MIDDLE, position)
            board_str += player_symbols[field.currentPawn().player()
                                        ] if field and field.currentPawn() else "o"
            board_str += 4 * \
                "-" if position_square in [pos_sq.OUTER,
                                           pos_sq.MIDDLE] else ""
        board_str += 9 * " "
    board_str += "\n"
    return board_str


def get_top_or_bottom_part_of_board(board, position_given, print_dic, print_dic_2, print_dic_3, player_symbols):
    string = ""
    positions_list = [pos_sq.OUTER, pos_sq.MIDDLE, pos_sq.INNER]
    if position_given == pos.BOTTOM:
        positions_list.reverse()
    for position_square in positions_list:
        if position_given == pos.BOTTOM:
            string += print_dic[position_square]()
            string += "\n"
        for position in [pos.LEFT, pos.CENTER, pos.RIGHT]:
            field = board.find_field_with_given_positions(
                position_square, position_given, position)
            # Print will difer if field will be empty or there will be different pawns
            string += print_dic_2[position_square][position]
            string += player_symbols[field.currentPawn().player()
                                     ] if field and field.currentPawn() else "o"
        string += print_dic_3[position_square]
        string += "\n"
        if position_given == pos.TOP:
            string += print_dic[position_square]()
            string += "\n"
    return string


def print_outer():
    return"|              |              |"


def print_middle():
    return"|    |         |         |    |"


def print_inner():
    return"|    |    |         |    |    |"


def print_welcome():
    print("WELCOME IN THE MILL GAME!")


def print_choose_mode():
    pass
