import collections
from random import choice

from .board import Board
from .game_logic import possible_moves


def set_pawn_by_bot_easy(board: Board):
    return choice(board.get_all_free_fields())


def move_pawn_by_bot_easy(board: Board):
    all_possible_moves = []
    for curr_field in board.get_all_player_fields():
        for new_field_id in possible_moves(board, curr_field):
            all_possible_moves.append(
                (curr_field, board.field_by_id(new_field_id)))
    return choice(all_possible_moves)

# Bot próbuje postawić pionek na polu sąsiadującym z obecnie już postawionym
# W pierwszej kolejności wybierane są pola w pobliżu których jest najwięcej innych pionków


def set_pawn_by_bot_hard(board: Board):
    all_posible_sets = []
    for curr_field in board.get_all_player_fields():
        for new_field_id in possible_moves(board, curr_field):
            all_posible_sets.append(board.field_by_id(new_field_id))
    fields_occurences = collections.Counter(all_posible_sets)
    max_occurences = max(fields_occurences.values())
    # Żeby się choice nie wywalił dla pustej listy
    return choice([key for key, val in fields_occurences if val == max_occurences])


# Rusza się tak, żeby powstał młynek
def move_pawn_by_bot_hard(board: Board):
    all_possible_moves = []
    for curr_field in board.get_all_player_fields():
        for new_field_id in possible_moves(board, curr_field):
            all_possible_moves.append(
                (curr_field, board.field_by_id(new_field_id)))
    #TODO Sprawdzenie keidy wystąpi młynek
