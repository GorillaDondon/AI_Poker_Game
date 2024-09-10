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
    suits = ["hearts", "diamonds", "clubs", "spades"]
    levels = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    
    def __init__(self):
        self.cards = [Card(suite, level) for suite in Deck.suits for level in Deck.levels]
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
        level_values.sort()
        return level_values == list(range(level_values[0], level_values[0] + 3)) or level_values == [2, 3, 14]

    def is_triple(self, levels):
        return levels[0] == levels[1] == levels[2]
    
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
        if self.is_pair(levels):
            return ("pair", self.level_values(levels[0]))

        # If none of the above, return high card
        return ("high-card", self.level_values(levels[-1]))
    

# Function that lets user place bet
def place_bet():
    return int(input("Enter your bet: "))
    
# Function that deals the cards at the beginning of each game and the last third card
def deal_cards(deck, hand, cards):
    for _ in range(cards):
        hand.cards.append(deck.deal_card())

# Function that shows the cards
def show_cards(player, hand, cards):
    face_up_cards = hand.cards[:cards]  # Number of cards that are face-up
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

# Function to determine if the AI will win, lose or draw
def determine_winner(user_hand, computer_hand):

    # Evaluete both hands, it returns what the player has and its highest card
    user_score, user_value = user_hand.evaluate_hand()
    computer_score, computer_value = computer_hand.evaluate_hand()

    # Get a score from the helper function based on what hand they have and compare them
    if hand_rank(user_score) > hand_rank(computer_score):
        return "lose", user_score
    elif hand_rank(user_score) < hand_rank(computer_score):
        return "win", computer_score
    else:
        # If hand ranks are the same, compare the highest card values
        if user_value > computer_value:
            return "lose", user_score
        elif user_value < computer_value:
            return "win", user_score
        else:
            return "draw" ,user_score

# Function that determines the AI move
def ai_move(profit, win_rate, pot):


    # If we know computer is going to win or draw
    if profit < 0:
        if win_rate > 0.7:
            move = random.choices(["call", "raise"], weights=[0.3, 0.7])[0]
            if move == "raise":
                return int(pot*1.5) # Computer makes a raise 
            else:
                return pot
        
        # If we know AI will win but have bad starting cards make a sensible decison with starting cards
        else:
            # We cant to call or raise to make money back
            if profit < 0:
                move = random.choices(["call", "raise"], weights=[0.7, 0.3])[0]
                if move == "raise":
                    return int(pot*1.25)
                else:
                    return pot
            else:
                # If we already in profit we can fold with worse cards
                move = random.choices(["call", "raise", "fold"], weights=[0.3, 0.1, 0.6])[0]
                if move == "raise":
                    return int(pot*1.25)
                elif move == "call":
                    return pot
                else:
                    return 0
    else:
        move = random.choices(["call", "raise"], weights=[0.3, 0.7])[0]
        if move == "raise":
            return int(pot*1.5) # Computer makes a raise 
        else:
            return pot
        
            

def main():
    # Initialize profit for company to 0
    computer_profit = 0

    win = 0
    loss = 0

    while True:

        if win+loss > 1:
            win_rate = win/(win+loss)
        else:
            win_rate = 0.5

        print("New Game!\n")
        # Initialize a deck
        deck = Deck()

        # User places a bet that the AI also starts with
        user_bet = place_bet()
        ai_bet = user_bet

        # Initialize a hand for both user and AI
        user_hand = Hand([])
        computer_hand = Hand([])

        # Deal two cards to both user and computer
        deal_cards(deck, user_hand, 2)
        deal_cards(deck, computer_hand, 2)

        show_cards("User", user_hand, 2)
        show_cards("Computer", computer_hand, 2)

        # User place a second bet
        user_decision = input("\nDo you want to raise? (yes/no): ").lower()

        if user_decision == 'yes':
            additional_bet = place_bet()
            user_bet += additional_bet

        
        ai_bet = ai_move(computer_profit, win_rate, user_bet)

        if ai_bet == user_bet:
            print("Computer called.\n")
        elif ai_bet > user_bet:
            print(f"Computer raised to {ai_bet}.\n")
        else:
            print("Computer folded.\n")
            # If user raised and computer folded. Just subtract original bet
            if user_decision == "yes":
                computer_profit -= (user_bet - additional_bet)
            else:
                computer_profit -= user_bet

            print(f"Current computer profit: {computer_profit}\n")

            play_more = input("Do you want to play another game? (yes/no): \n").lower()
            if play_more == "no":
                break
            else:
                continue

        # If computer raised, user gets a choice to call or fold
        if ai_bet > user_bet:
            user_move = input("\nDo you want to call the raise? (yes/no): ").lower()
            if user_move == "yes":
                user_bet = ai_bet
            else:
                print("User folded. Computer wins this round.\n")
                computer_profit += user_bet
                print(f"Current computer profit: {computer_profit}\n")

                play_more = input("Do you want to play another game? (yes/no): \n").lower()
                if play_more == "no":
                    break
                else:
                    continue
                
        # Deal last card in a normal game
        deal_cards(deck, user_hand, 1)
        deal_cards(deck, computer_hand, 1)

        show_cards("User", user_hand, 3)
        show_cards("Computer", computer_hand, 3)

        result, winning_type = determine_winner(user_hand, computer_hand)
        
        if result == "win":
            computer_profit += user_bet
            print(f"Computer wins the round! {winning_type}\n")
            win +=1
        elif result == "lose":
            computer_profit -= ai_bet
            print(f"User wins the round! {winning_type}\n")
            loss +=1
        else:
            print("It's a draw!\n")

        print(f"Current computer profit: {computer_profit}\n")

        play_more = input("Do you want to play another game? (yes/no): \n").lower()

        if play_more == "no":
            break

main()



