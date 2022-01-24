
import random
from turtle import position
from typing import List, Tuple

from PySide2 import sys

# https://realpython.com/absolute-vs-relative-python-imports/
# Upewnić się czy importy w ten sposób są okej
from .board import FIELD_IDS, Board
from .bot import move_pawn_by_bot, set_pawn_by_bot
from .consts import (CANCEL_KEY, MOVES_TO_DRAW, NUM_TO_PLAYER, OTHER_PLAYER,
                     POS_LCR_INDEX, POS_LCR_LIST, POS_SQ_INDEX, POS_TMB_INDEX,
                     POS_TMB_LIST, STR_TO_BOT_LVL, STR_TO_PAWNS_NUMBER,
                     WHERE_ADD_PAWN, WHERE_MOVE_PAWN, WHICH_PAWN_MOVE, WHICH_PAWN_REMOVE)
from .coordinates import Coordinates
from .enums import BotLvl, PawnsNumber, Player
from .enums import Position as pos
from .enums import PositionSquare as pos_sq
from .field import Field
from .interface import (get_user_input, print_before_move, print_blank_lines,
                        print_board, print_cancel_move, print_draw,
                        print_field_occupied, print_game_over,
                        print_improper_id, print_last_move, print_last_remove,
                        print_last_set, print_mill_occurred,
                        print_move_canceled, print_no_connection,
                        print_no_pawn, print_no_possible_move,
                        print_not_your_pawn, print_pawns_left,
                        print_possible_moves, print_remove_own_pawn,
                        print_starting_player,
                        print_transition_to_moving_phase, print_welcome,
                        print_winner)

# Podwójny młynek -DONE
# Koniec gry, gdy nie ma żadnego dostępnego ruchu - DONE
# Koniec gry, gdy zostaną dwa - DONE
# Remis, gdy trzykrotnie powtórzy się sytuacja na planszy
# Gdy graczowi zostaną trzy pionki może poruszać się swoimi pionkami na dowolne pola
# Brak młynka przez 40 ruchów to remis - DONE


def main(args) -> None:
    """
    Main function, game logic starts here
    Introduction is printed, and board instance is created
    """

    print_welcome()
    print_blank_lines(2)
    pawns_number = STR_TO_PAWNS_NUMBER[args.pawns_number]
    bot_lvl = STR_TO_BOT_LVL[args.bot]
    board = Board(pawns_number, bot_lvl, args.delay)
    print_board(board)
    start_game(board)


def start_game(board: Board) -> None:
    """Calls draw starting player and functions for next phases of the game"""

    draw_starting_player(board)
    print_blank_lines(1)
    setting_pawns_phase(board)
    print_transition_to_moving_phase()
    print_blank_lines(1)
    moving_pawns_phase(board)


def draw_starting_player(board: Board) -> None:
    """Draw starting player and sets it in board"""

    number = random.randint(1, 2)
    board.set_starting_player(NUM_TO_PLAYER[number])
    print_starting_player(NUM_TO_PLAYER[number])

# Przenieść wszystkie printy do interfejsu - DONE
# Dodać wyświetlanie pionków, które pozostały do umieszczenie i które zostały zbite - DONE


def setting_pawns_phase(board: Board) -> None:
    """
    Calls fucntions to set pawn either by player or bot
    Continues until all pawns for each player are set or game is over
    """

    # Można by jakoś poprawić tę ilość pionków
    pawns_number = board.pawns_number().value
    pawns_in_hand = {
        Player.ONE: pawns_number, Player.TWO: pawns_number}
    first_player = board.starting_player()
    second_player = OTHER_PLAYER[first_player]
    while pawns_in_hand[first_player] > 0 or pawns_in_hand[second_player] > 0:
        # Bot zawsze będzie drugim graczem
        if board.bot() != BotLvl.OFF and first_player == Player.TWO:
            set_pawn_by_bot(board)
        else:
            set_pawn_by_player(board, first_player,
                               pawns_in_hand[first_player])
        pawns_in_hand[first_player] -= 1

        if not is_game_still_played(board, pawns_in_hand):
            game_over(board)

        if board.bot() != BotLvl.OFF and second_player == Player.TWO:
            set_pawn_by_bot(board)
        else:
            set_pawn_by_player(board, second_player,
                               pawns_in_hand[second_player])
        pawns_in_hand[second_player] -= 1

    if not is_game_still_played(board, pawns_in_hand):
        game_over(board)


def set_pawn_by_player(board: Board, player: Player, pawns_in_hand: int) -> None:
    """
    Asks player where to add pawn, checks if it is proper action,
    then sets pawn and checks if mill occured
    """

    print_before_move(player)
    print_board(board)
    print_pawns_left(board, player, pawns_in_hand)

    field = get_free_field(board, WHERE_ADD_PAWN)
    board.add_pawn(field, player)

    print_board(board)
    print_last_set(field.id())

    player_with_mill, mill_num = check_mill(board, field)

    if mill_num > 0:
        print_mill_occurred(mill_num)
        board.reset_moves_without_mill()
    else:
        board.add_one_move_without_mill()
    for _ in range(mill_num):
        remove_opponents_pawn(board, player_with_mill)

# Dodać wyświetlanie jaki był ostatni wykonany ruch - DONE


def moving_pawns_phase(board: Board) -> None:
    """
    Calls fucntions to move pawn either by player or bot
    Continues until game is over
    """

    first_player = board.starting_player()
    second_player = OTHER_PLAYER[first_player]
    while is_game_still_played(board):
        if board.bot() != BotLvl.OFF and first_player == Player.TWO:
            move_pawn_by_bot(board)
        else:
            move_pawn_by_player(board, first_player)

        if not is_game_still_played(board):
            break

        if board.bot() and second_player == Player.TWO:
            move_pawn_by_bot(board)
        else:
            move_pawn_by_player(board, second_player)

    game_over(board)


def move_pawn_by_player(board: Board, player: Player) -> None:
    """
    Asks player which pawn move and where, checks if it is proper action,
    then moves pawn and checks if mill occured
    """

    print_before_move(player)
    print_board(board)
    # Podpowiedzi jakie na jakie pola można się ruszyć swoim pionkiem - DONE
    while True:
        curr_field = get_players_field(board, player, WHICH_PAWN_MOVE)

        # Dodatkowo sprawdzić czy pola z którymi jest połączenie są zajęte - DONE
        # Anulowanie wyboru danego pola - DONE
        # Od razu blokowanie wykonania ruchu jeżeli nie ma żadnego wolnego pola dookoła -DONE
        moves = possible_moves(board, curr_field)
        if not moves:
            print_no_possible_move()
            continue
            # Coś, żeby wybrać jeszcze raz - DONE

        print_possible_moves(moves)
        print_cancel_move()
        new_field = get_free_field_with_connection(
            board, curr_field, WHERE_MOVE_PAWN)
        if new_field is not None:
            break

    board.move_pawn(curr_field, new_field, player)
    print_board(board)
    print_last_move(curr_field.id(), new_field.id())
    # Jeżeli nie został wykonany ruch no to nie sprawdza młynka - DONE
    player_with_mill, mill_num = check_mill(board, new_field)
    if mill_num > 0:
        print_mill_occurred(mill_num)
        board.reset_moves_without_mill()
    else:
        board.add_one_move_without_mill()
    for _ in range(mill_num):
        remove_opponents_pawn(board, player_with_mill)


def remove_opponents_pawn(board: Board, player: Player) -> None:
    """
    Asks player which pawn remove,
    checks if it is proper action, then removes it
    """

    while True:
        field_id = get_user_input(WHICH_PAWN_REMOVE).upper()
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


def get_free_field_with_connection(board: Board, curr_field: Field, message: str) -> Field:
    """
    Asks user for field id until user enters field
    which is free and has connection with current field
    """

    while True:
        field = get_free_field(board, message)
        if field is None:
            return None
        if field.id() in curr_field.connections():
            return field
        else:
            print_no_connection()


def get_free_field(board: Board, message: str) -> Field:
    """Asks user for field id until user enters field which is free"""

    while True:
        id = get_user_input(message).upper()
        if id == CANCEL_KEY:
            print_move_canceled()
            return None
        if id in FIELD_IDS:
            field = board.field_by_id(id)
            if board.is_field_free(field):
                return field
            else:
                print_field_occupied()
        else:
            print_improper_id()


def get_players_field(board: Board, player: Player, message: str) -> Field:
    """Asks user for field id until user enters his field """

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


def is_game_still_played(board: Board, player_pawns_in_hand={Player.ONE: 0, Player.TWO: 0}) -> bool:
    """Checks conditions if game should be continued or not"""

    pawns_on_field_one = board.player_pawns_number(Player.ONE)
    player_one_pawns_no = pawns_on_field_one + player_pawns_in_hand[Player.ONE]
    pawns_on_field_two = board.player_pawns_number(Player.TWO)
    player_two_pawns_no = pawns_on_field_two + player_pawns_in_hand[Player.TWO]

    if player_one_pawns_no <= 2 or player_two_pawns_no <= 2:
        return False
    # Koniec gry również gdy nie można wykonać żadnego ruchu
    # Gdy będzie faza latania to może wykonać każdy ruch
    if is_draw(board, player_pawns_in_hand):
        return False
    if not is_any_possible_move(board, Player.ONE) and player_pawns_in_hand[Player.ONE] == 0 or not is_any_possible_move(board, Player.TWO) and player_pawns_in_hand[Player.TWO] == 0:
        return False
    return True


def is_any_possible_move(board: Board, player: Player) -> bool:
    """Checks if given player can make any move or not"""

    for field in board.get_all_player_fields(player):
        for connection in field.connections():
            connection_field = board.field_by_id(connection)
            if board.is_field_free(connection_field):
                return True
    return False


def is_draw(board: Board, player_pawns_in_hand={Player.ONE: 0, Player.TWO: 0}):
    """Checks if draw occured or not"""

    pawns_on_field_one = board.player_pawns_number(Player.ONE)
    player_one_pawns_no = pawns_on_field_one + player_pawns_in_hand[Player.ONE]
    pawns_on_field_two = board.player_pawns_number(Player.TWO)
    player_two_pawns_no = pawns_on_field_two + player_pawns_in_hand[Player.TWO]

    if player_one_pawns_no == player_two_pawns_no and not is_any_possible_move(board, Player.ONE) and not is_any_possible_move(board, Player.TWO):
        return True
    return True if board.moves_without_mill() >= MOVES_TO_DRAW else False


def check_mill(board: Board, field: Field) -> Tuple[Player, int]:
    """Checks if last action created a mill"""

    mills_num = 0
    field_position_tmb = field.coordiantes().position_top_middle_bottom()
    field_position_lcr = field.coordiantes().position_left_center_right()
    field_all_positions = list(field.coordiantes().get_all_coordinates())

    if board.pawns_number() == PawnsNumber.THREE:
        return _check_mill_three_pawns(board, field)

    if board.pawns_number() != PawnsNumber.SIX:
        if field_position_tmb == pos.MIDDLE or field_position_lcr == pos.CENTER:
            mills_num += _check_mill_loop(board, field,
                                          field_all_positions, pos_sq, POS_SQ_INDEX)

    if field_position_lcr in [pos.LEFT, pos.RIGHT]:
        mills_num += _check_mill_loop(board, field,
                                      field_all_positions, POS_TMB_LIST, POS_TMB_INDEX)

    if field_position_tmb in [pos.TOP, pos.BOTTOM]:
        mills_num += _check_mill_loop(board, field,
                                      field_all_positions, POS_LCR_LIST, POS_LCR_INDEX)

    if board.pawns_number() == PawnsNumber.TWELVE:
        if (field_position_tmb, field_position_lcr) in [(pos.TOP, pos.LEFT), (pos.TOP, pos.RIGHT), (pos.BOTTOM, pos.LEFT), (pos.BOTTOM, pos.RIGHT)]:
            mills_num += _check_mill_loop(board, field,
                                          field_all_positions, pos_sq, POS_SQ_INDEX)

    if mills_num == 0:
        return (None, mills_num)
    return (field.player(), mills_num)


def _check_mill_three_pawns(board: Board, field: Field):
    """Checks if last action created a mill for three pawns board"""

    mills_num = 0
    for position_tmb in POS_TMB_LIST:
        positions = [pos_sq.MIDDLE, position_tmb, None]
        mills_num += _check_mill_loop(board, field,
                                      positions, POS_LCR_LIST, POS_LCR_INDEX)

    for position_lcr in POS_LCR_LIST:
        positions = [pos_sq.MIDDLE, None, position_lcr]
        mills_num += _check_mill_loop(board, field,
                                      positions, POS_TMB_LIST, POS_TMB_INDEX)

    mills_num += _check_mill_zip_loop(board, field, pos_sq.MIDDLE,  zip(
        POS_TMB_LIST, POS_LCR_LIST))

    mills_num += _check_mill_zip_loop(board, field, pos_sq.MIDDLE, zip(
        reversed(POS_TMB_LIST), POS_LCR_LIST))

    return (field.player(), mills_num)


def _check_mill_loop(board: Board, field: Field, positions, loop_list,  index):
    """Iterates for given list and looks for mills"""

    fields_to_check = []
    for element in loop_list:
        positions[index] = element
        coord = Coordinates(positions[0], positions[1], positions[2])
        found_field = board.field_by_positions(coord)
        fields_to_check.append(found_field)
    return _check_mill_condition(field, fields_to_check)


def _check_mill_zip_loop(board: Board, field: Field, square, loop_list):
    """Iterates for given zipped lists and looks for mills"""

    fields_to_check = []
    for position_tmb, position_lcr in loop_list:
        coord = Coordinates(square, position_tmb, position_lcr)
        found_field = board.field_by_positions(coord)
        fields_to_check.append(found_field)
    return _check_mill_condition(field, fields_to_check)


def _check_mill_condition(field: Field, fields_to_check: List[Field]):
    """Checks are three pawns in row and mill occured or not"""

    if all([field.player() == check_field.player() for check_field in fields_to_check]):
        return 1
    return 0


def possible_moves(board: Board, field: Field) -> List[str]:
    """Returns all possible moves from given field"""

    field_ids = []
    for conenction in field.connections():
        if board.field_by_id(conenction).player() is None:
            field_ids.append(conenction)
    return field_ids


def game_over(board: Board):
    """Called when game isn't continued, choose winner and then exit program"""

    print_game_over()
    choose_winner(board)
    sys.exit()


def choose_winner(board: Board) -> None:
    """Checks who is the winner or if draw occured"""

    if is_draw(board):
        print_draw()
    else:
        if board.player_pawns_number(Player.ONE) <= 2 or not is_any_possible_move(board, Player.ONE):
            winner = Player.TWO
        elif board.player_pawns_number(Player.TWO) <= 2 or not is_any_possible_move(board, Player.TWO):
            winner = Player.ONE
        print_winner(winner)
