from board import Board
from enums import Position, PositionSquare
from itertools import cycle


def main():
    print_welcome()
    choose_mode()
    print_board()


def choose_mode():
    print_choose_mode()


def print_board():
    board = Board()
    printDic = {PositionSquare.OUTER: print_outer,
                PositionSquare.MIDDLE: print_middle, PositionSquare.INNER: print_inner}
    printDic2 = {(PositionSquare.OUTER, Position.LEFT): "",
                 (PositionSquare.OUTER, Position.CENTER): 14*"-",
                 (PositionSquare.OUTER, Position.RIGHT): 14*"-",
                 (PositionSquare.MIDDLE, Position.LEFT): "|" + 4*" ",
                 (PositionSquare.MIDDLE, Position.CENTER):  9*"-",
                 (PositionSquare.MIDDLE, Position.RIGHT): 9*"-",
                 (PositionSquare.INNER, Position.LEFT): "|" + 4*" " + "|" + 4*" ",
                 (PositionSquare.INNER, Position.CENTER): 4*"-",
                 (PositionSquare.INNER, Position.RIGHT): 4*"-"}
    printDic3 = {PositionSquare.OUTER: "",
                 PositionSquare.MIDDLE: 4*" " + "|",
                 PositionSquare.INNER: 2*(4*" " + "|")}
    string = ""
    for positionSquare in [PositionSquare.OUTER, PositionSquare.MIDDLE, PositionSquare.INNER]:
        for position in [Position.LEFT, Position.CENTER, Position.RIGHT]:
            field = board.find_field_with_given_positions(
                positionSquare, Position.TOP, position)
            # Print will difer if field will be empty or there will be different pawns
            string += printDic2[(positionSquare, position)]
            string += "o"
        string += printDic3[positionSquare]
        string += "\n"
        string += printDic[positionSquare]()
        string += "\n"
    # MIDDLE
    for position in [Position.LEFT,  Position.RIGHT]:
        for positionSquare in [PositionSquare.OUTER, PositionSquare.MIDDLE, PositionSquare.INNER]:
            field = board.find_field_with_given_positions(
                positionSquare, Position.MIDDLE, position)
            string += "o"
            string += 4*"-" if positionSquare == PositionSquare.OUTER or positionSquare == PositionSquare.MIDDLE else ""
        string += 9 * " "
    string += "\n"
    # BOTTOM
    for positionSquare in [PositionSquare.INNER, PositionSquare.MIDDLE, PositionSquare.OUTER]:
        string += printDic[positionSquare]()
        string += "\n"
        for position in [Position.LEFT, Position.CENTER, Position.RIGHT]:
            field = board.find_field_with_given_positions(
                positionSquare, Position.TOP, position)
            # Print will difer if field will be empty or there will be different pawns
            string += printDic2[(positionSquare, position)]
            string += "o"
        string += printDic3[positionSquare]
        string += "\n"

    print(string)

# OUTER -> TOP -> LEFT CENTER RIGHT
# MIDDLE -> TOP -> LEFT CENTER RIGHT
# INNER -> TOP -> LEFT CENTER RIGHT
# OUTER MIDDLE LEFT -> MIDDLE MIDDLE LEFT -> INNER MIDDLE LEFT -> INNER MIDDLE RIGHT -> MIDDLE MIDDLE RIGHT -> OUTER MIDDLE RIGHT
# INNER -> BOTTOM -> LEFT CENTER RIGHT
# MIDDLE -> BOTTOM -> LEFT CENTER RIGHT
# OUTTER -> BOTTOM -> LEFT CENTER RIGHT


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


if __name__ == "__main__":
    main()
