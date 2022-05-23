
# AcePy
<img align="left" src="https://user-images.githubusercontent.com/8881202/169818987-99843287-f2cd-476b-94e3-2333bfc4ae1f.jpeg" width="100" height="100" />

AcePy is a lightweight, open-source Python package with a simple interface for poker hand comparison.

<br />
<br />

## Installation
With poetry:
```sh
poetry add ace_py
```

With Pip:
```sh
pip install ace_py
```

## Basic Usage
AcePy can be used to evaluate and compare 5-card poker hands.

### Hand Evaluation
To evaluate an unknown hand:
```python
from ace_py import Card, CardRank, CardSuit, Hand


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
from ace_py import Card, CardRank, CardSuit, Hand


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
- [x] 5-card hand comparison
- [ ] Deck support
- [ ] Board & dealing (Flop, Turn, River)
- [ ] Full board & hole card evaluation
- [ ] Expand beyond Texas Hold 'Em (Pot Limit Omaha)
