import random

from .board import FIELD_IDS, Board
from .enums import PawnsNumber, Player
from .enums import Position as pos
from .enums import PositionSquare as pos_sq
from .field import Field
from .interface import (OTHER_PLAYER, print_before_move, print_board,
                        print_choose_mode, print_empty_lines,
                        print_field_occupied, print_improper_id,
                        print_mill_occurred, print_no_pawn,
                        print_not_your_pawn, print_pawns_left,
                        print_starting_player,
                        print_transition_to_moving_phase, print_welcome)

# Podwójny młynek
# Koniec gry, gdy nie ma żadnego dostępnego ruchu
# Koniec gry, gdy zostaną dwa
# Remis, gdy trzykrotnie powtórzy się sytuacja na planszy
# Gdy graczowi zostaną trzy pionki może poruszać się swoimi pionkami na dowolne pola


def main():
    print_welcome()
    choose_mode()  # Zwróci liczbę pionków
    board = Board()
    print_board(board)
    start_game(board)


def start_game(board: Board):
    starting_player = get_starting_player()
    board.set_starting_player(starting_player)
    print_starting_player(starting_player)
    setting_pawns_phase(board)
    print_transition_to_moving_phase()
    moving_pawns_phase(board)


def get_starting_player():
    num_to_player = {1: Player.FIRST, 2: Player.SECOND}
    number = random.randint(1, 2)
    return num_to_player[number]

# Przenieść wszystkie printy do interfejsu
# Dodać wyświetlanie pionków, które pozostały do umieszczenie i które zostały zbite


def setting_pawns_phase(board: Board) -> None:
    print_empty_lines(1)
    first_player_pawns_no = board.pawns_number().value
    second_player_pawns_no = board.pawns_number().value
    while first_player_pawns_no > 0 or second_player_pawns_no > 0:
        set_pawn_by_player(board, board.starting_player())
        first_player_pawns_no -= 1
        print_board(board)
        set_pawn_by_player(board, OTHER_PLAYER[board.starting_player()])
        second_player_pawns_no -= 1
        print_board(board)


def moving_pawns_phase(board: Board):
    print_empty_lines(1)
    while is_game_still_played(board):
        move_pawn_by_player(board, board.starting_player())
        print_board(board)
        move_pawn_by_player(board, OTHER_PLAYER[board.starting_player()])
        print_board(board)

# TODO


def is_game_still_played(board: Board) -> bool:
    return True


def set_pawn_by_player(board: Board, player: Player):
    print_before_move(player)
    print_pawns_left(board, player)
    field = get_field_condition_field_is_free(
        board, "Where do you want to add your pawn: ")
    board.add_pawn(field, player)
    player_with_mill = check_mill(board, field)
    if player_with_mill is not None:
        print_board(board)
        after_mill_occured(board, player_with_mill)
    print_empty_lines(1)


def get_field_condition_field_is_free(board: Board, message: str) -> Field:
    # Czy tu nie będzie nieskończonej pętli kiedyś?
    while True:
        id = get_user_input(message).upper()
        if id in FIELD_IDS:
            field = board.field_by_id(id)
            if board.is_field_free(field):
                return field
            else:
                print_field_occupied()
        else:
            print_improper_id()


def get_field_condition_proper_player(board: Board, player: Player, message: str) -> Field:
    while True:
        id = get_user_input(message).upper()
        if id in FIELD_IDS:
            field = board.field_by_id(id)
            if field.player() == player:
                return field
            elif field.player() is None:
                print_no_pawn()
            else:
                print_not_your_pawn()
        else:
            print_improper_id()


def move_pawn_by_player(board: Board, player: Player) -> None:
    print_before_move(player)
    # Podpowiedzi jakie na jakie pola można się ruszyć swoim pionkiem
    curr_field = get_field_condition_proper_player(
        board, player, "Which pawn do you want to move? Enter field id: ")
    new_field = get_field_condition_field_is_free(
        board, "Where do you want to move your pawn? Enter field id: ")
    board.move_pawn(curr_field, new_field, player)
    player_with_mill = check_mill(board, new_field)
    if player_with_mill is not None:
        print_board(board)
        after_mill_occured(board, player_with_mill)
    print()


"""
Checks if last move created a mill
"""


def check_mill(board: Board, field: Field):
    if field.coordiantes().position_top_middle_bottom() == pos.MIDDLE or field.coordiantes().position_left_center_right() == pos.CENTER:
        fields_to_check = []
        for square in pos_sq:
            found_field = board.field_by_positions(square, field.coordiantes(
            ).position_top_middle_bottom(), field.coordiantes().position_left_center_right())
            fields_to_check.append(found_field)
        if all([field.player() == check_field.player() for check_field in fields_to_check]):
            return field.player()
    if field.coordiantes().position_left_center_right() in [pos.LEFT, pos.RIGHT]:
        fields_to_check = []
        for position in [pos.TOP, pos.MIDDLE, pos.BOTTOM]:
            found_field = board.field_by_positions(field.coordiantes().square(
            ), position, field.coordiantes().position_left_center_right())
            fields_to_check.append(found_field)
        if all([field.player() == check_field.player() for check_field in fields_to_check]):
            return field.player()
    if field.coordiantes().position_top_middle_bottom() in [pos.TOP, pos.BOTTOM]:
        fields_to_check = []
        for position in [pos.LEFT, pos.CENTER, pos.RIGHT]:
            found_field = board.field_by_positions(field.coordiantes().square(
            ), field.coordiantes().position_top_middle_bottom(), position)
            fields_to_check.append(found_field)
        if all([field.player() == check_field.player() for check_field in fields_to_check]):
            return field.player()


def after_mill_occured(board: Board, player: Player):
    print_mill_occurred()
    while True:
        field_id = get_user_input(
            "Which pawn would you like to remove? Enter field id: ").upper()
        if field_id in FIELD_IDS:
            if board.field_by_id(field_id).player() is None:
                print_no_pawn()
            elif board.field_by_id(field_id).player() == player:
                print("You cannot remove your own pawn")
            else:
                break
        else:
            print_improper_id()
    board.remove_pawn(board.field_by_id(field_id))


def get_user_input(message):
    return input(message)


def choose_mode() -> PawnsNumber:
    print_choose_mode()
