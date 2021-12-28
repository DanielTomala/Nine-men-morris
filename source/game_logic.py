from .enums import Player
from .board import Board
import random


def start_game():
    board = Board()
    starting_player = get_starting_player()
    setting_pawns_phase(board, starting_player)
    moving_pawns_phase()


def get_starting_player():
    num_to_player = {1: Player.FIRST, 2: Player.SECOND}
    number = random.randint(1, 2)
    return num_to_player[number]


def setting_pawns_phase(board: Board, starting_player):
    other_player_dict = {Player.FIRST: Player.SECOND,
                         Player.SECOND: Player.FIRST}
    while board.players_pawns_number(Player.FIRST) < board.size() or board.players_pawns_number(Player.SECOND) < board.size():
        if board.players_pawns_number(Player.FIRST) < board.size():
            set_pawn_by_player(board, starting_player)
        if board.players_pawns_number(Player.SECOND) < board.size():
            set_pawn_by_player(board, other_player_dict[starting_player])


def set_pawn_by_player(board: Board, player: Player):
    id = get_user_input("Where do you want to add your pawn: ")
    field = board.get_field_by_id(id)
    board.add_pawn(field, player)


def get_user_input(message):
    return input(message)


def moving_pawns_phase():
    pass
