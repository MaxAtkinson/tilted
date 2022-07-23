import random
from dataclasses import dataclass, field
from functools import cached_property
from typing import Iterable, List, Tuple, Type

from tilted.constants import (
    MADE_POKER_HAND_SIZE,
    NUM_BITS,
    ROYAL_FLUSH_VALUE,
    STRAIGHT_VALUE,
    WHEEL_STRAIGHT_VALUE,
)
from tilted.enums import BoardState, CardRank, CardSuit, HandRank
from tilted.exceptions import EmptyDeckException
from tilted.hand_evaluation import HandEvaluator
from tilted.utils import (
    bit_sequence_to_int,
    get_binary_index_from_card_rank,
    get_combinations,
)


@dataclass(frozen=True)
class Card:
    rank: CardRank
    suit: CardSuit

    @staticmethod
    def sort(card):
        return card.rank.value

    @cached_property
    def value(self):
        return self.rank.value + 1

    def __eq__(self, other):
        return self.rank.value == other.rank.value

    def __repr__(self) -> str:
        return f"{CardRank.as_str(self.rank)}{self.suit.value}"


@dataclass
class Player:
    name: str
    hole_cards: Tuple = field(default_factory=tuple)

    def __repr__(self):
        return f"<Player: {self.name}>"

    def set_hole_cards(self, hole_cards):
        assert len(hole_cards) == 2, "Texas Hold 'Em is a two hole-card game."
        self.hole_cards = hole_cards


@dataclass
class Hand:
    cards: Iterable[Type[Card]]
    player: Player | None = None

    def __post_init__(self):
        assert len(self.cards) == 5, "A poker hand is 5 cards."
        assert len(self.cards) == len(
            set(self.cards)
        ), "All cards in a hand must be unique."
        self.cards = sorted(self.cards, key=Card.sort)
        self.evaluator = HandEvaluator(self)

    def __repr__(self) -> str:
        cards = " ".join(str(card) for card in self.cards)
        return f"<Hand: {cards}>"

    def __gt__(self, other) -> bool:
        if other is None:
            return True

        is_same_hand_rank = self.evaluator.is_same_hand_rank(other)
        is_better_hand = self.hand_rank.value > other.hand_rank.value
        return (
            self.evaluator.break_tie(other) == self
            if is_same_hand_rank
            else is_better_hand
        )

    def __lt__(self, other) -> bool:
        if other is None:
            return False

        is_same_hand_rank = self.evaluator.is_same_hand_rank(other)
        is_worse_hand = self.hand_rank.value < other.hand_rank.value
        return (
            self.evaluator.break_tie(other) is other
            if is_same_hand_rank
            else is_worse_hand
        )

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        is_same_hand_rank = self.evaluator.is_same_hand_rank(other)
        return self.evaluator.break_tie(other) is None if is_same_hand_rank else False

    def __contains__(self, value: CardRank) -> bool:
        return any([card.rank == value for card in self.cards])

    @cached_property
    def card_values(self) -> int:
        """
        Returns int representation of a binary number of the form:

        A K Q J T 9 8 7 6 5 4 3 2 - -
        1 1 1 1 1 0 0 0 0 0 0 0 0 0 0

        Where a 1 represents that the card rank is in the hand and a 0
        represents that the card rank isn't in the hand.
        """
        result = list("0" * NUM_BITS)
        for card in self.cards:
            binary_idx = get_binary_index_from_card_rank(card.rank)
            result[binary_idx] = "1"
        return bit_sequence_to_int(result)

    @cached_property
    def card_counts(self) -> int:
        """
        Returns int representation of a binary number of the form:

        A    K    Q    J    T    9    8    7    6    5    4    3    2    -    -
        0001 0001 0001 0001 0001 0000 0000 0000 0000 0000 0000 0000 0000 0000 0000

        Where each 4-bit field represents the number of cards of that rank
        in the hand.
        """
        result = ["0000" for _ in range(NUM_BITS)]
        counts = {
            card.rank: len(
                [
                    count_card
                    for count_card in self.cards
                    if count_card.rank == card.rank
                ]
            )
            for card in self.cards
        }
        for rank, count in counts.items():
            binary_idx = get_binary_index_from_card_rank(rank)
            binary_value = ("1" * count).zfill(4)
            result[binary_idx] = binary_value
        return bit_sequence_to_int(result)

    @cached_property
    def is_straight(self) -> bool:
        lsb = self.card_values & -self.card_values
        return (
            self.card_values / lsb == STRAIGHT_VALUE
            or self.card_values == WHEEL_STRAIGHT_VALUE
        )

    @cached_property
    def is_wheel(self) -> bool:
        """
        In poker, the term "wheel" refers to the ace-low straight (A2345).
        """
        return self.is_straight and CardRank.ACE in self and CardRank.FIVE in self

    @cached_property
    def is_flush(self) -> bool:
        return len(set(card.suit for card in self.cards)) == 1

    @cached_property
    def is_royal_flush(self) -> bool:
        return (
            self.is_straight and self.is_flush and self.card_values == ROYAL_FLUSH_VALUE
        )

    @cached_property
    def hand_rank(self) -> HandRank:
        return self.evaluator.get_hand_rank()


class Deck:
    cards: List[Card]

    def __init__(self):
        self.cards = []

        for suit in CardSuit:
            for rank in CardRank:
                self.cards.append(Card(rank, suit))

        random.shuffle(self.cards)

    def __len__(self) -> int:
        return len(self.cards)

    def draw(self) -> Card:
        try:
            return self.cards.pop()
        except IndexError as ex:
            raise EmptyDeckException from ex

    def draw_many(self, num_cards: int) -> List[Card]:
        return [self.draw() for _ in range(num_cards)]

    def burn(self) -> None:
        self.draw()


@dataclass
class Board:
    cards: List[Card] = field(default_factory=list)

    @property
    def state(self):
        cards_dealt = len(self.cards)

        if cards_dealt == 0:
            return BoardState.PREFLOP
        elif cards_dealt == 3:
            return BoardState.FLOP
        elif cards_dealt == 4:
            return BoardState.TURN
        elif cards_dealt == 5:
            return BoardState.RIVER
        else:
            raise ValueError("Invalid game state")

    @property
    def flop(self):
        return self.cards[0:3] if len(self.cards) >= 3 else None

    @flop.setter
    def flop(self, value: List[Card]):
        assert len(value) == 3, "The flop is 3 cards."
        assert len(self.cards) == 0, "The flop is the first street."
        self.cards.extend(value)

    @property
    def turn(self):
        return self.cards[3] if len(self.cards) >= 4 else None

    @turn.setter
    def turn(self, value: Card):
        assert len(self.cards) == 3, "The turn is the second street."
        self.cards.append(value)

    @property
    def river(self):
        return self.cards[4] if len(self.cards) >= 5 else None

    @river.setter
    def river(self, value: Card):
        assert len(self.cards) == 4, "The river is the third street."
        self.cards.append(value)

    def __repr__(self) -> str:
        cards = " ".join([str(card) for card in self.cards])
        return f"<Board: {cards}>"


@dataclass
class Game:
    num_players: int = 0
    deck: Deck = field(default_factory=Deck)
    board: Board = field(default_factory=Board)
    players: List[Player] = field(default_factory=list)

    def __post_init__(self):
        self.deck = Deck() if self.deck is None else self.deck
        self.board = Board() if self.board is None else self.board
        self.players = [Player(f"Player #{i + 1}") for i in range(self.num_players)]
        self.deal_hole_cards()

    def deal_hole_cards(self):
        for player in self.players:
            hole_cards = tuple(self.deck.draw_many(2))
            player.set_hole_cards(hole_cards)

    def deal_next_street(self):
        board_state = self.board.state

        if board_state == BoardState.PREFLOP:
            self.deal_flop()
        elif board_state == BoardState.FLOP:
            self.deal_turn()
        elif board_state == BoardState.TURN:
            self.deal_river()
        else:
            raise ValueError("No more streets to deal.")

    def deal_flop(self):
        cards = self.deck.draw_many(3)
        self.board.flop = cards

    def deal_turn(self):
        card = self.deck.draw()
        self.board.turn = card

    def deal_river(self):
        card = self.deck.draw()
        self.board.river = card

    def _get_candidate_hands(self, player: Player) -> List[Hand]:
        return [
            Hand(candidate_hand, player)
            for candidate_hand in get_combinations(
                list(player.hole_cards) + self.board.cards, MADE_POKER_HAND_SIZE
            )
        ]

    def get_winner(self) -> List[Player]:
        """
        Gets all combinations of board + hole cards for each player
        (the candidate hands), selects the best (the showdown hand)
        then pits all the best hands off against eachother, returning
        the winning player(s).
        """
        showdown_hands = []
        for player in self.players:
            candidate_hands = self._get_candidate_hands(player)
            showdown_hand = max(candidate_hands)
            showdown_hands.append(showdown_hand)

        best_hand = max(showdown_hands)
        winning_hands = [hand for hand in showdown_hands if hand == best_hand]
        return [
            winning_hand.player for winning_hand in winning_hands if winning_hand.player
        ]
