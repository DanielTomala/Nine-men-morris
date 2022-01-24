import os

from source.consts import FILES_DIRECTORY, PAWNS_NUMBER_TO_BOARD_FILE
from source.enums import PawnsNumber


def read_board_from_file(pawns_number: PawnsNumber):
    file_path = get_path_to_file(pawns_number)
    with open(file_path, "r") as board_file:
        board_str = board_file.read()
    return board_str


def get_path_to_file(pawns_number: PawnsNumber):
    absolute_path = os.path.abspath(__file__)
    file_directory = os.path.dirname(absolute_path)
    parent_directory = os.path.dirname(file_directory)
    file_path = os.path.join(parent_directory, FILES_DIRECTORY,
                             PAWNS_NUMBER_TO_BOARD_FILE[pawns_number])
    return file_path
