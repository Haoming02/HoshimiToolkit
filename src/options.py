from enum import Enum

UNITY_VERSION = "2022.3.22f1"

CPU_THREADS = 16
"""adjust this according to your hardware"""
MAX_RETRY = 5
"""number of attempts to download an asset"""
OPTIMIZE = False
"""compress the images (slower)"""

FILTER = r".*"
"""the regular expression for assets to download"""


class WorkMode(Enum):
    remote = 0
    local = 1


class DiffMode(Enum):
    diff = 0
    all = 1


class Game(Enum):
    ipr = 0
    gakumas = 1
    kr = 2


class MagicStrings:
    @staticmethod
    def get(game: Game) -> tuple[bytes, bytes]:
        match game:
            case Game.ipr:
                return (
                    bytes.fromhex("db3cf044ca27e0fbe672bc4c507bda5b"),
                    bytes.fromhex("1c6e6f9255c0e5412712f4010225e378"),
                )
            case Game.gakumas:
                return (
                    bytes.fromhex("9d8dfd7b1371612846f7ba44e01af160"),
                    bytes.fromhex("1c6e6f9255c0e5412712f4010225e378"),
                )
            case Game.kr:
                return (
                    bytes.fromhex("62ec03eb7971f85cffda333e123155a7"),
                    bytes.fromhex("1c6e6f9255c0e5412712f4010225e378"),
                )
