import pytest

from ace_py.enums import CardRank, CardSuit
from ace_py.models import Card, Hand


@pytest.fixture
def create_high_card():
    def _create_high_card(card_rank=CardRank.ACE):
        return Hand(
            [
                Card(card_rank, CardSuit.SPADES),
                Card(CardRank.SIX, CardSuit.CLUBS),
                Card(CardRank.FOUR, CardSuit.HEARTS),
                Card(CardRank.THREE, CardSuit.DIAMIONDS),
                Card(CardRank.TWO, CardSuit.HEARTS),
            ]
        )

    return _create_high_card


@pytest.fixture
def create_pair():
    def _create_pair(card_rank=CardRank.ACE):
        return Hand(
            [
                Card(card_rank, CardSuit.SPADES),
                Card(card_rank, CardSuit.CLUBS),
                Card(CardRank.FOUR, CardSuit.HEARTS),
                Card(CardRank.THREE, CardSuit.DIAMIONDS),
                Card(CardRank.TWO, CardSuit.HEARTS),
            ]
        )

    return _create_pair


@pytest.fixture
def create_two_pair():
    def _create_two_pair(card_ranks=(CardRank.ACE, CardRank.KING)):
        return Hand(
            [
                Card(card_ranks[0], CardSuit.SPADES),
                Card(card_ranks[0], CardSuit.CLUBS),
                Card(card_ranks[1], CardSuit.HEARTS),
                Card(card_ranks[1], CardSuit.DIAMIONDS),
                Card(CardRank.TWO, CardSuit.HEARTS),
            ]
        )

    return _create_two_pair


@pytest.fixture
def create_three_of_a_kind():
    def _create_three_of_a_kind(card_rank=CardRank.ACE):
        return Hand(
            [
                Card(card_rank, CardSuit.SPADES),
                Card(card_rank, CardSuit.CLUBS),
                Card(card_rank, CardSuit.HEARTS),
                Card(CardRank.THREE, CardSuit.DIAMIONDS),
                Card(CardRank.TWO, CardSuit.HEARTS),
            ]
        )

    return _create_three_of_a_kind


@pytest.fixture
def create_straight():
    def _create_straight(start_at=CardRank.TEN, wheel=False):
        suits = (
            CardSuit.SPADES,
            CardSuit.HEARTS,
            CardSuit.SPADES,
            CardSuit.DIAMIONDS,
            CardSuit.CLUBS,
        )
        if wheel:
            ranks = [
                CardRank.ACE,
                CardRank.TWO,
                CardRank.THREE,
                CardRank.FOUR,
                CardRank.FIVE,
            ]
        else:
            ranks = [
                CardRank(rank)
                for rank in range(start_at.value, start_at.value + len(suits))
            ]
        return Hand([Card(rank, suit) for rank, suit in zip(ranks, suits)])

    return _create_straight


@pytest.fixture
def create_flush():
    def _create_flush(top_card_rank=CardRank.ACE, suit=CardSuit.SPADES):
        ranks = (
            CardRank.TWO,
            CardRank.FOUR,
            CardRank.FIVE,
            CardRank.SIX,
            top_card_rank,
        )
        return Hand([Card(rank, suit) for rank in ranks])

    return _create_flush


@pytest.fixture
def create_full_house():
    def _create_full_house(card_ranks=(CardRank.ACE, CardRank.KING)):
        return Hand(
            [
                Card(card_ranks[0], CardSuit.SPADES),
                Card(card_ranks[0], CardSuit.CLUBS),
                Card(card_ranks[0], CardSuit.HEARTS),
                Card(card_ranks[1], CardSuit.DIAMIONDS),
                Card(card_ranks[1], CardSuit.HEARTS),
            ]
        )

    return _create_full_house


@pytest.fixture
def create_four_of_a_kind():
    def _create_four_of_a_kind(card_rank=CardRank.ACE):
        return Hand(
            [
                Card(card_rank, CardSuit.SPADES),
                Card(card_rank, CardSuit.CLUBS),
                Card(card_rank, CardSuit.HEARTS),
                Card(card_rank, CardSuit.DIAMIONDS),
                Card(CardRank.TWO, CardSuit.HEARTS),
            ]
        )

    return _create_four_of_a_kind


@pytest.fixture
def create_straight_flush():
    def _create_straight_flush(start_at=CardRank.NINE, wheel=False):
        if wheel:
            ranks = [
                CardRank.ACE,
                CardRank.TWO,
                CardRank.THREE,
                CardRank.FOUR,
                CardRank.FIVE,
            ]
        else:
            ranks = [
                CardRank(rank) for rank in range(start_at.value, start_at.value + 5)
            ]
        return Hand([Card(rank, CardSuit.SPADES) for rank in ranks])

    return _create_straight_flush


@pytest.fixture
def create_royal_flush():
    def _create_royal_flush():
        return Hand(
            [
                Card(CardRank.ACE, CardSuit.SPADES),
                Card(CardRank.KING, CardSuit.SPADES),
                Card(CardRank.QUEEN, CardSuit.SPADES),
                Card(CardRank.JACK, CardSuit.SPADES),
                Card(CardRank.TEN, CardSuit.SPADES),
            ]
        )

    return _create_royal_flush
