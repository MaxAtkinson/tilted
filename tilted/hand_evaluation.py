from collections import Counter
from dataclasses import dataclass
from functools import reduce
from operator import ior
from typing import TYPE_CHECKING, List, Type

from tilted.constants import (
    BINARY_ARITHMETIC_RESULT_TO_HAND_RANK,
    NUM_BITS,
    TIEBREAKER_BITWISE_LEFT_SHIFTS,
)
from tilted.enums import HandRank

if TYPE_CHECKING:
    from tilted.models import Card, Hand


@dataclass
class HandEvaluator:
    hand: Type["Hand"]

    def _get_cards_ordered_by_frequency_and_face_value(self) -> List[Type["Card"]]:
        cards = self.hand.cards
        counter = Counter([card.value for card in cards])
        return sorted(cards, key=lambda card: (-counter[card.value], card.value))

    def get_hand_rank(self) -> HandRank:
        modulo_division_result = self.hand.card_counts % NUM_BITS  # type: ignore
        rank = BINARY_ARITHMETIC_RESULT_TO_HAND_RANK[modulo_division_result]

        if rank == HandRank.HIGH_CARD:
            # If binary result is high card, check for
            # hands which can't be determined by modulo division
            if self.hand.is_flush:
                if self.hand.is_straight:
                    if self.hand.is_royal_flush:
                        return HandRank.ROYAL_FLUSH
                    return HandRank.STRAIGHT_FLUSH
                return HandRank.FLUSH
            elif self.hand.is_straight:
                return HandRank.STRAIGHT
        return rank

    def get_tiebreak_score(self):
        """
        In order to break ties, we sort cards by their frequency of occurence
        and rank, then left shift each card's rank by TIEBREAKER_BITWISE_LEFT_SHIFTS.
        """
        ordered_cards = self._get_cards_ordered_by_frequency_and_face_value()

        left_shifted_bits = [
            card.value << shift_by
            for card, shift_by in zip(ordered_cards, TIEBREAKER_BITWISE_LEFT_SHIFTS)
        ]

        score = reduce(ior, left_shifted_bits)
        return score

    def is_same_hand_rank(self, other) -> bool:
        return self.get_hand_rank() == other.evaluator.get_hand_rank()

    def break_tie(self, other_hand: Type["Hand"]) -> Type["Hand"] | None:
        score = self.get_tiebreak_score()
        other_score = other_hand.evaluator.get_tiebreak_score()
        if score == other_score:
            return None

        # If either hand is a wheel (low straight A2345) then the higher
        # straight wins. Wheel vs wheel would have the same score and be
        # handled above.
        either_hand_is_wheel = any([self.hand.is_wheel, other_hand.is_wheel])
        if either_hand_is_wheel:
            winner = next(hand for hand in (self.hand, other_hand) if not hand.is_wheel)
            return winner

        # Return the hand with the highest score
        return self.hand if score > other_score else other_hand
