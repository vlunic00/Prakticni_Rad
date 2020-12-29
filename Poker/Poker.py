import sys
import pygame
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
        ranks = {"Two": 2,
                 "Three": 3,
                 "Four" : 4,
                 "Five" : 5,
                 "Six" : 6,
                 "Seven" : 7,
                 "Eight" : 8,       #Dictionary za lakse prepoznat high card
                 "Nine" : 9,
                 "Ten" : 10,
                 "Jack" : 11,
                 "Queen" : 12,
                 "King" : 13,
                 "Ace" : 14}

        for name in ranks:
            for suit in suits:
                self.cards.append(Card(suit, ranks[name]))

    def shuffle(self):
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
        self.all_in = False
        self.won = False
        self.role = []
        self.attributes = []


#class Table(object):
    
   # def __init__(self):
   #     self.head = Player()
    #    self.head.name = None
    #    self.head.next = None
    
    #def add(self, player_name):
     #   player = Player(player_name)
      #  current = self.head

       # if self.head.name == None:
           # self.head = player
        #else:
         #   while current.next != self.head:
          #      current = current.next

       # player.next = self.head
        #current.next = player

    #def print(self):
     #   current = self.head
      #  print(current.name, current.chips)
       # while current.next != self.head:
        #    current = current.next
         #  print(current.name, current.chips)

class Game(object):
    def __init__(self):
        self.number_of_players = 0
        self.list_of_players = []
        self.cards_on_table = []
        self.game_over = False
        self.acting_player = Player()
        self.possible_actions = []
        self.cards = []
        self.pot = 0
        self.round = 0
        self.small_blind_amount = 0
        self.big_blind_amount = 0
        self.dealer = Player()
        self.small_blind = Player()
        self.big_blind = Player()
        self.first = Player() #first_actor
        self.winners = []
        self.deck = Deck()


        self.number_of_players = int(input("How many players in this game? "))
        while self.number_of_players <= 0 or self.number_of_players > 11:
           self.number_of_players = int(input("Invalid amount, try again (1-11): "))

        for people in range(self.number_of_players): 
            name = input("Please eneter the player's name: ")
            self.list_of_players.append(Player(name))

        starting_chips = input("Starting chips? ")
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
        self.small_blind = self.listlist_of_players[position_of_player]
        self.small_blind.attributes.append("small blind")
        
        position_of_player += 1
        position_of_player %= len(self.list_of_players)

        self.big_blind = self.list_of_players[position_of_player]
        self.big_blind.attributes.append("big blind")

        position_of_player += 1
        position_of_player %= len(self.list_of_players)

        self.first = self.list_of_players[position_of_player]
        self.first.attributes.append("first")
        self.list_of_players.append(self.list_of_players.pop(0))
                
    def deal_to_players(self):
        for player in self.list_of_players:
            self.deck.deal(player, 2)

    def flop(self):
        self.deck.deal(self.cards_on_table, 3)
    
    def turn(self):
        self.deck.deal(self.cards_on_table, 1)

    def river(self):
        self.deck.deal(self.cards_on_table, 1)
        
        



def run_game():
    #Inicijalizira pygame, Settings i ekran
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Texas Hold'Em")
    

    #Glavna petlja - igra radi dok je petlja aktivna
    while True:
        #Unosi sa misa/tipkovnice
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               sys.exit()
              
        screen.fill(settings.bg_color)
        #refresha ekran
        pygame.display.flip()

#run_game()

standardDeck = Deck()
standardDeck.shuffle()
game = Game()






