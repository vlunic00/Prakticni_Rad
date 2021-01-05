import sys
import pygame
import operator
import re
import random


from Settings_Poker import Settings

class Card():
    """Karte za poker"""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

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

        for name in ranks:
            for suit in suits:
                self.cards.append(Card(suit, ranks[name]))

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
        self.hand = [] 
        self.dealt = [] #probat sa dictionaryem
        self.Fold = False
        self.turn = False
        self.done = False
        self.all_in = False
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
                
        if int(amount) > int(self.chips):
            self.all_in
        elif int(amount) < 0:
            print("Don't try to cheat...")
            print("You have now folded.")
            self.Fold = True
        else: 
            self.chips -= int(amount) + int(self.gap_to_bet)
            self.on_table += int(amount) + int(self.gap_to_bet)
        if "highest bidder" not in self.attributes:
            self.attributes.append("highest bidder")
        


    def all_in(self):
        self.on_table += self.chips
        self.chips = 0
        self.all_in = True

    def fold(self):
        self.Fold = True



class Game(object):
    position_counter = 0 #za new_turn() funkciju

    def __init__(self):
        self.number_of_players = 0
        self.list_of_players = []
        self.players_out = []
        self.cards_on_table = []
        self.game_over = False
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
                self.pot += int(self.small_blind_amount)
            if 'big blind' in player.attributes:
                player.chips -= int(self.big_blind_amount)
                player.on_table += int(self.big_blind_amount)
                self.pot += int(self.big_blind_amount)
                player.attributes.append("highest bidder")

    def pre_flop(self):
        self.deck.shuffle()
        for player in self.list_of_players:
            for x in range(2):
                player.dealt.append(self.deck.cards.pop(0))

        round_not_over = True

        while round_not_over:
            for player in self.list_of_players:
                if player.turn == True and round_not_over:
                    self.update_player_status()
                    self.write_state(player)
                    print("\n")
                    self.write_options(player) 
                    self.player_input(player) 
                    #self.wipe() 
                    player.done = True
                    player.turn = False
                    round_not_over = self.check_if_round_over()
                    self.new_turn()               




    def update_player_status(self):
        for player in self.list_of_players:
            if "highest bidder" in player.attributes:
                player.gap_to_bet = 0
            else:
                player.gap_to_bet = int(self.highest_bid) - int(player.on_table)



    def write_state(self, player):

        for person in self.list_of_players:
            if person.turn != True:
                print(person.name.title() + ": " + str(person.chips) + "\tIn pot: " + str(person.on_table))

        if self.cards_on_table:
            print("CARDS ON TABLE:")
            print(self.cards_on_table.title())
        print("\n")

        print("POT:" + str(self.pot))
        print("\n")
        print(player.name.title())
        print("HAND: " + str(player.dealt))
        print("CHIPS: " + str(player.chips))
        if player.on_table != 0:
            print("IN POT: " + str(player.on_table))


    def write_options(self, player):
         if player.gap_to_bet == 0:
             print("Check\tBet\tFold\tAll in")
         elif player.gap_to_bet != 0 and player.gap_to_bet < player.chips:
             print("Call\tRaise\tFold\tAll in")
         elif player.gap_to_bet != 0 and player.gap_to_bet > player.chips:
             print("Fold\tAll in")

    def player_input(self, player):
        final_action = False

        while final_action != True:
            action = input()
            if action.lower() == "call":
                if player.gap_to_bet != 0 and player.gap_to_bet < player.chips:
                    self.pot += player.gap_to_bet
                    player.call()
                    final_action = True
                elif player.gap_to_bet == 0:
                    print("Nothing to call.")
                elif player.gap_to_bet != 0 and player.gap_to_bet > player.chips:
                    self.pot += player.chips
                    player.all_in()
                    final_action = True

            elif action.lower() == "fold":
                player.fold()
                final_action = True

            elif re.search("bet", action):
                if player.gap_to_bet != 0:
                   answer = input("Did you mean raise? (Y/N) ")
                   while answer.lower() != "y" and answer.lower() != "n":
                       answer = input("Invalid answer, try again: ")
                   if answer.lower() != "y":
                       continue
                if re.search(r'\d+', action):
                   bet_amount = re.findall(r'\d+', action)
                   player.bet(int(bet_amount[0]))
                   self.pot += int(bet_amount[0])
                   self.highest_bid = int(bet_amount[0])
                else: 
                    bet_amount = int(input("How much would you like to bet: "))
                    player.bet(bet_amount)
                    self.pot += bet_amount
                    self.highest_bid = bet_amount

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
                   player.bet(int(raise_amount[0]))
                   self.pot += int(raise_amount[0])
                   self.highest_bid = int(raise_amount[0])
                else: 
                    raise_amount = int(input("How much would you like to raise: "))
                    player.bet(raise_amount)
                    self.pot += raise_amount
                    self.highest_bid = raise_amount

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


    def wipe():
        for i in range(100):
            print("\n")


    def check_if_round_over(self):
        self.update_player_status()
        i = 0
        for player in self.list_of_players:
            if player.done == True and player.gap_to_bet == 0:
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

    def start_game(self):
        #self.wipe()
        print("Welcome to Texas Hold'em Poker, please take your seats:")
        print("\n")
        game_not_over = True

        while game_not_over:
            self.start_round()
            self.pre_flop()
            game_not_over = False




    
        

   #Napravit funkciju za odredit jacinu karata i pobjednika


standardDeck = Deck()
standardDeck.shuffle()
game = Game()
game.start_game()














