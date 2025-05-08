from Deck import values


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def add_card(self, card):
        self.hand.append(card)

    def calculate_score(self):
        self.score = 0
        aces = 0
        for card in self.hand:
            rank = card[0]
            self.score += values[rank]
            if rank == 'A':
                aces += 1
        while self.score > 21 and aces:
            self.score -= 10
            aces -= 1
        return self.score
