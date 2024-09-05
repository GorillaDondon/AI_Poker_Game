import random

class Card:
    def __init__(self, suite, level):
        self.suite = suite
        self.level = level

class Deck:
    suites = ["hearts", "diamons", "clubs", "spades"]
    levels = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    def __init__(self):
        self.cards = [Card(suite, level) for suite in Deck.suites for level in Deck.levels]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    

class Hand:
    def __init__(self, cards):
        self.cards = cards

    def is_pair(self, levels):
        if levels[0] == levels[1] or levels[1] == levels[2] or levels[0] == levels[2]:
            return levels[0]

    




def place_bet():
    bet = int(input("Enter your bet: "))

def deal_cards(deck):
    return [deck.deal_card() for _ in range(3)]

def show_face_cards(hand):
    return [hand.cards[:2]]

def determine_winner(user_hand, computer_hand):

    user_rank = user_hand.evaluate_hand()
    computer_rank = computer_hand.evaluate_hand()




