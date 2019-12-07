import random

class blackjack:
    def __init__(self):
        self.score = 0
        self.deck = []
    
    def new_deck(self):
        suits = {"Spade", "Heart", "Diamond", "Club"}
        ranks = {'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'}
        for name in suits:
            for num in ranks:
                self.deck.append({"suit": name, "rank": num})
        random.shuffle(self.deck)
        return self.deck
    
    def hit(self, deck):
        if self.deck == []:
            self.deck = new_deck()
        return (self.deck[0] , self.deck[1:])