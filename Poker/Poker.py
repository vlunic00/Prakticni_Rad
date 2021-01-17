import sys
import operator
import re
import random
import time


from Settings_Poker import Settings

class Card():
    """Karte za poker"""

    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __repr__(self):
        return str(self.rank) + " of " + self.suit


class Deck():
    """Deck karata"""

    def __init__(self):
        self.cards = [] 
        suits = ["Spades", "Hearts", "Diamonds", "Clubs"]
        ranks = { 2 : "Two",
                  3 : "Three",
                  4 : "Four",
                  5 : "Five",
                  6 : "Six",
                  7 : "Seven",
                  8 : "Eight",       #Dictionary za lakse prepoznat high card
                  9 : "Nine",
                  10 : "Ten",
                  11 : "Jack",
                  12 : "Queen",
                  13 : "King",
                  14 : "Ace"}

        for key in ranks:
            for suit in suits:
                self.cards.append(Card(suit, ranks[key], key))

    def shuffle(self):
        for i in range(3):
            random.shuffle(self.cards)

    def deal(self, location, amount):
        for number in range(amount):
            location.append(self.cards.pop(0))

class Player():
    def __init__(self, name = "Guest"):
        self.name = name
        self.chips = 0
        self.on_table = 0
        self.gap_to_bet = 0
        self.bid = 0
        self.hand = [] 
        self.dealt = [] #probat sa dictionaryem
        self.score = 0
        self.Fold = False
        self.turn = False
        self.done = False
        self.is_all_in = False
        self.won = False
        self.role = []
        self.attributes = []

    def call(self):
        self.chips -= int(self.gap_to_bet)
        self.on_table += int(self.gap_to_bet)
        self.gap_to_bet = 0

    def bet(self, amount):
        amount_int = isinstance(amount, int)

        while amount_int != True:
            amount = int(input("Invalid bet, try again: "))
            amount_int = isinstance(amount, int)
                
        if int(amount) < 0:
            print("Don't try to cheat...")
            print("You have now folded.")
            self.Fold = True
        else: 
            self.chips -= int(amount)
            self.on_table += int(amount)
        if "highest bidder" not in self.attributes:
            self.attributes.append("highest bidder")
        


    def all_in(self):
        self.on_table += self.chips
        self.chips = 0
        self.is_all_in = True

    def fold(self):
        self.Fold = True





class Game(object):
    position_counter = 0 #za new_turn() funkciju

    def __init__(self):
        self.number_of_players = 0
        self.list_of_players = []
        self.players_out = []
        self.cards_on_table = []
        self.game_not_over = True
        self.acting_player = Player()
        self.highest_bidder = Player()
        self.cards = []
        self.pot = 0
        self.round = 0
        self.small_blind_amount = 0
        self.big_blind_amount = 0
        self.highest_bid = self.big_blind_amount
        self.small_blind = Player()
        self.big_blind = Player()
        self.first = Player() 
        self.winners = []
        self.deck = Deck()


        self.number_of_players = int(input("How many players in this game? "))
        while self.number_of_players <= 0 or self.number_of_players > 11:
           self.number_of_players = int(input("Invalid amount, try again (1-11): "))

        for people in range(self.number_of_players): 
            name = input("Please enter the player's name: ")
            self.list_of_players.append(Player(name))

        starting_chips = int(input("Starting chips? "))
        while int(starting_chips) <= 0:
           starting_chips = input("Too low, choose a bigger amount: ")

        self.big_blind_amount = int(starting_chips) / 50
        self.small_blind_amount = int(self.big_blind_amount) / 2  
        print("Each player get's " + str(starting_chips) + " chips")
        print("Big blind: " + str(self.big_blind_amount))
        print("Small blind: " + str(self.small_blind_amount))
        
        answer = input("Do you want to change the blinds? (Y/N) ")
        while answer.lower() != "y" and answer.lower() != "n":
            answer = input("Invalid answer, try again: (Y/N) ")
            
        if answer.lower() == "y":
            self.set_blinds()

        self.highest_bid = int(self.big_blind_amount)
        for player in self.list_of_players:
            player.chips = starting_chips

        
    def set_blinds(self):
        self.big_blind_amount = input("Choose the big blind: ")
        self.small_blind_amount = input("Choose the small blind: ")
            
        while int(self.small_blind_amount) >= int(self.big_blind_amount):
          print("Small blind can't be higher or equal to the big blind, choose again:")
          self.big_blind_amount = input("Big blind: ")
          self.small_blind_amount = input("Small blind: ")

    def set_player_attributes(self):
        position_of_player = 0
        self.small_blind = self.list_of_players[position_of_player]
        self.small_blind.attributes.append("small blind")
        
        position_of_player += 1
        position_of_player %= len(self.list_of_players)

        self.big_blind = self.list_of_players[position_of_player]
        self.big_blind.attributes.append("big blind")

        position_of_player += 1
        position_of_player %= len(self.list_of_players)

        self.first = self.list_of_players[position_of_player]
        self.first.attributes.append("first")
        self.list_of_players.append(self.list_of_players.pop(0)) #da se redosljed promijeni za sljedeci krug
                
    def deal_to_players(self):
        for player in self.list_of_players:
            self.deck.deal(player, 2)

    def flop(self):
        self.deck.deal(self.cards_on_table, 3)
    
    def turn(self):
        self.deck.deal(self.cards_on_table, 1)

    def river(self):
        self.deck.deal(self.cards_on_table, 1)

    def start_round(self):

        self.pot = 0
        self.winners.clear()
        for player in self.list_of_players:
            player.dealt.clear()
            player.on_table = 0
            player.bid = 0
            player.gap_to_bet = 0
            player.Fold = False
        for player in self.list_of_players:
            player.attributes.clear()

        self.set_player_attributes()
       
        print("Round: " + str(self.round))
        print("Players on table:")
        for player in self.list_of_players:        
            print(str(player.name) + str(player.attributes))
            if 'first' in player.attributes: 
                player.turn = True
                self.position_counter = self.list_of_players.index(player)
            if 'small blind' in player.attributes:
                player.chips -= int(self.small_blind_amount)
                player.on_table += int(self.small_blind_amount)
                player.bid += int(self.small_blind_amount)
                self.pot += int(self.small_blind_amount)
            if 'big blind' in player.attributes:
                player.chips -= int(self.big_blind_amount)
                player.on_table += int(self.big_blind_amount)
                player.bid += int(self.big_blind_amount)
                self.pot += int(self.big_blind_amount)
                player.attributes.append("highest bidder")
        
                
        print("-------------------------------------------------")

    def pre_flop(self):
        self.deck.shuffle()
        for player in self.list_of_players:
            for x in range(2):
                player.dealt.append(self.deck.cards.pop(0))

    def live_round(self):

        round_not_over = True

        while round_not_over:
            for player in self.list_of_players:
                if player.turn == True and round_not_over:
                    if player.Fold != True and player.is_all_in != True:
                        self.update_player_status()
                        self.write_state(player)
                        print("\n")
                        self.write_options(player) 
                        self.player_input(player) 
                        self.wipe_with_delay() 

                    player.done = True
                    player.turn = False
                    round_not_over = self.check_if_round_over()
                    self.new_turn()               




    def update_player_status(self):
        for player in self.list_of_players:
            if "highest bidder" in player.attributes:
                player.gap_to_bet = 0
            else:
                player.gap_to_bet = int(self.highest_bid) - int(player.bid)



    def write_state(self, player):

        for person in self.list_of_players:
            if person.turn != True:
                print(person.name.title() + ": " + str(person.chips) + "\tIn pot: " + str(person.on_table))

        print("\n")

        if self.cards_on_table:
            print("CARDS ON TABLE:")
            for card in self.cards_on_table:
                print(card)
        print("\n")

        print("POT:" + str(self.pot))
        print("\n")
        print(player.name.title())
        print("HAND: " + str(player.dealt))
        print("CHIPS: " + str(player.chips))
        print("GAP TO BET: " + str(player.gap_to_bet))
        if player.on_table != 0:
            print("IN POT: " + str(player.on_table))


    def write_options(self, player):
         if player.gap_to_bet == 0:
             print("Check\tBet\tFold\tAll in")
         elif player.gap_to_bet != 0 and player.gap_to_bet < player.chips:
             print("Call\tRaise\tFold\tAll in")
         elif player.gap_to_bet != 0 and player.gap_to_bet > player.chips or player.gap_to_bet == player.chips:
             print("Fold\tAll in")
        

    def player_input(self, player):
        final_action = False

        while final_action != True:
            action = input()
            if action.lower() == "call":
                if player.gap_to_bet != 0 and player.gap_to_bet < player.chips:
                    self.pot += player.gap_to_bet
                    player.bid += player.gap_to_bet
                    player.call()
                    final_action = True
                elif player.gap_to_bet == 0:
                    print("Nothing to call.")
                elif player.gap_to_bet > player.chips or player.gap_to_bet == player.chips:
                    self.pot += player.chips
                    player.bid += player.chips
                    player.all_in()
                    final_action = True

            elif action.lower() == "fold":
                player.fold()
                final_action = True

            elif re.search("bet", action):
                if re.search(r'\d+', action):
                   bet_amount = re.findall(r'\d+', action)
                   if int(bet_amount[0]) > player.chips:
                       if self.highest_bid < player.chips:
                           self.highest_bid = player.chips
                       self.pot += player.chips
                       player.bid += player.chips
                       player.all_in()
                   else:
                       player.bet(int(bet_amount[0]))
                       self.pot += int(bet_amount[0])
                       player.bid += int(bet_amount[0])
                       self.highest_bid = player.bid
                else: 
                    bet_amount = int(input("How much would you like to bet: "))
                    if bet_amount > player.chips:
                       if self.highest_bid < player.chips:
                           self.highest_bid = player.chips
                       self.pot += player.chips
                       player.bid += player.chips
                       player.all_in()
                    else:
                       player.bet(bet_amount)
                       self.pot += bet_amount
                       player.bid += bet_amount
                       self.highest_bid = player.bid

                for people in self.list_of_players:
                    if people.name != player.name and "highest bidder" in people.attributes:
                        people.attributes.remove("highest bidder")

                final_action = True
                
            elif re.search("raise", action):
                if player.gap_to_bet == 0:
                   answer = input("Did you mean bet? (Y/N) ")
                   while answer.lower() != "y" and answer.lower() != "n":
                       answer = input("Invalid answer, try again: ")
                   if answer.lower() != "y":
                       continue
                if re.search(r'\d+', action):
                   raise_amount = re.findall(r'\d+', action)
                   if int(raise_amount[0]) > player.chips:
                       self.pot += player.chips
                       player.bid += player.chips
                       if self.highest_bid < player.chips:
                           self.highest_bid = player.bid
                       player.all_in()
                   else:
                       if int(raise_amount[0]) < player.gap_to_bet:
                           print("Don't try to cheat... ")
                           player.Fold = True
                       else:
                           player.bet(int(raise_amount[0]))
                           self.pot += int(raise_amount[0])
                           player.bid += int(raise_amount[0])
                           self.highest_bid = player.bid
                else: 
                    raise_amount = int(input("How much would you like to raise: "))
                    if raise_amount > player.chips:
                       self.pot += player.chips
                       player.bid += player.chips
                       if self.highest_bid < player.chips:
                           self.highest_bid = player.bid
                       player.all_in()
                    else:
                        if int(raise_amount[0]) < player.gap_to_bet:
                           print("Don't try to cheat... ")
                           player.Fold = True
                        else:
                           player.bet(raise_amount)
                           self.pot += raise_amount
                           player.bid += raise_amount
                           self.highest_bid = player.bid

                for people in self.list_of_players:
                    if people.name != player.name and "highest bidder" in people.attributes:
                        people.attributes.remove("highest bidder")

                final_action = True

            elif action.lower() == "check":
                if player.gap_to_bet != 0:
                    print("Can't check now!")
                else:
                    final_action = True

            elif action.lower() == "all in":
                self.pot += player.chips
                player.bid += player.chips
                if player.chips > self.highest_bid:
                    self.highest_bid = player.bid
                    player.attributes.append("highest bidder")
                    for people in self.list_of_players:
                        if people.name != player.name and "highest bidder" in people.attributes:
                            people.attributes.remove("highest bidder")
                player.all_in()
                final_action = True

            elif re.search("tip the dealer", action):
                if re.search(r'\d+', action):
                   tip = re.findall(r'\d+', action)
                   print("How generous!")
                   player.chips -= int(tip[0])
                else: 
                    tip = int(input("How generous! How much would you like to tip: "))
                    player.chips -= tip


            else:
                print("Unknown action, try again:")


    def wipe(self):

        for _ in range(100):
            print("\n")

    def wipe_with_delay(self):
        time.sleep(3)
        self.wipe()

    def check_if_round_over(self):
        self.update_player_status()
        i = 0
        for player in self.list_of_players:
            if player.done == True and player.gap_to_bet == 0 or player.Fold == True or player.is_all_in == True:
                i += 1

        if i == len(self.list_of_players):
            return False
        else:
            return True

    def new_turn(self):
        self.position_counter += 1
        self.position_counter %= len(self.list_of_players)
        self.list_of_players[self.position_counter].done = False
        self.list_of_players[self.position_counter].turn = True    


    def check_for_winners_pre_river(self):
        for player in self.list_of_players:
            player.done = False
            if player.Fold != True:
                self.winners.append(player)
        if len(self.winners) == 1:
            self.winners[0].chips += self.pot
        else:
            self.winners.clear()


    def check_for_losers(self):
        for player in self.list_of_players:
            if player.chips == 0 and player.is_all_in != True:
                self.players_out.append(self.list_of_players.pop(self.list_of_players.index(player)))

    def check_for_winners(self):
        self.check_hand()
        max_score = 0
        max_value = 0

        for player in self.list_of_players:
            if player.score > max_score:
                max_score = player.score
                self.winners.clear()
                self.winners.append(player)
            elif player.score == max_score:
                self.winners.append(player)
                
        if len(self.winners) == 1:
            self.winners[0].chips += self.pot
        elif len(self.winners) > 1:
            for player in self.winners:
                for card in player.hand:
                    if card.value > max_value:
                        max_value = card.value
                        winner = player
            winner.chips += self.pot

            if winner.score == 0:
                print(winner.name + " won with a high card.")
            elif winner.score == 1:
                print(winner.name + " won with a pair.")
            elif winner.score == 2:
                print(winner.name + " won with two pairs.")
            elif winner.score == 3:
                print(winner.name + " won with three of a kind.")
            elif winner.score == 4:
                print(winner.name + " won with a straight.")
            elif winner.score == 5:
                print(winner.name + " won with a flush.")
            elif winner.score == 6:
                print(winner.name + " won with a full house.")
            elif winner.score == 7:
                print(winner.name + " won with four of a kind.")
            elif winner.score == 8:
                print(winner.name + " won with a straight flush.")
            elif winner.score == 9:
                print(winner.name + " won with a royal flush. WOW!!")

    def check_hand(self):
        pair = False
        two_pair = False
        three_of_a_kind = False
        straight = False
        flush = False
        full_house = False
        four_of_a_kind = False
        straight_flush = False
        royal_flush = False
        
        temp = []
        matching = 0
        max = 0
        pairs = 0
        str_flush = 0
        cards_in_straight = []
        cards_in_flush = []


        for player in self.list_of_players:
            player.hand = player.dealt + self.cards_on_table
            for card in player.hand:
                if card.rank in temp:
                    pairs += 1
                    temp.pop(temp.index(card.rank))
                else:
                    temp.append(card.rank)

            if pairs == 1:
                pair = True
            elif pairs == 2:
                two_pair = True

            for card in player.hand:
                for other in player.hand[player.hand.index(card) + 1:]:
                    if card.rank == other.rank:
                        matching += 1
                if matching > max:
                    max = matching
                matching = 0

            if max == 2:
                three_of_a_kind = True
            elif max == 3:
                four_of_a_kind = True
                
            temp.clear()
            matching = 0
            
            prev_card = player.hand[0]

            player.hand.sort(key = lambda x: x.value)
            for card in player.hand[1:]:
                if card.value == prev_card.value + 1:
                    matching += 1
                    if prev_card.rank not in cards_in_straight:
                        cards_in_straight.append(prev_card.rank) 
                        cards_in_straight.append(card.rank)
                    else:
                        cards_in_straight.append(card.rank)
                    if card.suit == prev_card.suit:
                        str_flush += 1
                else:
                    matching = 0
                    str_flush = 0
                    cards_in_straight.clear()

                prev_card = card

            if matching == 4:
                straight = True
            if str_flush == 4:
                straight_flush = True

            matching = 0

            for card in player.hand:
                for other in player.hand[player.hand.index(card) + 1:]:
                    if card.suit == other.suit:
                        matching += 1
                        cards_in_flush.append(card.rank)
                if matching == 4:
                    flush = True
                    break
                else:
                    matching = 0
                    cards_in_flush.clear()

            if three_of_a_kind == True and two_pair == True:
                full_house = True

            if straight_flush == True and cards_in_straight[0] == "Ten" and cards_in_straight[4] == "Ace":
                royal_flush = True

            if royal_flush == True:
                player.score = 9
            elif straight_flush == True:
                player.score = 8
            elif four_of_a_kind == True:
                player.score = 7
            elif full_house == True:
                player.score = 6
            elif flush == True:
                player.score = 5
            elif straight == True:
                player.score = 4
            elif three_of_a_kind == True:
                player.score = 3
            elif two_pair == True:
                player.score = 2
            elif pair == True:
                player.score = 1
            else:
                player.score = 0


    def check_if_game_over(self):

        if len(self.list_of_players) == 1:
            self.game_not_over = False
            print("Congratulations " + self.list_of_players[0].name.title() + "! You won!!!!")
            for player in self.players_out:
                print(player.name.title() + ",")
            print("Better luck next time!")
    


    def start_game(self):
        self.wipe()
        print("Welcome to Texas Hold'em Poker, please take your seats:")
        print("\n")

        while self.game_not_over:
            self.start_round()
            self.pre_flop()
            self.live_round()
            self.check_for_winners_pre_river()
            self.check_for_losers()
            if self.winners:
                self.round += 1
                if self.round != 0 and self.round % 5 == 0:
                    self.big_blind_amount *= 2
                    self.small_blind_amount *= 2
                continue
            self.flop()
            self.live_round()
            self.check_for_winners_pre_river()
            self.check_for_losers()
            if self.winners:
                self.round += 1
                if self.round != 0 and self.round % 5 == 0:
                    self.big_blind_amount *= 2
                    self.small_blind_amount *= 2
                continue
            self.turn()
            self.live_round()
            self.check_for_winners_pre_river()
            self.check_for_losers()
            if self.winners:
                self.round += 1
                if self.round != 0 and self.round % 5 == 0:
                    self.big_blind_amount *= 2
                    self.small_blind_amount *= 2
                continue
            self.river()
            self.live_round()
            self.check_for_winners()
            for player in self.list_of_players:
                player.is_all_in = False
            self.check_for_losers()
            self.check_if_game_over()
            self.round += 1
            if self.round != 0 and self.round % 5 == 0:
                self.big_blind_amount *= 2
                self.small_blind_amount *= 2




standardDeck = Deck()
standardDeck.shuffle()
game = Game()
game.start_game()
















