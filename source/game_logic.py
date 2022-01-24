
import random
from typing import List, Tuple

# https://realpython.com/absolute-vs-relative-python-imports/
# Upewnić się czy importy w ten sposób są okej
from .board import FIELD_IDS, Board
from .bot import move_pawn_by_bot, set_pawn_by_bot
from .consts import (NUM_TO_PLAYER, OTHER_PLAYER, POS_LCR_LIST, POS_TMB_LIST, STR_TO_BOT_LVL,
                     STR_TO_PAWNS_NUMBER, OTHER_PLAYER)
from .coordinates import Coordinates
from .enums import BotLvl, PawnsNumber, Player
from .enums import Position as pos
from .enums import PositionSquare as pos_sq
from .field import Field
from .interface import (print_before_move, print_blank_lines,
                        print_board, print_field_occupied, print_improper_id,
                        print_last_move, print_last_remove, print_last_set,
                        print_mill_occurred, print_no_pawn,
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
# Brak młynka przez 50 ruchów to remis


def main(args) -> None:
    """
    Main function, game starts here
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
    draw_starting_player(board)
    setting_pawns_phase(board)
    print_transition_to_moving_phase()
    moving_pawns_phase(board)


def draw_starting_player(board: Board) -> None:
    """Draw starting player and sets it in board"""

    number = random.randint(1, 2)
    board.set_starting_player(NUM_TO_PLAYER[number])
    print_starting_player(NUM_TO_PLAYER[number])

# Przenieść wszystkie printy do interfejsu - DONE
# Dodać wyświetlanie pionków, które pozostały do umieszczenie i które zostały zbite - DONE


def setting_pawns_phase(board: Board) -> None:
    """Continues until all pawns for each player are set"""

    print_blank_lines(1)
    # Można by jakoś poprawić tę ilość pionków
    player_one_pawns_no = board.pawns_number().value
    player_two_pawns_no = board.pawns_number().value
    while player_one_pawns_no > 0 or player_two_pawns_no > 0:
        # Bot zawsze będzie drugim graczem
        if board.bot and board.starting_player() == Player.TWO:
            set_pawn_by_bot(board)
        else:
            set_pawn_by_player(board, board.starting_player(),
                               player_one_pawns_no)
        player_one_pawns_no -= 1
        if board.bot and OTHER_PLAYER[board.starting_player()] == Player.TWO:
            set_pawn_by_bot(board)
        else:
            set_pawn_by_player(
                board, OTHER_PLAYER[board.starting_player()], player_two_pawns_no)
        player_two_pawns_no -= 1


def set_pawn_by_player(board: Board, player: Player, pawns_in_hand: int) -> None:
    print_before_move(player)
    print_board(board)
    print_pawns_left(board, player, pawns_in_hand)
    field = get_free_field(
        board, "Where do you want to add your pawn: ")
    board.add_pawn(field, player)
    print_board(board)
    print_last_set(field.id())
    player_with_mill, mill_num = check_mill(board, field)

    if mill_num > 0:
        print_mill_occurred(mill_num)
    for _ in range(mill_num):
        remove_opponents_pawn(board, player_with_mill)
    print_blank_lines(1)

# Dodać wyświetlanie jaki był ostatni wykonany ruch - DONE


def moving_pawns_phase(board: Board) -> None:
    print_blank_lines(1)
    while is_game_still_played(board):
        if board.bot() and board.starting_player() == Player.TWO:
            move_pawn_by_bot(board)
        else:
            move_pawn_by_player(board, board.starting_player())
        if not is_game_still_played(board):
            break

        if board.bot() and OTHER_PLAYER[board.starting_player()] == Player.TWO:
            move_pawn_by_bot(board)
        else:
            move_pawn_by_player(board, OTHER_PLAYER[board.starting_player()])

    check_winner(board)


def move_pawn_by_player(board: Board, player: Player) -> None:
    print_before_move(player)
    print_board(board)
    # Podpowiedzi jakie na jakie pola można się ruszyć swoim pionkiem - DONE
    while True:
        curr_field = get_players_field(
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

        new_field = get_free_field_with_connection(
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


def get_free_field_with_connection(board: Board, curr_field: Field, message: str) -> Field:
    while True:
        field = get_free_field(board, message)
        if field is None:
            return None
        if field.id() in curr_field.connections():
            return field
        else:
            print("There is no connection beetween these fields")


def get_free_field(board: Board, message: str) -> Field:
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


def get_players_field(board: Board, player: Player, message: str) -> Field:
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
    if board.player_pawns_number(Player.ONE) <= 2 or board.player_pawns_number(Player.TWO) <= 2:
        return False
    # Koniec gry również gdy nie można wykonać żadnego ruchu
    # Gdy będzie faza latania to może wykonać każdy ruch
    if not is_any_possible_move(board, Player.ONE) or not is_any_possible_move(board, Player.TWO):
        return False
    # TODO
    if check_is_draw():
        return False
    return True


def is_any_possible_move(board: Board, player: Player) -> bool:
    for field in board.get_all_player_fields(player):
        for connection in field.connections():
            connection_field = board.field_by_id(connection)
            if board.is_field_free(connection_field):
                return True
    return False


def check_is_draw():
    return False


def check_mill(board: Board, field: Field) -> Tuple[Player, int]:
    """Checks if last move created a mill"""

    mills_num = 0
    field_position_tmb = field.coordiantes().position_top_middle_bottom()
    field_position_lcr = field.coordiantes().position_left_center_right()
    field_square = field.coordiantes().square()

    if board.pawns_number() == PawnsNumber.THREE:
        return _check_mill_three_pawns(board, field)

    if board.pawns_number() != PawnsNumber.SIX:
        if field_position_tmb == pos.MIDDLE or field_position_lcr == pos.CENTER:
            mills_num += _check_mill_square_loop(
                board, field, field_position_tmb, field_position_lcr)

    if field_position_lcr in [pos.LEFT, pos.RIGHT]:
        mills_num += _check_mill_position_tmb_loop(
            board, field, field_square, field_position_lcr)

    if field_position_tmb in [pos.TOP, pos.BOTTOM]:
        mills_num += _check_mill_position_lcr_loop(
            board, field, field_square, field_position_tmb)

    if board.pawns_number() == PawnsNumber.TWELVE:
        if (field_position_tmb, field_position_lcr) in [(pos.TOP, pos.LEFT), (pos.TOP, pos.RIGHT), (pos.BOTTOM, pos.LEFT), (pos.BOTTOM, pos.RIGHT)]:
            mills_num += _check_mill_square_loop(
                board, field, field_position_tmb, field_position_lcr)

    if mills_num == 0:
        return (None, mills_num)
    return (field.player(), mills_num)


def _check_mill_three_pawns(board: Board, field: Field):
    mills_num = 0
    for position_tmb in POS_TMB_LIST:
        mills_num += _check_mill_position_lcr_loop(
            board, field, pos_sq.MIDDLE, position_tmb)

    for position_lcr in POS_LCR_LIST:
        mills_num += _check_mill_position_tmb_loop(
            board, field, pos_sq.MIDDLE, position_lcr)

    mills_num += _check_mill_zip_loop(board, field, pos_sq.MIDDLE,  zip(
        POS_TMB_LIST, POS_LCR_LIST))

    mills_num += _check_mill_zip_loop(board, field, pos_sq.MIDDLE, zip(
        reversed(POS_TMB_LIST), POS_LCR_LIST))

    return (field.player(), mills_num)


def _check_mill_position_lcr_loop(board: Board, field: Field, square, position_tmb):
    fields_to_check = []
    for position_lcr in POS_LCR_LIST:
        coord = Coordinates(square, position_tmb, position_lcr)
        found_field = board.field_by_positions(coord)
        fields_to_check.append(found_field)
    return _check_mill_condition(field, fields_to_check)


def _check_mill_position_tmb_loop(board: Board, field: Field, square, position_lcr):
    fields_to_check = []
    for position_tmb in POS_TMB_LIST:
        coord = Coordinates(square, position_tmb, position_lcr)
        found_field = board.field_by_positions(coord)
        fields_to_check.append(found_field)
    return _check_mill_condition(field, fields_to_check)


def _check_mill_square_loop(board: Board, field: Field, position_tmb, position_lcr):
    fields_to_check = []
    for square in pos_sq:
        coord = Coordinates(square, position_tmb, position_lcr)
        found_field = board.field_by_positions(coord)
        fields_to_check.append(found_field)
    return _check_mill_condition(field, fields_to_check)


def _check_mill_zip_loop(board: Board, field: Field, square, loop_list):
    fields_to_check = []
    for position_tmb, position_lcr in loop_list:
        coord = Coordinates(square, position_tmb, position_lcr)
        found_field = board.field_by_positions(coord)
        fields_to_check.append(found_field)
    return _check_mill_condition(field, fields_to_check)


def _check_mill_condition(field: Field, fields_to_check: List[Field]):
    if all([field.player() == check_field.player() for check_field in fields_to_check]):
        return 1
    return 0


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


def check_winner(board: Board) -> Player:
    if board.player_pawns_number(Player.ONE) <= 2 or not is_any_possible_move(board, Player.ONE):
        winner = Player.TWO
    elif board.player_pawns_number(Player.TWO) <= 2 or not is_any_possible_move(board, Player.TWO):
        winner = Player.ONE
    print_winner(winner)


def get_user_input(message):
    return input(message)
