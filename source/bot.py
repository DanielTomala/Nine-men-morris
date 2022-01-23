import collections
from random import choice
from time import sleep

from .interface import print_before_move, print_before_move_bot, print_board, print_bot_mill_occurred, print_last_move, print_last_remove, print_last_set

from .board import Board
from .enums import BotLvl, Player
import source.game_logic as gl


def set_pawn_by_bot(board: Board):
    print_before_move_bot()
    if board.bot() == BotLvl.EASY:
        _set_pawn_by_bot_easy(board)
    elif board.bot() == BotLvl.HARD:
        _set_pawn_by_bot_hard(board)
    sleep(3)


def move_pawn_by_bot(board: Board):
    print_before_move_bot()
    if board.bot() == BotLvl.EASY:
        _move_pawn_by_bot_easy(board)
    elif board.bot() == BotLvl.HARD:
        _move_pawn_by_bot_hard(board)
    sleep(3)


def _set_pawn_by_bot_easy(board: Board):
    field = choice(board.get_all_free_fields())
    board.add_pawn(field, Player.SECOND)
    print_board(board)
    print_last_set(field.id())
    player_with_mill, mill_num = gl.check_mill(board, field)
    if mill_num > 0:
        print_bot_mill_occurred(mill_num)
    for _ in range(mill_num):
        _remove_opponents_pawn_by_bot_easy(board)


def _move_pawn_by_bot_easy(board: Board):
    all_possible_moves = []
    for curr_field in board.get_all_player_fields(Player.SECOND):
        for new_field_id in gl.possible_moves(board, curr_field):
            all_possible_moves.append(
                (curr_field, board.field_by_id(new_field_id)))
    final_move = choice(all_possible_moves)
    board.move_pawn(final_move[0], final_move[1], Player.SECOND)
    print_board(board)
    print_last_move(final_move[0].id(), final_move[1].id())
    player_with_mill, mill_num = gl.check_mill(board, final_move[1])
    if mill_num > 0:
        print_bot_mill_occurred(mill_num)
    for _ in range(mill_num):
        _remove_opponents_pawn_by_bot_easy(board)

# Bot próbuje postawić pionek na polu sąsiadującym z obecnie już postawionym
# W pierwszej kolejności wybierane są pola w pobliżu których jest najwięcej innych pionków


def _set_pawn_by_bot_hard(board: Board):
    all_posible_sets = []
    for curr_field in board.get_all_player_fields(Player.SECOND):
        for new_field_id in gl.possible_moves(board, curr_field):
            all_posible_sets.append(board.field_by_id(new_field_id))
    fields_occurences = collections.Counter(all_posible_sets)
    if fields_occurences:
        max_occurences = max(fields_occurences.values())
        # Żeby się choice nie wywalił dla pustej listy
        # final_moves = [
        #     key for dict in fields_occurences if val == max_occurences]
        final_moves = [key for key in fields_occurences.keys(
        ) for val in fields_occurences.values() if val == max_occurences]
        field = choice(final_moves)
        board.add_pawn(field, Player.SECOND)
        print_board(board)
        print_last_set(field.id())
        player_with_mill, mill_num = gl.check_mill(board, field)
        if mill_num > 0:
            print_bot_mill_occurred(mill_num)
        for _ in range(mill_num):
            _remove_opponents_pawn_by_bot_hard(board)

    else:
        _set_pawn_by_bot_easy(board)


# Rusza się tak, żeby powstał młynek
def _move_pawn_by_bot_hard(board: Board):
    all_possible_moves = []
    for curr_field in board.get_all_player_fields(Player.SECOND):
        for new_field_id in gl.possible_moves(board, curr_field):
            all_possible_moves.append(
                (curr_field, board.field_by_id(new_field_id)))
    # TODO Sprawdzenie keidy wystąpi młynek

    final_move = choice(all_possible_moves)
    board.move_pawn(final_move[0], final_move[1], Player.SECOND)
    print_board(board)
    print_last_move(final_move[0].id(), final_move[1].id())
    player_with_mill, mill_num = gl.check_mill(board, final_move[1])
    if mill_num > 0:
        print_bot_mill_occurred(mill_num)
    for _ in range(mill_num):
        _remove_opponents_pawn_by_bot_hard(board)


def _remove_opponents_pawn_by_bot_easy(board: Board):
    all_opponents_fields = board.get_all_player_fields(Player.FIRST)
    field = choice(all_opponents_fields)
    board.remove_pawn(field)
    print_board(board)
    print_last_remove(field.id())


def _remove_opponents_pawn_by_bot_hard(board: Board):
    # Usuwa gdy więcej niż jeden w linii
    all_opponents_fields = board.get_all_player_fields(Player.FIRST)
    field = choice(all_opponents_fields)
    board.remove_pawn(field)
    print_board(board)
    print_last_remove(field.id())
