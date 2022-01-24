import argparse

from source.consts import BOT_HELP, DELAY_HELP, PAWNS_NUMBER_HELP
from source.game_logic import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-pn", "--pawns-number",
                        help=PAWNS_NUMBER_HELP, choices=["9", "3", "6", "12"], default="9")
    parser.add_argument(
        "-b", "--bot", help=BOT_HELP, choices=["e", "easy", "h", "hard"], default=False)
    parser.add_argument(
        "-d", "--delay", help=DELAY_HELP, type=float, default=0)
    args = parser.parse_args()
    main(args)
