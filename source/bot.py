import collections
import copy
from random import choice
from time import sleep

import source.game_logic as gl

from .board import Board
from .enums import BotLvl, Player
from .interface import (print_before_move_bot, print_board,
                        print_bot_mill_occurred, print_last_move,
                        print_last_remove, print_last_set)


def set_pawn_by_bot(board: Board):
    """Calls function to set pawn by bot depending on bot level"""

    print_before_move_bot()
    if board.bot() == BotLvl.EASY:
        _set_pawn_by_bot_easy(board)
    elif board.bot() == BotLvl.HARD:
        _set_pawn_by_bot_hard(board)
    sleep(board.delay())


def move_pawn_by_bot(board: Board):
    """Calls function to move pawn by bot depending on bot level"""

    print_before_move_bot()
    if board.bot() == BotLvl.EASY:
        _move_pawn_by_bot_easy(board)
    elif board.bot() == BotLvl.HARD:
        _move_pawn_by_bot_hard(board)
    sleep(board.delay())


def _set_pawn_by_bot_easy(board: Board):
    """Sets pawn at random field from all available"""

    field = choice(board.get_all_free_fields())
    board.add_pawn(field, Player.TWO)
    print_board(board)
    print_last_set(field.id())
    player_with_mill, mill_num = gl.check_mill(board, field)
    if mill_num > 0:
        print_bot_mill_occurred(mill_num)
        board.reset_moves_without_mill()
    else:
        board.add_one_move_without_mill()
    for _ in range(mill_num):
        _remove_opponents_pawn_by_bot_easy(board)


def _move_pawn_by_bot_easy(board: Board):
    """Makes random move from all available """

    all_possible_moves = []
    for curr_field in board.get_all_player_fields(Player.TWO):
        for new_field_id in gl.possible_moves(board, curr_field):
            all_possible_moves.append(
                (curr_field, board.field_by_id(new_field_id)))
    final_move = choice(all_possible_moves)
    board.move_pawn(final_move[0], final_move[1], Player.TWO)
    print_board(board)
    print_last_move(final_move[0].id(), final_move[1].id())
    player_with_mill, mill_num = gl.check_mill(board, final_move[1])
    if mill_num > 0:
        print_bot_mill_occurred(mill_num)
        board.reset_moves_without_mill()
    else:
        board.add_one_move_without_mill()
    for _ in range(mill_num):
        _remove_opponents_pawn_by_bot_easy(board)

# Bot próbuje postawić pionek na polu sąsiadującym z obecnie już postawionym
# W pierwszej kolejności wybierane są pola w pobliżu których jest najwięcej innych pionków


def _set_pawn_by_bot_hard(board: Board):
    all_posible_sets = []
    for curr_field in board.get_all_player_fields(Player.TWO):
        for new_field_id in gl.possible_moves(board, curr_field):
            all_posible_sets.append(board.field_by_id(new_field_id))
    fields_occurences = collections.Counter(all_posible_sets)
    if fields_occurences:
        max_occurences = max(fields_occurences.values())
        final_moves = [key for key, val in zip(
            fields_occurences.keys(), fields_occurences.values()) if val == max_occurences]
        field = choice(final_moves)
        board.add_pawn(field, Player.TWO)
        print_board(board)
        print_last_set(field.id())
        player_with_mill, mill_num = gl.check_mill(board, field)
        if mill_num > 0:
            print_bot_mill_occurred(mill_num)
            board.reset_moves_without_mill()
        else:
            board.add_one_move_without_mill()
        for _ in range(mill_num):
            _remove_opponents_pawn_by_bot_hard(board)

    else:
        _set_pawn_by_bot_easy(board)


# Rusza się tak, żeby powstał młynek
def _move_pawn_by_bot_hard(board: Board):
    all_possible_moves = []
    for curr_field in board.get_all_player_fields(Player.TWO):
        for new_field_id in gl.possible_moves(board, curr_field):
            all_possible_moves.append(
                (curr_field, board.field_by_id(new_field_id)))
    # Sprawdzenie keidy wystąpi młynek -DONE
    moves_with_mill = []
    for move in all_possible_moves:
        board.move_pawn(move[0], move[1], Player.TWO)
        player_with_mill, mill_num = gl.check_mill(board, move[1])
        if mill_num != 0:
            moves_with_mill.append(move)
        board.move_pawn(move[1], move[0], Player.TWO)

    if moves_with_mill:
        final_move = choice(moves_with_mill)
    else:
        final_move = choice(all_possible_moves)
    board.move_pawn(final_move[0], final_move[1], Player.TWO)
    print_board(board)
    print_last_move(final_move[0].id(), final_move[1].id())
    player_with_mill, mill_num = gl.check_mill(board, final_move[1])
    if mill_num > 0:
        print_bot_mill_occurred(mill_num)
        board.reset_moves_without_mill()
    else:
        board.add_one_move_without_mill()
    for _ in range(mill_num):
        _remove_opponents_pawn_by_bot_hard(board)


def _remove_opponents_pawn_by_bot_easy(board: Board):
    """Removes random opponent's pawn from all available"""

    all_opponents_fields = board.get_all_player_fields(Player.ONE)
    field = choice(all_opponents_fields)
    board.remove_pawn(field)
    print_board(board)
    print_last_remove(field.id())


def _remove_opponents_pawn_by_bot_hard(board: Board):
    # Usuwa gdy więcej niż jeden w linii
    all_opponents_fields = board.get_all_player_fields(Player.ONE)
    adjacent_fields = {}
    for field in all_opponents_fields:
        conn_count = 0
        for connection in field.connections():
            if board.field_by_id(connection).player() == Player.ONE:
                conn_count += 1
        adjacent_fields[field] = conn_count
    max_occurences = max(adjacent_fields.values())
    final_moves = [key for key, val in zip(
        adjacent_fields.keys(), adjacent_fields.values()) if val == max_occurences]
    field = choice(final_moves)
    board.remove_pawn(field)
    print_board(board)
    print_last_remove(field.id())
