import random
from traceback import print_last
from typing import List, Tuple

# https://realpython.com/absolute-vs-relative-python-imports/
# Upewnić się czy importy w ten sposób są okej
from .board import FIELD_IDS, Board
from .bot import move_pawn_by_bot, set_pawn_by_bot
from .enums import BotLvl, PawnsNumber, Player
from .enums import Position as pos
from .enums import PositionSquare as pos_sq
from .field import Field
from .interface import (OTHER_PLAYER, print_before_move, print_blank_lines,
                        print_board, print_choose_against_who,
                        print_choose_pawns_number, print_field_occupied,
                        print_improper_id, print_last_move, print_last_remove, print_last_set, print_mill_occurred, print_no_pawn,
                        print_not_your_pawn, print_pawns_left,
                        print_possible_moves, print_remove_own_pawn,
                        print_starting_player,
                        print_transition_to_moving_phase, print_welcome, print_winner)

STR_TO_PAWNS_NUMBER = {"9": PawnsNumber.NINE, "3": PawnsNumber.THREE,
                       "6": PawnsNumber.SIX, "12": PawnsNumber.TWELVE}
STR_TO_BOT_LVL = {False: BotLvl.OFF, "e": BotLvl.EASY,
                  "easy": BotLvl.EASY, "h": BotLvl.HARD, "hard": BotLvl.HARD}

# Podwójny młynek -DONE
# Koniec gry, gdy nie ma żadnego dostępnego ruchu - DONE
# Koniec gry, gdy zostaną dwa - DONE
# Remis, gdy trzykrotnie powtórzy się sytuacja na planszy
# Gdy graczowi zostaną trzy pionki może poruszać się swoimi pionkami na dowolne pola
# Brak młynka przez 50 ruchów to remis


def main(args) -> None:
    print_welcome()
    print_blank_lines(2)
    # pawns_number = choose_pawns_number()  # Zwróci liczbę pionków
    # print_blank_lines(2)
    # choose_against_who()
    board = Board(STR_TO_PAWNS_NUMBER[args.pawns_number])
    board.set_bot(STR_TO_BOT_LVL[args.bot])
    print_board(board)
    start_game(board)


def start_game(board: Board) -> None:
    starting_player = get_starting_player()
    board.set_starting_player(starting_player)
    print_starting_player(starting_player)
    setting_pawns_phase(board)
    print_transition_to_moving_phase()
    moving_pawns_phase(board)


def get_starting_player() -> None:
    num_to_player = {1: Player.FIRST, 2: Player.SECOND}
    number = random.randint(1, 2)
    return num_to_player[number]

# Przenieść wszystkie printy do interfejsu - DONE
# Dodać wyświetlanie pionków, które pozostały do umieszczenie i które zostały zbite - DONE


def setting_pawns_phase(board: Board) -> None:
    print_blank_lines(1)
    # Można by jakoś poprawić tę ilość pionków
    first_player_pawns_no = board.pawns_number().value
    second_player_pawns_no = board.pawns_number().value
    while first_player_pawns_no > 0 or second_player_pawns_no > 0:
        # Bot zawsze będzie drugim graczem
        if board.bot and board.starting_player() == Player.SECOND:
            set_pawn_by_bot(board)
        else:
            set_pawn_by_player(board, board.starting_player(),
                               first_player_pawns_no)
        first_player_pawns_no -= 1
        if board.bot and OTHER_PLAYER[board.starting_player()] == Player.SECOND:
            set_pawn_by_bot(board)
        else:
            set_pawn_by_player(
                board, OTHER_PLAYER[board.starting_player()], second_player_pawns_no)
        second_player_pawns_no -= 1


def set_pawn_by_player(board: Board, player: Player, pawns_in_hand: int) -> None:
    print_before_move(player)
    print_board(board)
    print_pawns_left(board, player, pawns_in_hand)
    field = get_field_condition_field_is_free(
        board, "Where do you want to add your pawn: ")
    board.add_pawn(field, player)
    print_board(board)
    print_last_set(field.id())
    player_with_mill, mill_num = check_mill(board, field)
    # if player_with_mill is not None:
    #     print_board(board)
    #     remove_opponents_pawn(board, player_with_mill)
    if mill_num > 0:
        print_mill_occurred(mill_num)
    for _ in range(mill_num):
        remove_opponents_pawn(board, player_with_mill)
    print_blank_lines(1)

# Dodać wyświetlanie jaki był ostatni wykonany ruch


def moving_pawns_phase(board: Board) -> None:
    print_blank_lines(1)
    while is_game_still_played(board):
        if board.bot and board.starting_player() == Player.SECOND:
            move_pawn_by_bot(board)
        else:
            move_pawn_by_player(board, board.starting_player())
        if not is_game_still_played(board):
            break

        if board.bot and OTHER_PLAYER[board.starting_player()] == Player.SECOND:
            move_pawn_by_bot(board)
        else:
            move_pawn_by_player(board, OTHER_PLAYER[board.starting_player()])
    # TODO
    check_winner()


def move_pawn_by_player(board: Board, player: Player) -> None:
    print_before_move(player)
    print_board(board)
    # Podpowiedzi jakie na jakie pola można się ruszyć swoim pionkiem - DONE
    while True:
        curr_field = get_field_condition_proper_player(
            board, player, "Which pawn do you want to move? Enter field id: ")

        # Dodatkowo sprawdzić czy pola z którymi jest połączenie są zajęte - DONE
        # Anulowanie wyboru danego pola - DONE
        # Od razu blokowanie wykonania ruchu jeżeli nie ma żadnego wolnego pola dookoła -DONE
        moves = possible_moves(board, curr_field)
        if not moves:
            print("There is no possible move with this pawn")
            continue
            # Coś, żeby wybrać jeszcze raz - DONE

        print_possible_moves(moves)

        new_field = get_field_condition_free_and_connection(
            board, curr_field, "Where do you want to move your pawn? Enter field id: ")
        if new_field is not None:
            break

    board.move_pawn(curr_field, new_field, player)
    print_board(board)
    print_last_move(curr_field.id(), new_field.id())
    # Jeżeli nie został wykonany ruch no to nie sprawdza młynka - DONE
    player_with_mill, mill_num = check_mill(board, new_field)
    if mill_num > 0:
        print_mill_occurred(mill_num)
    for _ in range(mill_num):
        remove_opponents_pawn(board, player_with_mill)
    print_blank_lines(1)


def get_field_condition_free_and_connection(board: Board, curr_field: Field, message: str) -> Field:
    while True:
        field = get_field_condition_field_is_free(board, message)
        if field is None:
            return None
        if field.id() in curr_field.connections():
            return field
        else:
            print("There is no connection beetween these fields")


def get_field_condition_field_is_free(board: Board, message: str) -> Field:
    # Czy tu nie będzie nieskończonej pętli kiedyś? - RACZEJ NIE
    while True:
        id = get_user_input(message).upper()
        if id == "`":
            return None
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


def is_game_still_played(board: Board) -> bool:
    if board.player_pawns_number(Player.FIRST) <= 2 or board.player_pawns_number(Player.SECOND) <= 2:
        return False
    # Koniec gry również gdy nie można wykonać żadnego ruchu
    # Gdy będzie faza latania to może wykonać każdy ruch
    if not check_is_any_possible_move(board, Player.FIRST) or not check_is_any_possible_move(board, Player.SECOND):
        return False
    # TODO
    if check_is_draw():
        return False
    return True


def check_is_any_possible_move(board: Board, player: Player) -> bool:
    for field in board.get_all_player_fields(player):
        for connection in field.connections():
            connection_field = board.field_by_id(connection)
            if board.is_field_free(connection_field):
                return True
    return False


def check_is_draw():
    return False


"""
Checks if last move created a mill
"""

# Czy tu na pewno jest potrzeba zwracania tego playera


def check_mill(board: Board, field: Field) -> Tuple[Player, int]:
    mills_num = 0
    if field.coordiantes().position_top_middle_bottom() == pos.MIDDLE or field.coordiantes().position_left_center_right() == pos.CENTER:
        fields_to_check = []
        for square in pos_sq:
            found_field = board.field_by_positions(square, field.coordiantes(
            ).position_top_middle_bottom(), field.coordiantes().position_left_center_right())
            fields_to_check.append(found_field)
        if all([field.player() == check_field.player() for check_field in fields_to_check]):
            # return field.player()
            mills_num += 1
    if field.coordiantes().position_left_center_right() in [pos.LEFT, pos.RIGHT]:
        fields_to_check = []
        for position in [pos.TOP, pos.MIDDLE, pos.BOTTOM]:
            found_field = board.field_by_positions(field.coordiantes().square(
            ), position, field.coordiantes().position_left_center_right())
            fields_to_check.append(found_field)
        if all([field.player() == check_field.player() for check_field in fields_to_check]):
            # return field.player()
            mills_num += 1
    if field.coordiantes().position_top_middle_bottom() in [pos.TOP, pos.BOTTOM]:
        fields_to_check = []
        for position in [pos.LEFT, pos.CENTER, pos.RIGHT]:
            found_field = board.field_by_positions(field.coordiantes().square(
            ), field.coordiantes().position_top_middle_bottom(), position)
            fields_to_check.append(found_field)
        if all([field.player() == check_field.player() for check_field in fields_to_check]):
            # return field.player()
            mills_num += 1
    if mills_num == 0:
        return (None, mills_num)
    return (field.player(), mills_num)


def remove_opponents_pawn(board: Board, player: Player) -> None:
    while True:
        field_id = get_user_input(
            "Which pawn would you like to remove? Enter field id: ").upper()
        if field_id in FIELD_IDS:
            if board.field_by_id(field_id).player() is None:
                print_no_pawn()
            elif board.field_by_id(field_id).player() == player:
                print_remove_own_pawn()
            else:
                break
        else:
            print_improper_id()
    board.remove_pawn(board.field_by_id(field_id))
    print_board(board)
    print_last_remove(field_id)


def possible_moves(board: Board, field: Field) -> List[str]:
    result = []
    for conenction in field.connections():
        if board.field_by_id(conenction).player() is None:
            result.append(conenction)
    return result


def check_winner() -> Player:
    print_winner()


def get_user_input(message):
    return input(message)


# def choose_pawns_number() -> PawnsNumber:
#     print_choose_pawns_number()
#     while True:
#         mode = get_user_input("Which mode do you choose? Enter mode number: ")
#         if mode in ["1", "2", "3", "4"]:
#             break
#         elif mode in ["6", "9", "12"]:
#             print("\nPlease enter mode number (1/2/3/4), not the number of pawns")
#         else:
#             print("\nPlease enter proper mode number (1/2/3/4)")
#     return MODE_TO_PAWNS_NUMBER[mode]


# def choose_against_who():
#     print_choose_against_who()
#     while True:
#         mode = get_user_input("Which mode do you choose? Enter mode number: ")
#         if mode in ["1", "2"]:
#             return mode
#         else:
#             print("\nPlease enter proper mode number (1/2)")
