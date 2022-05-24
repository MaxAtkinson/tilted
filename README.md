
# Tilted
<img align="left" src="https://user-images.githubusercontent.com/8881202/169894189-c4d64c08-7751-4d0e-a95f-640f07c2e7bd.jpeg" width="100" height="100" />

Tilted is a lightweight, open-source Python package with a simple interface for poker hand evaluation & comparison.

<img src="https://img.shields.io/github/v/release/MaxAtkinson/tilted" />

<br />
<br />

## Installation
With Poetry:
```sh
poetry add tilted
```

With Pip:
```sh
pip install tilted
```

## Basic Usage
Tilted can be used to generate, evaluate and compare 5-card poker hands.

### Hand Generation
To generate a random hand:
```python
from tilted import Deck, Hand


deck = Deck()
unknown_hand = Hand(deck.draw_many(5))

unknown_hand  # <Hand: 8♦ T♠ T♣ Q♣ K♥>
unknown_hand.hand_rank  # <HandRank.PAIR: 2>
```

### Hand Evaluation
To evaluate an unknown hand:
```python
from tilted import Card, CardRank, CardSuit, Hand


unknown_hand = Hand([
  Card(CardRank.TEN, CardSuit.SPADES),
  Card(CardRank.JACK, CardSuit.SPADES),
  Card(CardRank.QUEEN, CardSuit.SPADES),
  Card(CardRank.KING, CardSuit.SPADES),
  Card(CardRank.ACE, CardSuit.SPADES),
])

unknown_hand.hand_rank  # <HandRank.ROYAL_FLUSH: 10>
```

### Hand Comparison
To compare two hands:
```python
from tilted import Card, CardRank, CardSuit, Hand


royal_flush = Hand([
  Card(CardRank.TEN, CardSuit.SPADES),
  Card(CardRank.JACK, CardSuit.SPADES),
  Card(CardRank.QUEEN, CardSuit.SPADES),
  Card(CardRank.KING, CardSuit.SPADES),
  Card(CardRank.ACE, CardSuit.SPADES),
])

straight_flush = Hand([
  Card(CardRank.NINE, CardSuit.HEARTS),
  Card(CardRank.TEN, CardSuit.HEARTS),
  Card(CardRank.JACK, CardSuit.HEARTS),
  Card(CardRank.QUEEN, CardSuit.HEARTS),
  Card(CardRank.KING, CardSuit.HEARTS),
])

royal_flush > straight_flush  # True
```


## Roadmap

### Features
- [x] Hand evaluation
- [x] Hand comparison
- [x] Deck support
- [ ] Board & dealing (Flop, Turn, River)
- [ ] Full board & hole card evaluation
- [ ] Expand beyond Texas Hold 'Em (Pot Limit Omaha)

### Deployment
- [ ] CI
