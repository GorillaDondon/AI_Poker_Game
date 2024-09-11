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
        return levels[0] == levels[1] or levels[1] == levels[2] or levels[0] == levels[2]
        
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
    

    def cheat(self, deck):

        # Gets the suite and level of cards in the user or computer hands 
        levels = sorted([self.level_values(card.level) for card in self.cards])
        suits = [card.suit for card in self.cards]

        # Cheat for flush
        print("Cheating: ", suits[0], suits[1])
        if suits[0] == suits[1]:
            for card in deck.cards:
                print(card.suit, suits[0])
                if card.suit == suits[0]:
                    self.cards.append(card)
                    deck.cards.remove(card)
                    return True
            return False

        # Cheat for triple    
        if levels[0] == levels[1]:
            for card in deck.cards:
                card_value = self.level_values(card.level)  # Convert card level to integer for comparison
                if card_value == levels[0]:
                    self.cards.append(card)
                    deck.cards.remove(card)
                    return True
            return False

                    
        # Cheat for straight
        if (self.level_values(self.cards[0].level) + 1) == self.level_values(self.cards[1].level):
            # Check for a card that would complete a straight
            for card in deck.cards:
                card_level_value = self.level_values(card.level)
                
                # Check if the card can complete a straight, considering Ace as both low and high
                if (card_level_value == levels[1] + 1 or card_level_value == levels[0] - 1 or
                    (levels == [2, 3] and card.level == 'A')):
                    self.cards.append(card)
                    deck.cards.remove(card)
                    return True
            return False

        # Cheat for pair
        if levels[0] != levels[1] and suits[0] != suits[1]:
            random_card = random.choice([levels[0], levels[1]]) # Get highest card
            for card in deck.cards:
                card_value = self.level_values(card.level)  # Convert card level to integer for comparison
                if card_value == random_card:
                    self.cards.append(card)
                    deck.cards.remove(card)
                    return True
            return False
                
# Function that lets user place bet
def place_bet():
    return int(input("Enter your bet: "))
    
# Function that deals the cards at the beginning of each game and the last third card
def deal_cards(deck, hand, cards):
    for _ in range(cards):
        hand.cards.append(deck.deal_card())

# Function that shows the cards
def show_cards(player, hand):
    face_up_str = ', '.join([f"{card.level} of {card.suit}" for card in hand.cards])
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

# Function to determine if the AI will win, lose or draw and return how they won
def determine_winner(user_hand, computer_hand):

    # Evaluete both hands, it returns what the player has and its highest card e.g (straight, 7)
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
def ai_move(pot, should_cheat, prob_win):

    # If we know computer is going to cheat to win
    if should_cheat:
            move = random.choices(["call", "raise"], weights=[0.3,0.7])[0]
            if move == "raise":
                return int(pot*1.5) # Computer makes a raise 
            else:
                return pot 
        
    else:
        if prob_win > 0.65:
            move = random.choices(["call", "raise"], weights=[0.4,0.6])[0]
            if move == "raise":
                return int(pot*1.5) # Computer makes a raise 
            else:
                return pot
        elif prob_win < 0.3:
            return 0
        else:
            move = random.choices(["call", "raise", "fold"], weights=[0.5, 0.2, 0.3])[0]
            if move == "raise":
                return int(pot*1.5) # Computer makes a raise 
            elif move == "call":
                return pot
            else:
                return 0

# Function that checks the strength of the first state with only 2 cards showing
def calc_probability(user_hands, computer_hands, deck, simulations=5000):

    win = 0
    lose = 0
    draw = 0

    # extract visible two cards
    computer_visible = computer_hands.cards
    user_visible = user_hands.cards

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

    # Keep track of wins and losses
    win = 0
    loss = 0

    while True:

        # Initialize win rate to 0.5
        if win+loss > 1:
            win_rate = win/(win+loss)
        else:
            win_rate = 0.5

        # Initialize a deck
        print("New Game!\n")
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

        show_cards("User", user_hand)
        show_cards("Computer", computer_hand)

        # User place a second bet or not
        user_decision = input("\nDo you want to raise? (yes/no): ").lower()

        if user_decision == 'yes':
            additional_bet = place_bet()
            user_bet += additional_bet

        # Calculates the strength of hands with first two cards for AI to make a reasonable desicion
        prob_win = calc_probability(user_hand, computer_hand, deck)

        # Check for cheating condition based on win rate or negative profit
        should_cheat = (win_rate < 0.5 or computer_profit < -250)

        # 66% chance to cheat when conditions are met and the first two cards are not really bad
        ai_cheated = False
        if should_cheat and random.random() < 0.66 and prob_win > 0.15: 
            print("AI is about to cheat")
            ai_cheated = computer_hand.cheat(deck)  # AI cheats by modifying its hand

        # AI makes a move depending on should_cheat and strenght of first 2 cards
        ai_bet = ai_move(user_bet, should_cheat, prob_win)

        if ai_bet == user_bet:
            print("Computer called.\n")
        elif ai_bet > user_bet:
            print(f"Computer raised to {ai_bet}.\n")

            user_move = input("\nDo you want to call the raise? (yes/no): ").lower()
            if user_move == "yes":
                user_bet = ai_bet
            else:
                print("User folded. Computer wins this round.\n")
                computer_profit += user_bet
                win +=1
                print(f"Current computer profit: {computer_profit}\n")

                play_more = input("Do you want to play another game? (yes/no): \n").lower()
                if play_more == "no":
                    break
                else:
                    continue
        else:
            print("Computer folded.\n")
            loss +=1
            # If user raised and computer folded. Just subtract stating bet
            if user_decision == "yes":
                computer_profit -= (user_bet - additional_bet)
            else:
                computer_profit-= user_bet
            
            print(f"Current computer profit: {computer_profit}\n")

            play_more = input("Do you want to play another game? (yes/no): \n").lower()
            if play_more == "no":
                break
            else:
                continue
   
        # If plaiyng a normal game just hand both the last card. Else if cheated the AI already have been given a card in ai_move function
        if not ai_cheated:
            deal_cards(deck, user_hand, 1)
            deal_cards(deck, computer_hand, 1)
        else:
            deal_cards(deck, user_hand, 1)

        # Display final cards
        show_cards("User", user_hand)
        show_cards("Computer", computer_hand)

        # From the final cards determine who won and with what hand
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



