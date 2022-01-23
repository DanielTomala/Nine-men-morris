import argparse
from random import choices
from source.game_logic import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-pn", "--pawns-number",
                        help="Pawns number for each player in the game", choices=["9", "3", "6", "12"], default="9")
    parser.add_argument(
        "-b", "--bot", help="If true, game is against bot", choices=["e", "easy", "h", "hard"], default=False)
    # Wyłączenie delaya między ruchami
    args = parser.parse_args()
    main(args)
