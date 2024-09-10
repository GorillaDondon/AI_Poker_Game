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
    suites = ["hearts", "diamonds", "clubs", "spades"]
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
    
    def trickUsers(self, )

    
# Function that lets user place bet
def place_bet():
    return int(input("Enter your bet: "))
    
# Function that deals the cards at the beginning of each game
def deal_cards(deck):
    return [deck.deal_card() for _ in range(3)]

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
def ai_move(user_hand, computer_hand, prob_win, ai_wins, ai_losses, num_of_games, profit, pot):

    # If AI has way worse cards than user it does not make sense to call or raise if they user bet high.
    if prob_win < 0.2 and pot > 100:
        return 0

    result, winnig_hand = determine_winner(user_hand, computer_hand)

    winning_rate = 0

    if num_of_games == 0:
        winning_rate = 0
    else:
        winning_rate


    print(result)
    # If we know computer is going to win or draw
    if result == "win" or result== "draw":
        if prob_win > 0.7:
            move = random.choices(["call", "raise"], weights=[0.3, 0.7])[0]
            if move == "raise":
                return int(pot*random.uniform(1.3,2)) # Computer makes a raise 
            else:
                return pot
        
        # If we know AI will win but have bad starting cards make a sensible decison with starting cards
        else:
            # We cant to call or raise to make money back
            if profit < 0:
                move = random.choices(["call", "raise"], weights=[0.7, 0.3])[0]
                if move == "raise":
                    return int(pot*random.uniform(1.1,1.5))
                else:
                    return pot
            else:
                # If we already in profit we can fold with worse cards
                move = random.choices(["call", "raise", "fold"], weights=[0.3, 0.1, 0.6])[0]
                if move == "raise":
                    return int(pot*random.uniform(1.1,1.5))
                elif move == "call":
                    return pot
                else:
                    return 0
            
    # If we know computer is going to loose
    else:
        if profit - pot < -300:
            # Play very conservatively when losing money and have low win probability
            move = random.choices(["fold", "call"], weights=[0.8, 0.2])[0]
            if move == "call":
                return pot  # Call
            else:
                return 0  # Fold
        else:
            # If profit is positive, AI might take a risk and call occasionally
            move = random.choices(["fold", "call"], weights=[0.6, 0.4])[0]
            if move == "call":
                return pot  # Call
            else:
                return 0  # Fold
        
    
def calc_probability(user_hands, computer_hands, deck, simulations=5000):
    #t = deepcopy(deck)

    win = 0
    lose = 0
    draw = 0

    # extract visible two cards
    computer_visible = computer_hands.cards[:2]
    user_visible = user_hands.cards[:2]

    # simulate calculating the win, lose, draw probabilities with 5000 random simulations
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
        result, winning_hand = determine_winner(user_hands, computer_hands)
        if result == "win":
            win += 1
        elif result == "lose":
            lose += 1
        else:
            draw += 1

    prob_win = win / simulations

    return prob_win


def main():
    # Initialize profit for company to 0
    computer_profit = 0
    
    # keep track of computer's winning/losing history
    ai_wins = 0
    ai_losses = 0

    # keep track of the total number of played games
    num_of_games = 0

    while True:

        print("New Game!\n")
        num_of_games += 1

        # Initialize a deck
        deck = Deck()

        # User places a bet
        user_bet = place_bet()

        # Deal three cards to both user and computer
        user_cards = deal_cards(deck)
        computer_cards = deal_cards(deck)

        # Evaluate the hand to determine winner
        user_hand = Hand(user_cards)
        computer_hand = Hand(computer_cards)

        show_cards("User", user_hand, 2)
        show_cards("Computer", computer_hand, 2)

        # User place a second bet
        user_decision = input("\nDo you want to raise? (yes/no): ").lower()

        if user_decision == 'yes':
            additional_bet = place_bet()
            user_bet += additional_bet

        # Calcualte the probaility based on the first two cards
        prob_win = calc_probability(user_hand, computer_hand, deck)

        print(prob_win)

        ai_bet = ai_move(user_hand, computer_hand, prob_win, ai_wins, ai_losses, computer_profit, user_bet)

        if ai_bet == user_bet:
            print("Computer called.\n")
        elif ai_bet > user_bet:
            print(f"Computer raised to {ai_bet}.\n")
        else:
            print("Computer folded.\n")

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
                

        show_cards("User", user_hand, 3)
        show_cards("Computer", computer_hand, 3)

        result, winning_type = determine_winner(user_hand, computer_hand)
        
        if result == "win":
            computer_profit += user_bet
            print(f"Computer wins the round! {winning_type}\n")
            ai_wins += 1
        elif result == "lose":
            computer_profit -= ai_bet
            print(f"User wins the round! {winning_type}\n")
            ai_losses += 1
        else:
            print("It's a draw!\n")

        print(f"Current computer profit: {computer_profit}\n")

        play_more = input("Do you want to play another game? (yes/no): \n").lower()

        if play_more == "no":
            break

main()





