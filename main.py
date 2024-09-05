import random

# Class for creating each card
class Card:
    def __init__(self, suit, level):
        self.suit = suit
        self.level = level

# Class for organizing the deck and shuffle it
class Deck:
    suites = ["hearts", "diamons", "clubs", "spades"]
    levels = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    def __init__(self):
        self.cards = [Card(suite, level) for suite in Deck.suites for level in Deck.levels]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    

# Class for initializing the players hand and evaluating it
class Hand:
    def __init__(self, cards):
        self.cards = cards

    def evaluate_hand(self):

        # Gets the suite and level of cards in the user or computer hands 
        levels = sorted([card.level for card in self.cards])
        suits = [card.suit for card in self.cards]

        # Check for straight-flush
        if self.is_straight(levels) and self.is_flush(suits):
            return ("straight-flush", self.level_values(levels[-1]))

        # Check for triple
        if self.is_triple(levels):
            return ("triple", self.level_values(levels[0]))

        # Check for straight
        if self.is_straight(levels):
            return ("straight", self.level_values(levels[-1]))

        # Check for flush
        if self.is_flush(suits):
            return ("flush", self.level_values(levels[-1]))

        # Check for pair
        pair_rank = self.is_pair(levels)
        if pair_rank:
            return ("pair", self.level_values(pair_rank))

        # If none of the above, return high card
        return ("high-card", self.level_values(levels[-1]))

    # Function that converts each card to it level compared to other cards    
    def level_values(self, level):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                  '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        return values[level]
    
    def is_pair(self, levels):
        if levels[0] == levels[1] or levels[1] == levels[2] or levels[0] == levels[2]:
            return levels[0]
        
    def is_flush(self, suites):
        return suites[0] == suites[1] == suites[2]

    def is_straight(self, levels):
        level_values = [self.level_values(level) for level in levels]
        return level_values == list(range(level_values[0], level_values[0] + 3))

    def is_triple(self, levels):
        return levels[0] == levels[1] == levels[2]
    

def place_bet():
    bet = int(input("Enter your bet: "))

def deal_cards(deck):
    return [deck.deal_card() for _ in range(3)]

def show_face_cards(hand):
    return [hand.cards[:2]]

def determine_winner(user_hand, computer_hand):

    user_rank = user_hand.evaluate_hand()
    computer_rank = computer_hand.evaluate_hand()



