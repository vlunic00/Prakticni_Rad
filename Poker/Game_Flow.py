 def pre_flop(self):
        self.deal_to_players()

        for player in self.list_of_players:
            self.write_state(player)
            print("\n")
            self.write_options(player) 



    def write_state(self, player):

        for person in self.list_of_players:
            if person.turn != True:
                print(person.name.title() + ": " + person.chips + "\tIn pot" + person.on_table)

        if self.cards_on_table:
            print("CARDS ON TABLE:")
            print(self.cards_on_table)
        print("\n")

        print("POT:" + self.pot)

        print(player.name.title())
        print("HAND: " + player.dealt)
        print("CHIPS: " + player.chips)
        if player.on_table != 0:
            print("IN POT: " + player.on_table)


    def write_options(self, player):
         if player.gap_to_bet == 0:
             print("Check\tBet\tFold\tAll in")
         elif player.gap_to_bet != 0 and player.gap_to_bet < player.chips:
             print("Call\tRaise\tFold\tAll in")
         elif player.gap_to_bet != 0 and player.gap_to_bet > player.chips:
             print("Call\tFold\tAll in")
