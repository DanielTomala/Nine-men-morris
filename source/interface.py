from typing import List

from source.board import Board
from source.consts import FIELD_IDS, PLAYER_SYMBOL, PLAYER_TO_STR
from source.enums import Player
from source.file_handler import read_board_from_file


def print_board(board: Board):
    board_blueprint = read_board_from_file(board.pawns_number())
    board_to_print = ""
    index = 0
    for char in board_blueprint:
        if char == PLAYER_SYMBOL[None]:
            field = board.field_by_id(FIELD_IDS[index])
            board_to_print += PLAYER_SYMBOL[field.player()]
            index += 1
        else:
            board_to_print += char
    print(board_to_print)
    print_blank_lines(1)


def print_welcome():
    print("\t\t-------------------------")
    print("\t\tWELCOME IN THE MILL GAME!")
    print("\t\t-------------------------")
    print_blank_lines(1)


def print_instruction():
    print("Below you can see mill board. One on the left is board where you play,")
    print("while one the right is to help you with field id identification.")
    print("Program will let you now, what phase of the game is and what you have to do.")
    print("\nGOOD LUCK and HAVE FUN during the MILL GAME!")


def print_starting_player(player):
    print(f"Player {PLAYER_TO_STR[player]} will start the game")
    print_blank_lines(1)


def print_before_move(player):
    print("\t\t-----------------")
    print(f"\t\tPlayer's {PLAYER_TO_STR[player].capitalize()} turn")
    print(f"\t\tYour symbol is {PLAYER_SYMBOL[player]}")
    print("\t\t----------------- ")
    print_blank_lines(1)


def print_before_move_bot():
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


def print_last_set(field_id):
    print(f"Last pawn was set at field {field_id}")
    print_blank_lines(1)


def print_last_move(old_field_id, new_field_id):
    print(f"Last move was from field {old_field_id} to {new_field_id}")
    print_blank_lines(1)


def print_last_remove(field_id):
    print(f"Last pawn was removed from field {field_id}")
    print_blank_lines(1)


def print_possible_moves(fields: List[str]):
    print(f"You can move to fields with id's: {fields}")


def print_cancel_move():
    print("If you want to cancel this move and choose another field enter: `")
    print_blank_lines(1)


def print_move_canceled():
    print("Move canceled")
    print_blank_lines(1)


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
    print("This pawn doesn't belong to you. Try again.")
    print_blank_lines(1)


def print_remove_own_pawn():
    print("You cannot remove your own pawn. Try again.")
    print_blank_lines(1)


def print_no_possible_move():
    print("There is no possible move with this pawn. Try again.")
    print_blank_lines(1)


def print_no_connection():
    print("There is no connection beetween these fields. Try again.")
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


def print_game_over():
    print("GAME OVER!")


def print_winner(winner):
    print(
        f"The Winner is player {PLAYER_TO_STR[winner]} ({PLAYER_SYMBOL[winner]})")


def print_draw():
    print("No one won, it's draw")


def print_blank_lines(how_many):
    print((how_many - 1) * "\n")


def get_user_input(message):
    return input(message)
