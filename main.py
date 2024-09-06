import random
from copy import deepcopy

# Class for creating each card
class Card:
    def __init__(self, suit, level):
        self.suit = suit
        self.level = level

    def __str__(self):
        return f"{self.level} of {self.suit}"

# Class for organizing the deck and shuffle it
class Deck:
    suites = ["hearts", "diamons", "clubs", "spades"]
    levels = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    def __init__(self):
        self.cards = [Card(suite, level) for suite in Deck.suites for level in Deck.levels]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

    def shuffle(self):
        # Shuffle the deck
        random.shuffle(self.cards)
    

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
    
# Function that lets user place bet
def place_bet():
    bet = int(input("Enter your bet: "))
    return bet

# Function that deals the cards at the beginning of each game
def deal_cards(deck):
    return [deck.deal_card() for _ in range(3)]

# Function tha shows the firs 2 cards
def show_face_cards(player, hand):
    face_up_cards = hand.cards[:2]  # First two cards are face-up
    face_up_str = ', '.join([f"{card.level} of {card.suit}" for card in face_up_cards])
    print(f"{player} hand: {face_up_str}")

# Helper function to determine the best hand 
def hand_rank(hand_type):
    ranks = {
        "high-card": 1,
        "pair": 2,
        "flush": 3,
        "straight": 4,
        "triple": 5,
        "straight-flush": 6
    }
    return ranks[hand_type]

# Function to determine the winner
def determine_winner(user_hand, computer_hand):

    user_score, user_value = user_hand.evaluate_hand()
    computer_score, computer_value = computer_hand.evaluate_hand()

    if hand_rank(user_score) > hand_rank(computer_score):
        return "user"
    elif hand_rank(user_score) < hand_rank(computer_score):
        return "computer"
    else:
        # If hand ranks are the same, compare the highest card values
        if user_value > computer_value:
            return "user"
        elif user_value < computer_value:
            return "computer"
        else:
            return "tie"

def ai_move(user_hand, computer_hand):

    winner = determine_winner(user_hand, computer_hand)

    # If we know computer is going to win
    if winner == "computer":
        # If win probability high
            # Random choice from [call, raise]
                # If raise:
                    # Raise == 2x current pot
        
        # If win probability low
            # If current profit is negative:
                # Random choice from [call, raise]
            # Else:
                # Random choice from [call, raise, fold]
        
        return 0
    
    # If we know computer is going to loose
    else:
        # If win probability high
            # If current profit is negative:
                # Random choice from [call, fold]
            # Else:
                # Random choice from [call, raise, fold]
        
        # If win probability low
            # If current profit is negative:
                # Random choice from [call, fold]
            # Else:
                # Random choice from [call, fold]
        
        return 0


def calc_probability(user_hands, computer_hands, deck, simulations=10000):
    #t = deepcopy(deck)

    win = 0
    lose = 0
    draw = 0

    # extract visible two cards
    computer_visible = computer_hands.cards[:2]
    user_visible = user_hands.cards[:2]

    print(computer_visible)
    print(user_visible)

    # simulate calculating the win, lose, draw probabilities with 10000 random simulations
    for _ in range(simulations):
        # reset the deck (without visible 4 cards) in every simulation
        temp = deepcopy(deck)
        temp.shuffle()

        # Randomly draw face-down cards from the deck
        computer_hands = computer_visible + [temp.deal_card()]
        computer_hands = Hand(computer_hands)
        user_hands = user_visible + [temp.deal_card()]
        user_hands = Hand(user_hands)
        
        # Compare hand strengths
        result = determine_winner(user_hands, computer_hands)
        if result == "win":
            win += 1
        elif result == "lose":
            lose += 1
        else:
            draw += 1

    prob_win = win / simulations
    prob_lose = lose / simulations
    prob_draw = draw / simulations

    return prob_win, prob_lose, prob_draw



def main():


    # Initialize profit for company to 0
    computer_profit = 0

    while True:

        # Initialize a deck
        deck = Deck()

        # User places a bet
        total_pot = place_bet()

        # Deal three cards to both user and computer
        user_cards = deal_cards(deck)
        computer_cards = deal_cards(deck)

        # Evaluate the hand to determine winner
        user_hand = Hand(user_cards)
        computer_hand = Hand(computer_cards)


        show_face_cards("User", user_hand)
        show_face_cards("Computer", computer_hand)

        # User place a second bet
        user_decision = input("\nDo you want to raise? (yes/no): ").lower()

        if user_decision == 'yes':
            additional_bet = place_bet()
            total_pot += additional_bet

        prob_win, prob_draw, prob_lose = calc_probability(user_hand, computer_hand, deck)
        print(prob_win, prob_draw, prob_lose)

        ai_move(user_hand, computer_hand)

        winner = determine_winner(user_hand, computer_hand)
        
        if winner == "user":
            computer_profit -= total_pot
        else:
            computer_profit += total_pot

        print("Current computer profit: ", computer_profit)
        play_more = input("Do you want to play another game? (yes/no): ").lower()

        if play_more == "no":
            return False

main()



