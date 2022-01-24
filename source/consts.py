from .enums import BotLvl, PawnsNumber, Player, Position as pos
from .enums import PositionSquare as pos_sq


FIELD_IDS = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
             "L", "M", "N", "O", "P", "R", "S", "T", "U", "W", "X", "Y", "Z"]

POS_TMB_LIST = [pos.TOP, pos.MIDDLE, pos.BOTTOM]
POS_LCR_LIST = [pos.LEFT, pos.CENTER, pos.RIGHT]
POS_SQ_OI_LIST = [pos_sq.OUTER, pos_sq.INNER]

OTHER_PLAYER = {Player.ONE: Player.TWO,
                Player.TWO: Player.ONE}
PLAYER_TO_STR = {Player.ONE: "One", Player.TWO: "Two"}
PLAYER_SYMBOL = {Player.ONE: "$", Player.TWO: "#", None: "o"}
NUM_TO_PLAYER = {1: Player.ONE, 2: Player.TWO}

STR_TO_PAWNS_NUMBER = {"9": PawnsNumber.NINE, "3": PawnsNumber.THREE,
                       "6": PawnsNumber.SIX, "12": PawnsNumber.TWELVE}
STR_TO_BOT_LVL = {False: BotLvl.OFF, "e": BotLvl.EASY,
                  "easy": BotLvl.EASY, "h": BotLvl.HARD, "hard": BotLvl.HARD}

CONNECTIONS_THREE = {"A": ["B", "D", "E"],
                     "B": ["A", "C", "E"],
                     "C": ["B", "F", "E"],
                     "D": ["A", "E", "G"],
                     "E": ["A", "B", "C", "D", "F", "G", "H", "I"],
                     "F": ["C", "E", "I"],
                     "G": ["D", "E", "H"],
                     "H": ["E", "G", "I"],
                     "I": ["E", "F", "H"]}

CONNECTIONS_SIX = {"A": ["B", "G"],
                   "B": ["A", "C", "E"],
                   "C": ["B", "J"],
                   "D": ["E", "H"],
                   "E": ["B", "D", "F"],
                   "F": ["E", "I"],
                   "G": ["A", "H", "N"],
                   "H": ["D", "G", "K"],
                   "I": ["F", "J", "M"],
                   "J": ["C", "I", "P"],
                   "K": ["H", "L"],
                   "L": ["K", "M", "O"],
                   "M": ["I", "L"],
                   "N": ["G", "O"],
                   "O": ["L", "N", "P"],
                   "P": ["J", "O"]}

CONNECTIONS_NINE = {"A": ["B", "J"],
                    "B": ["A", "C", "E"],
                    "C": ["B", "O"],
                    "D": ["E", "K"],
                    "E": ["B", "D", "F", "H"],
                    "F": ["E", "N"],
                    "G": ["H", "L"],
                    "H": ["E", "G", "I"],
                    "I": ["H", "M"],
                    "J": ["A", "K", "X"],
                    "K": ["D", "J", "L", "T"],
                    "L": ["G", "K", "P"],
                    "M": ["I", "N", "S"],
                    "N": ["F", "M", "O", "W"],
                    "O": ["C", "N", "Z"],
                    "P": ["L", "R"],
                    "R": ["P", "S", "U"],
                    "S": ["M", "R"],
                    "T": ["K", "U"],
                    "U": ["R", "T", "W", "Y"],
                    "W": ["N", "U"],
                    "X": ["J", "Y"],
                    "Y": ["U", "X", "Z"],
                    "Z": ["O", "Y"]}

CONNECTIONS_TWELVE = {"A": ["B", "D", "J"],
                      "B": ["A", "C", "E"],
                      "C": ["B", "F", "O"],
                      "D": ["A", "E", "G", "K"],
                      "E": ["B", "D", "F", "H"],
                      "F": ["C", "E", "I", "N"],
                      "G": ["D", "H", "L"],
                      "H": ["E", "G", "I"],
                      "I": ["F", "H", "M"],
                      "J": ["A", "K", "X"],
                      "K": ["D", "J", "L", "T"],
                      "L": ["G", "K", "P"],
                      "M": ["I", "N", "S"],
                      "N": ["F", "M", "O", "W"],
                      "O": ["C", "N", "Z"],
                      "P": ["L", "R", "T"],
                      "R": ["P", "S", "U"],
                      "S": ["M", "R", "W"],
                      "T": ["K", "P", "U", "X"],
                      "U": ["R", "T", "W", "Y"],
                      "W": ["N", "S", "U", "Z"],
                      "X": ["J", "T", "Y"],
                      "Y": ["U", "X", "Z"],
                      "Z": ["O", "W", "Y"]}
