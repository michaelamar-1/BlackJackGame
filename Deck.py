import random

suits = ["♠️", "♥️", "♦️", "♣️"]
ranks = ['2', '3', '4', '5', '6', '7', '8',
         '9', '10', 'J', 'Q', 'K', 'A']

values = {'2': 2, '3': 3, '4': 4, '5': 5,
          '6': 6, '7': 7, '8': 8, '9': 9,
          '10': 10, 'J': 10, 'Q': 10,
          'K': 10, 'A': 11}


class Deck:
    def __init__(self):
        self.cards = [(rank, suit) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
