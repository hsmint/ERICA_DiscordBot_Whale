import random

class blackjack:
    def __init__(self):
        self.deck = []
    
    def new_deck(self):
        suits = {"Spade", "Heart", "Diamond", "Club"}
        ranks = {'A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'}
        for name in suits:
            for num in ranks:
                self.deck.append({"suit": name, "rank": num})
        random.shuffle(self.deck)
        return

    def hit(self):
        if self.deck == []:
            self.new_deck()
        card, self.deck = self.deck[0], self.deck[1:]
        return card
    
    def count_score(self, cards):
        score = 0
        number_of_ace = 0
        for card in cards:
            save = card['rank']
            if card['rank'] in ('J', 'Q', 'K'):
                save = 10
            elif card['rank'] == 'A':
                save = 11
                number_of_ace += 1
            score += save
        while number_of_ace > 0 and score > 21:
            score -= 10
            number_of_ace -= 1
        return score