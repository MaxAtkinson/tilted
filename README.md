<img align="left" src="https://user-images.githubusercontent.com/8881202/169818987-99843287-f2cd-476b-94e3-2333bfc4ae1f.jpeg" width="120" height="120" />

# AcePy
AcePy is a lightweight, open-source Python package with a simple interface for poker hand comparison.

## Installation
.

## Basic Usage
AcePy can be used to evaluate and compare 5-card poker hands.

### Hand Comparison
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

### Hand Evaluation
.

## TODOs
.
