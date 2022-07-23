from tilted.enums import CardRank
from tilted.utils import (
    bit_sequence_to_int,
    get_binary_index_from_card_rank,
    get_combinations,
)


class TestUtils:
    def test_get_combinations(self):
        assert len(list(get_combinations([1, 2, 3, 4, 5, 6, 7], 5))) == 21

    def test_bit_sequence_to_int(self):
        assert bit_sequence_to_int("0110") == 6
        assert bit_sequence_to_int("0010") == 2

    def test_get_binary_index_from_card_rank(self):
        assert get_binary_index_from_card_rank(CardRank.TWO) == 12
        assert get_binary_index_from_card_rank(CardRank.THREE) == 11
        assert get_binary_index_from_card_rank(CardRank.FOUR) == 10
        assert get_binary_index_from_card_rank(CardRank.FIVE) == 9
        assert get_binary_index_from_card_rank(CardRank.SIX) == 8
        assert get_binary_index_from_card_rank(CardRank.SEVEN) == 7
        assert get_binary_index_from_card_rank(CardRank.EIGHT) == 6
        assert get_binary_index_from_card_rank(CardRank.NINE) == 5
        assert get_binary_index_from_card_rank(CardRank.TEN) == 4
        assert get_binary_index_from_card_rank(CardRank.JACK) == 3
        assert get_binary_index_from_card_rank(CardRank.QUEEN) == 2
        assert get_binary_index_from_card_rank(CardRank.KING) == 1
        assert get_binary_index_from_card_rank(CardRank.ACE) == 0
