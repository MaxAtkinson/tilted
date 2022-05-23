from enum import Enum, unique


@unique
class CardSuit(Enum):
    CLUBS = "♣"
    DIAMIONDS = "♦"
    HEARTS = "♥"
    SPADES = "♠"


@unique
class CardRank(Enum):
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12
    ACE = 13

    @staticmethod
    def as_str(entry):
        return str(
            entry.name[0] if entry.value > CardRank.NINE.value else entry.value + 1
        )


@unique
class HandRank(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10
