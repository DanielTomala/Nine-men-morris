from .enums import Player
from .board import Board
import random
from .interface import print_starting_player, print_welcome, print_board, print_choose_mode


def main():
    print_welcome()
    choose_mode()  # Zwróci liczbę pionków
    board = Board()
    print_board(board)
    start_game(board)


def start_game(board: Board):
    starting_player = get_starting_player()
    print_starting_player(starting_player)
    setting_pawns_phase(board, starting_player)
    moving_pawns_phase()


def get_starting_player():
    num_to_player = {1: Player.FIRST, 2: Player.SECOND}
    number = random.randint(1, 2)
    return num_to_player[number]

# Ponowne wpisanie pola, jeśli gracz wybrał już to zajęte


def setting_pawns_phase(board: Board, starting_player):
    other_player_dict = {Player.FIRST: Player.SECOND,
                         Player.SECOND: Player.FIRST}
    while board.player_pawns_number(Player.FIRST) < board.pawns_number().value or board.player_pawns_number(Player.SECOND) < board.pawns_number().value:
        if board.player_pawns_number(Player.FIRST) < board.pawns_number().value:
            set_pawn_by_player(board, starting_player)
        print_board(board)
        if board.player_pawns_number(Player.SECOND) < board.pawns_number().value:
            set_pawn_by_player(board, other_player_dict[starting_player])
        print_board(board)
    print("All pawns are set, let's move to the next phase of the game!")


def set_pawn_by_player(board: Board, player: Player):
    player_str = {Player.FIRST: "One", Player.SECOND: "Two"}
    print(f"Player number {player_str[player]}")
    # Zabezpiecznie przed nieoczekiwanym inputem, castowanie do upper case
    id = get_user_input("Where do you want to add your pawn: ")
    print()
    field = board.get_field_by_id(id)
    board.add_pawn(field, player)


def get_user_input(message):
    return input(message)


def moving_pawns_phase():
    pass


def choose_mode():
    print_choose_mode()
