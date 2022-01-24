import collections
from random import choice
from time import sleep

import source.game_logic as gl
from source.board import Board
from source.enums import BotLvl, Player
from source.interface import (print_before_move_bot, print_board,
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

    field = choice(board.all_free_fields())
    board.add_pawn(field, Player.TWO)
    print_board(board)
    print_last_set(field.id())
    _, mills_num = gl.check_mill(board, field)
    if mills_num > 0:
        print_bot_mill_occurred(mills_num)
        board.reset_moves_without_mill()
    else:
        board.add_one_move_without_mill()
    for _ in range(mills_num):
        _remove_opponents_pawn_by_bot_easy(board)


def _move_pawn_by_bot_easy(board: Board):
    """Makes random move from all available """

    all_possible_moves = []
    for curr_field in board.all_player_fields(Player.TWO):
        for new_field_id in board.possible_moves(curr_field):
            new_field = board.field_by_id(new_field_id)
            all_possible_moves.append((curr_field, new_field))

    final_move = choice(all_possible_moves)
    board.move_pawn(final_move[0], final_move[1], Player.TWO)
    print_board(board)
    print_last_move(final_move[0].id(), final_move[1].id())

    _, mills_num = gl.check_mill(board, final_move[1])
    if mills_num > 0:
        print_bot_mill_occurred(mills_num)
        board.reset_moves_without_mill()
    else:
        board.add_one_move_without_mill()
    for _ in range(mills_num):
        _remove_opponents_pawn_by_bot_easy(board)


def _set_pawn_by_bot_hard(board: Board):
    """Sets pawn as close as it is possible to other already set pawns"""

    all_posible_sets = []
    for curr_field in board.all_player_fields(Player.TWO):
        for new_field_id in board.possible_moves(curr_field):
            all_posible_sets.append(board.field_by_id(new_field_id))

    fields_occurences = collections.Counter(all_posible_sets)
    if fields_occurences:
        max_occur = max(fields_occurences.values())
        key_val_zip = zip(fields_occurences.keys(), fields_occurences.values())
        final_fields = [key for key, val in key_val_zip if val == max_occur]
        field = choice(final_fields)
        board.add_pawn(field, Player.TWO)
        print_board(board)
        print_last_set(field.id())

        _, mills_num = gl.check_mill(board, field)
        if mills_num > 0:
            print_bot_mill_occurred(mills_num)
            board.reset_moves_without_mill()
        else:
            board.add_one_move_without_mill()
        for _ in range(mills_num):
            _remove_opponents_pawn_by_bot_hard(board)

    else:
        _set_pawn_by_bot_easy(board)


def _move_pawn_by_bot_hard(board: Board):
    """
    If move which will cause mill is possible it makes it,
    else makes random move
    """

    all_possible_moves = []
    for curr_field in board.all_player_fields(Player.TWO):
        for new_field_id in board.possible_moves(curr_field):
            new_field = board.field_by_id(new_field_id)
            all_possible_moves.append((curr_field, new_field))

    moves_with_mill = []
    for move in all_possible_moves:
        board.move_pawn(move[0], move[1], Player.TWO)
        _, mills_num = gl.check_mill(board, move[1])
        if mills_num != 0:
            moves_with_mill.append(move)
        board.move_pawn(move[1], move[0], Player.TWO)

    if moves_with_mill:
        final_move = choice(moves_with_mill)
    else:
        final_move = choice(all_possible_moves)
    board.move_pawn(final_move[0], final_move[1], Player.TWO)
    print_board(board)
    print_last_move(final_move[0].id(), final_move[1].id())

    _, mills_num = gl.check_mill(board, final_move[1])
    if mills_num > 0:
        print_bot_mill_occurred(mills_num)
        board.reset_moves_without_mill()
    else:
        board.add_one_move_without_mill()
    for _ in range(mills_num):
        _remove_opponents_pawn_by_bot_hard(board)


def _remove_opponents_pawn_by_bot_easy(board: Board):
    """Removes random opponent's pawn from all available"""

    all_opponents_fields = board.all_player_fields(Player.ONE)
    remove_field = choice(all_opponents_fields)
    board.remove_pawn(remove_field)
    print_board(board)
    print_last_remove(remove_field.id())


def _remove_opponents_pawn_by_bot_hard(board: Board):
    """Removes opponent's pawn which has most pawns around it"""

    all_opponents_fields = board.all_player_fields(Player.ONE)
    fields_around_no = {}
    for field in all_opponents_fields:
        conn_count = 0
        for connection in field.connections():
            if board.field_by_id(connection).player() == Player.ONE:
                conn_count += 1
        fields_around_no[field] = conn_count
    max_occurences = max(fields_around_no.values())
    key_val_zip = zip(fields_around_no.keys(), fields_around_no.values())
    final_moves = [key for key, val in key_val_zip if val == max_occurences]
    remove_field = choice(final_moves)
    board.remove_pawn(remove_field)
    print_board(board)
    print_last_remove(remove_field.id())
