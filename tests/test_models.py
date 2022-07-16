import pytest

from tilted.enums import BoardState, CardRank, CardSuit, HandRank
from tilted.exceptions import EmptyDeckException
from tilted.models import Board, Card, Deck, Game


class TestCard:
    def test_value(self):
        card = Card(CardRank.ACE, CardSuit.SPADES)
        assert card.value == 14

    def test_eq(self):
        card1 = Card(CardRank.ACE, CardSuit.SPADES)
        card2 = Card(CardRank.ACE, CardSuit.HEARTS)
        assert card1 == card2

    def test_repr(self):
        card = Card(CardRank.ACE, CardSuit.SPADES)
        assert repr(card) == "A♠"


class TestHand:
    def test_repr(self, create_royal_flush):
        assert repr(create_royal_flush()) == "<Hand: T♠ J♠ Q♠ K♠ A♠>"

    def test_gt(self, create_royal_flush, create_straight_flush):
        assert create_royal_flush() > create_straight_flush()

    def test_lt(self, create_royal_flush, create_straight_flush):
        assert create_straight_flush() < create_royal_flush()

    def test_eq(self, create_straight):
        assert create_straight() == create_straight()

    def test_is_straight(
        self, create_straight, create_straight_flush, create_royal_flush
    ):
        assert all(
            [
                create_straight().is_straight,
                create_straight_flush().is_straight,
                create_royal_flush().is_straight,
            ]
        )

    def test_is_flush(self, create_flush, create_straight_flush, create_royal_flush):
        assert all(
            [
                create_flush().is_flush,
                create_straight_flush().is_flush,
                create_royal_flush().is_flush,
            ]
        )

    def test_hand_rank(
        self,
        create_high_card,
        create_pair,
        create_two_pair,
        create_three_of_a_kind,
        create_straight,
        create_flush,
        create_full_house,
        create_four_of_a_kind,
        create_straight_flush,
        create_royal_flush,
    ):
        hand = create_high_card()
        assert hand.hand_rank == HandRank.HIGH_CARD

        hand = create_pair()
        assert hand.hand_rank == HandRank.PAIR

        hand = create_two_pair()
        assert hand.hand_rank == HandRank.TWO_PAIR

        hand = create_three_of_a_kind()
        assert hand.hand_rank == HandRank.THREE_OF_A_KIND

        hand = create_straight()
        assert hand.hand_rank == HandRank.STRAIGHT

        hand = create_flush()
        assert hand.hand_rank == HandRank.FLUSH

        hand = create_full_house()
        assert hand.hand_rank == HandRank.FULL_HOUSE

        hand = create_four_of_a_kind()
        assert hand.hand_rank == HandRank.FOUR_OF_A_KIND

        hand = create_straight_flush()
        assert hand.hand_rank == HandRank.STRAIGHT_FLUSH

        hand = create_royal_flush()
        assert hand.hand_rank == HandRank.ROYAL_FLUSH

    def test_hand_rank_comparison(
        self,
        create_high_card,
        create_pair,
        create_two_pair,
        create_three_of_a_kind,
        create_straight,
        create_flush,
        create_full_house,
        create_four_of_a_kind,
        create_straight_flush,
        create_royal_flush,
    ):
        high_card = create_high_card()
        pair = create_pair()
        two_pair = create_two_pair()
        three_of_a_kind = create_three_of_a_kind()
        straight = create_straight()
        flush = create_flush()
        full_house = create_full_house()
        four_of_a_kind = create_four_of_a_kind()
        straight_flush = create_straight_flush()
        royal_flush = create_royal_flush()

        assert (
            high_card
            < pair
            < two_pair
            < three_of_a_kind
            < straight
            < flush
            < full_house
            < four_of_a_kind
            < straight_flush
            < royal_flush
        )

    def test_high_card_comparison(self, create_high_card):
        ace_high = create_high_card(card_rank=CardRank.ACE)
        king_high = create_high_card(card_rank=CardRank.KING)
        assert ace_high > king_high

    def test_pair_comparison(self, create_pair):
        aces = create_pair(card_rank=CardRank.ACE)
        kings = create_pair(card_rank=CardRank.KING)
        assert aces > kings

    def test_two_pair_comparison(self, create_two_pair):
        aces_and_kings = create_two_pair()
        aces_and_queens = create_two_pair(card_ranks=(CardRank.ACE, CardRank.QUEEN))
        assert aces_and_kings > aces_and_queens

    def test_three_of_a_kind_comparison(self, create_three_of_a_kind):
        three_aces = create_three_of_a_kind()
        three_kings = create_three_of_a_kind(card_rank=CardRank.KING)
        assert three_aces > three_kings

    def test_straight_comparison(self, create_straight):
        straight_two_to_five = create_straight(start_at=CardRank.TWO)
        straight_three_to_six = create_straight(start_at=CardRank.THREE)
        wheel = create_straight(wheel=True)
        wheel2 = create_straight(wheel=True)
        assert straight_three_to_six > straight_two_to_five
        assert straight_two_to_five > wheel
        assert wheel == wheel2

    def test_flush_comparison(self, create_flush):
        ace_high_flush = create_flush(top_card_rank=CardRank.ACE)
        king_high_flush = create_flush(top_card_rank=CardRank.KING)
        nine_high_flush = create_flush(top_card_rank=CardRank.NINE)
        assert ace_high_flush > king_high_flush > nine_high_flush

    def test_full_house_comparison(self, create_full_house):
        aces_full_of_kings = create_full_house()
        kings_full_of_aces = create_full_house(card_ranks=(CardRank.KING, CardRank.ACE))
        assert aces_full_of_kings > kings_full_of_aces

    def test_four_of_a_kind_comparison(self, create_four_of_a_kind):
        four_aces = create_four_of_a_kind()
        four_kings = create_four_of_a_kind(card_rank=CardRank.KING)
        assert four_aces > four_kings

    def test_straight_flush_comparison(self, create_straight_flush):
        king_high_straight_flush = create_straight_flush()
        queen_high_straight_flush = create_straight_flush(start_at=CardRank.EIGHT)
        assert king_high_straight_flush > queen_high_straight_flush

    def test_royal_flush_comparison(self, create_royal_flush):
        assert create_royal_flush() == create_royal_flush()


class TestDeck:
    def test_deck_creation(self):
        deck = Deck()
        assert len(deck) == 52

    def test_draw(self):
        deck = Deck()
        assert isinstance(deck.draw(), Card)
        assert len(deck) == 51

    def test_draw_many(self):
        deck = Deck()
        cards = deck.draw_many(2)
        assert isinstance(cards, list)
        assert len(deck) == 50
        assert isinstance(cards[0], Card)
        assert isinstance(cards[1], Card)

    def test_burn(self):
        deck = Deck()
        card = deck.burn()
        assert card is None
        assert len(deck) == 51

    def test_raises_when_deck_empty(self):
        deck = Deck()
        with pytest.raises(EmptyDeckException):
            deck.draw_many(53)
        with pytest.raises(EmptyDeckException):
            deck.burn()


class TestBoard:
    def test_repr(self):
        board = Board(
            cards=[
                Card(CardRank.ACE, CardSuit.SPADES),
                Card(CardRank.ACE, CardSuit.HEARTS),
                Card(CardRank.ACE, CardSuit.CLUBS),
            ]
        )
        assert repr(board) == "<Board: A♠ A♥ A♣>"

    def test_state(self):
        board = Board()
        assert board.state == BoardState.PREFLOP

        board.flop = [
            Card(CardRank.ACE, CardSuit.SPADES),
            Card(CardRank.ACE, CardSuit.HEARTS),
            Card(CardRank.ACE, CardSuit.CLUBS),
        ]
        assert board.state == BoardState.FLOP

        board.turn = Card(CardRank.ACE, CardSuit.DIAMIONDS)
        assert board.state == BoardState.TURN

        board.river = Card(CardRank.KING, CardSuit.HEARTS)
        assert board.state == BoardState.RIVER

        with pytest.raises(ValueError):
            board.cards.append(Card(CardRank.KING, CardSuit.DIAMIONDS))
            board.state


class TestGame:
    def test_game_post_init_inits_with_deck_and_board(self):
        game = Game()
        assert isinstance(game.deck, Deck)
        assert isinstance(game.board, Board)

    def test_game_deals_all_streets_and_raises_when_all_dealt(self):
        game = Game()

        assert game.board.flop is None
        game.deal_next_street()
        assert len(game.board.cards) == 3
        assert len(game.board.flop) == 3

        assert game.board.turn is None
        game.deal_next_street()
        assert len(game.board.cards) == 4
        assert game.board.turn is not None

        assert game.board.river is None
        game.deal_next_street()
        assert len(game.board.cards) == 5
        assert game.board.river is not None

        with pytest.raises(ValueError):
            game.deal_next_street()
