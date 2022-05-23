from typing import Dict, Final, Tuple

from tilted.enums import CardRank, HandRank

# Hand values based on the binary arithmetic
# FLUSH & STRAIGHT_FLUSH have no entries here
# as the methods for detection of flushy hands
# don't require binary arithmetic.
HIGH_CARD_VALUE: Final[int] = 5
PAIR_VALUE: Final[int] = 6
TWO_PAIR_VALUE: Final[int] = 7
THREE_OF_A_KIND_VALUE: Final[int] = 9
STRAIGHT_VALUE: Final[int] = 31
WHEEL_STRAIGHT_VALUE: Final[int] = 16444
FULL_HOUSE_VALUE: Final[int] = 10
FOUR_OF_A_KIND_VALUE: Final[int] = 1
ROYAL_FLUSH_VALUE: Final[int] = 31744

# Map of binary arithmetic results to hand ranks
# for easy access.
BINARY_ARITHMETIC_RESULT_TO_HAND_RANK: Final[Dict[int, HandRank]] = {
    HIGH_CARD_VALUE: HandRank.HIGH_CARD,
    PAIR_VALUE: HandRank.PAIR,
    TWO_PAIR_VALUE: HandRank.TWO_PAIR,
    THREE_OF_A_KIND_VALUE: HandRank.THREE_OF_A_KIND,
    STRAIGHT_VALUE: HandRank.STRAIGHT,
    WHEEL_STRAIGHT_VALUE: HandRank.STRAIGHT,
    FULL_HOUSE_VALUE: HandRank.FULL_HOUSE,
    FOUR_OF_A_KIND_VALUE: HandRank.FOUR_OF_A_KIND,
    ROYAL_FLUSH_VALUE: HandRank.ROYAL_FLUSH,
}


# We use 15 bits for binary arithmetic, but there
# are only 13 card ranks.
NUM_BITS: Final[int] = 15
UNUSED_BITS: Final[int] = NUM_BITS - len(CardRank)

# For ties, we sort the cards then left bit shift
# each card by the below numbers
TIEBREAKER_BITWISE_LEFT_SHIFTS: Final[Tuple[int, ...]] = (16, 12, 8, 4, 0)
