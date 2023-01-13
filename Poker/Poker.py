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
        self.winning_hand = []
        self.high_card = 0
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
        self.folded = 0
        self.small_blind_amount = 0
        self.big_blind_amount = 0
        self.highest_bid = self.big_blind_amount
        self.small_blind = Player()
        self.big_blind = Player()
        self.first = Player() 
        self.winners = []
        self.deck = Deck()


        self.number_of_players = int(input("How many players in this game? "))
        while self.number_of_players < 2 or self.number_of_players > 11:
           self.number_of_players = int(input("Invalid amount, try again (2-11): "))

        for people in range(self.number_of_players): 
            name = input("Please enter the player's name: ")
            self.list_of_players.append(Player(name))

        starting_chips = int(input("Starting chips? "))
        while int(starting_chips) <= 0:
           starting_chips = input("Too low, choose a bigger amount: ")

        self.big_blind_amount = int(starting_chips) / 50
        self.small_blind_amount = int(self.big_blind_amount) / 2  
        print("Each player get's " + str(starting_chips) + " chips")
        print("Big blind: " + str(int(self.big_blind_amount)))
        print("Small blind: " + str(int(self.small_blind_amount)))
        
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
        self.folded = 0
        self.highest_bid = int(self.big_blind_amount)
        for player in self.list_of_players:
            player.dealt.clear()
            player.on_table = 0
            player.bid = 0
            player.gap_to_bet = 0
            player.Fold = False
            player.turn = False
            player.done = False
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
                    if self.folded == len(self.list_of_players) - 1:
                        return

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
                if person.Fold == True:
                    print(person.name.title() + ": " + str(person.chips) + "\tOUT")
                else:
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
                self.folded += 1
                final_action = True

            elif re.search("bet", action):
                if player.gap_to_bet >= player.chips:
                    print("Can't bet, all in or fold!")
                    continue
                if re.search(r'\d+', action):
                   bet_amount = re.findall(r'\d+', action)
                   if int(bet_amount[0]) > player.chips:
                       self.pot += player.chips
                       player.bid += player.chips
                       if self.highest_bid < player.chips:
                           self.highest_bid = player.bid
                       player.all_in()
                   else:
                       player.bet(int(bet_amount[0]))
                       self.pot += int(bet_amount[0])
                       player.bid += int(bet_amount[0])
                       self.highest_bid = player.bid
                else: 
                    bet_amount = int(input("How much would you like to bet: "))
                    if bet_amount > player.chips:
                       self.pot += player.chips
                       player.bid += player.chips
                       if self.highest_bid < player.chips:
                           self.highest_bid = player.bid
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
                if player.gap_to_bet >= player.chips:
                    print("Can't raise, all in or fold!")
                    continue
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
            print(self.winners[0].name.title() + " won!")
            self.winners[0].chips += self.pot
            self.wipe_with_delay()
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
            if player.score > max_score and player.Fold != True:
                max_score = player.score
                self.winners.clear()
                self.winners.append(player)
            elif player.score == max_score:
                self.winners.append(player)
                
        if len(self.winners) == 1:
            self.winners[0].chips += self.pot
        elif len(self.winners) > 1:
            for player in self.winners:
                if player.winning_hand:
                    for card in player.winning_hand:
                        if card > player.high_card:
                            player.high_card = card
                    if player.high_card > max_value:
                        max_value = player.high_card
                    elif player.high_card == max_value:
                        player.high_card = 0
                        max_value = 0
                        for card in player.dealt:
                            if card.value > player.high_card:
                                player.high_card = card.value
                        if player.high_card > max_value:
                            max_value = player.high_card
                else:
                    for card in player.hand:
                        if card > player.high_card:
                            player.high_card = card
                    if player.high_card > max_value:
                        max_value = player.high_card
            for player in self.winners:
                if player.high_card < max_value:
                    self.winners.pop(self.winners.index(player))
            if len(self.winners) == 1:
                self.winners[0].chips += self.pot
            elif len(self.winners) > 1:
                for player in self.winners:
                    player.chips += self.pot / len(self.winners)

        self.wipe()
        print(self.cards_on_table)
        
        if len(self.winners) == 1:
            if self.winners[0].score == 0:
                    print(self.winners[0].name.title() + " won with a high card.")
                    print(self.winners[0].dealt)
            elif self.winners[0].score == 1:
                    print(self.winners[0].name.title() + " won with a pair.")
                    print(self.winners[0].dealt)
            elif self.winners[0].score == 2:
                    print(self.winners[0].name.title() + " won with two pairs.")
                    print(self.winners[0].dealt)
            elif self.winners[0].score == 3:
                    print(self.winners[0].name.title() + " won with three of a kind.")
                    print(self.winners[0].dealt)
            elif self.winners[0].score == 4:
                    print(self.winners[0].name.title() + " won with a straight.")
                    print(self.winners[0].dealt)
            elif self.winners[0].score == 5:
                    print(self.winners[0].name.title() + " won with a flush.")
                    print(self.winners[0].dealt)
            elif self.winners[0].score == 6:
                    print(self.winners[0].name.title() + " won with a full house.")
                    print(self.winners[0].dealt)
            elif self.winners[0].score == 7:
                    print(self.winners[0].name.title() + " won with four of a kind.")
                    print(self.winners[0].dealt)
            elif self.winners[0].score == 8:
                    print(self.winners[0].name.title() + " won with a straight flush.")
                    print(self.winners[0].dealt)
            elif self.winners[0].score == 9:
                    print(self.winners[0].name.title() + " won with a royal flush. WOW!!")
                    print(self.winners[0].dealt)
            
        elif len(self.winners) > 1:
            for winner in self.winners:
                print(winner.name)
            print("Share the pot.")
        time.sleep(7)



    def check_hand(self):
        


        for player in self.list_of_players:
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
            
            player.hand = player.dealt + self.cards_on_table
            
            for card in player.hand:
                if card.value in temp:
                    pairs += 1
                    player.winning_hand.append(temp.pop(temp.index(card.value)))
                else:
                    temp.append(card.value)

            if pairs == 1:
                pair = True
            elif pairs == 2:
                two_pair = True
            elif pairs == 0:
                player.winning_hand.clear()

            temp.clear()

            for card in player.hand:
                for other in player.hand[player.hand.index(card) + 1:]:
                    if card.value == other.value:
                        matching += 1
                        temp.append(card.value)
                if matching > max:
                    max = matching
                matching = 0

            if max == 2:
                three_of_a_kind = True
                player.winning_hand.clear()
                player.winning_hand = temp.copy()
            elif max == 3:
                four_of_a_kind = True
                player.winning_hand.clear()
                player.winning_hand = temp.copy()
                
            temp.clear()
            matching = 0
            

            player.hand.sort(key = lambda x: x.value)
            prev_card = player.hand[0]
            for card in player.hand[1:]:
                if card.value == prev_card.value + 1:
                    matching += 1
                    if prev_card.rank not in temp:
                        temp.append(prev_card.value) 
                        temp.append(card.value)
                    else:
                        temp.append(card.value)
                    if card.suit == prev_card.suit:
                        str_flush += 1
                else:
                    matching = 0
                    str_flush = 0
                    temp.clear()

                prev_card = card

            if str_flush == 4:
                straight_flush = True
                player.winning_hand.clear()
                player.winning_hand = temp.copy()

            elif matching == 4:
                straight = True
                player.winning_hand.clear()
                player.winning_hand = temp.copy()


            matching = 0
            temp.clear()

            for card in player.hand:
                for other in player.hand[player.hand.index(card) + 1:]:
                    if card.suit == other.suit:
                        matching += 1
                        temp.append(card.value)


                if matching == 4:
                    flush = True
                    if str_flush != True or four_of_a_kind != True:
                        player.winning_hand.clear()
                        player.winning_hand = temp.copy()
                    break
                else:
                    matching = 0
                    temp.clear()

            temp.clear()

            if three_of_a_kind == True and two_pair == True:
                full_house = True
                if four_of_a_kind != True:
                    player.winning_hand.clear()
                    for card in player.hand:                #Dodane ce bit samo 4 karte ali nije bitno jer su svi "rankovi"                                                  
                        if card.rank in temp:               #karata isti tako da ce high card bit isti
                            player.winning_hand.append(temp.pop(temp.index(card.value)))
                        else:
                            temp.append(card.value)
                    

            if straight_flush == True and player.winning_hand[0] == 10 and player.winning_hand[4] == 14:
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
                self.cards_on_table.clear()
                if self.round != 0 and self.round % 5 == 0:
                    self.big_blind_amount *= 2
                    self.small_blind_amount *= 2
                continue
            self.turn()
            self.live_round()
            self.check_for_winners_pre_river()
            self.check_for_losers()
            if self.winners:
                self.cards_on_table.clear()
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
            self.cards_on_table.clear()
            if self.round != 0 and self.round % 5 == 0:
                self.big_blind_amount *= 2
                self.small_blind_amount *= 2




standardDeck = Deck()
standardDeck.shuffle()
game = Game()
game.start_game()






