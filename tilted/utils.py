from typing import Any, Sequence

from tilted.constants import NUM_BITS, UNUSED_BITS
from tilted.enums import CardRank


def combinations(items: Sequence[Any], n: int):
    if n == 1:
        for x in items:
            yield [x]
    for i in range(len(items)):
        for x in combinations(items[:i], n - 1):
            yield [items[i]] + x


def bit_sequence_to_int(bit_list: Sequence[str]):
    bits = "".join(bit_list)
    return int(f"0b{bits}", 2)


def get_binary_index_from_card_rank(rank: CardRank):
    return NUM_BITS - rank.value - UNUSED_BITS
