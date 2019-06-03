#  File: Poker.py
#  Description: Please Hire Me, Portfolio Project 1
#  Name: Christopher Lee
#  Date Created: 05/08/19
#  Date Last Modified: 05/13/19

import random

class Card (object):
  RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

  SUITS = ('C', 'D', 'H', 'S')

  # constructor
  def __init__ (self, rank = 12, suit = 'S'):
    if (rank in Card.RANKS):
      self.rank = rank
    else:
      self.rank = 12

    if (suit in Card.SUITS):
      self.suit = suit
    else:
      self.suit = 'S'

  # string representation of a Card object
  def __str__ (self):
    if (self.rank == 14):
      rank = 'A'
    elif (self.rank == 13):
      rank = 'K'
    elif (self.rank == 12):
      rank = 'Q'
    elif (self.rank == 11):
      rank = 'J'
    else:
      rank = str (self.rank)
    return rank + self.suit

  # equality tests
  def __eq__ (self, other):
    return self.rank == other.rank

  def __ne__ (self, other):
    return self.rank != other.rank

  def __lt__ (self, other):
    return self.rank < other.rank

  def __le__ (self, other):
    return self.rank <= other.rank

  def __gt__ (self, other):
    return self.rank > other.rank

  def __ge__ (self, other):
    return self.rank >= other.rank

class Deck (object):
  # constructor
  def __init__ (self, num_decks = 1):
    self.deck = []
    for i in range (num_decks):
      for suit in Card.SUITS:
        for rank in Card.RANKS:
          card = Card (rank, suit)
          self.deck.append (card)

  # shuffle the deck
  def shuffle (self):
    random.shuffle (self.deck)

  # deal a card
  def deal (self):
    if (len(self.deck) == 0):
      return None
    else:
      return self.deck.pop(0)
  
  #remove card
  def removeCard (self):
    return self.deck.pop(0)

class Poker (object):
  # constructor
  def __init__ (self, num_players = 3, num_cards = 2):
    self.deck = Deck()
    self.deck.shuffle()
    self.numCards_in_Hand = num_cards
    self.all_hands = [[0]*self.numCards_in_Hand for h in range(num_players)]

    # create the number of Player objects
    self.num_players = num_players
    self.player_list = []
    for i in range (self.num_players):
      player = [self.deck.deal(), self.deck.deal()]
      self.player_list.append (player)

    #deal cards to the players
    for i in range (self.numCards_in_Hand):
      for j in range (num_players):
        self.all_hands[j][i] = self.deck.deal()

  ###simulate the play of poker###
  def play (self):
    #create dictionary of player funds, prompt players how much they would like to buy in
    pokerFunds = {}
    keys = []
    values = []
    #values = [0]*self.num_players
    for g in range(self.num_players):
      keys.append('Player ' + str(g+1))
      values.append(input('Player ' + str(g+1) + ", How much would you like to buy in? "))
    print(keys)
    print(values)
    for h in range(len(keys)):
      pokerFunds[keys[h]] = values[h]
    print (pokerFunds)

    # sort the hands of each player and print
    for i in range (len(self.all_hands)):
      sorted_hand = sorted (self.all_hands[i], reverse = True)
      self.all_hands[i] = sorted_hand
      hand_str = ''
      for card in sorted_hand:
        hand_str = hand_str + str (card) + ' '
      print ('Player ' + str(i + 1) + ': ' + hand_str)

    self.pot = 0
    betArray = [int(0)] * self.num_players
    self.playersPlaying = self.num_players
    self.playerNumbers = list(range(1,self.num_players+1))
    #betting, flop, turn, river
    for round in range(1,5):
      if self.playersPlaying > 1:
        if round == 1:
          self.playerOrder(betArray, round)
          self.promptPlayers(betArray, round)
          self.deck.removeCard() #burn one card from the deck
          table = [self.deck.deal(), self.deck.deal(), self.deck.deal()]
          self.printTable(table)
        elif 3 >= round >= 2:
          self.playerOrder(betArray, round)
          self.promptPlayers(betArray, round)
          self.deck.removeCard()
          table.append(self.deck.deal()) #turn/river
          self.printTable(table)
        else:
          self.playerOrder(betArray, round)
          self.promptPlayers(betArray, round)
    #if one player remaining, s/he wins
    if self.playersPlaying == 1:
      for i in range(self.num_players):
        if betArray[i] != -1:
          print('Player ' + str(i+1) + ' Wins!')

    
  #ask players if bet, call/check, fold
  def promptPlayers(self, betArray, round):
    #add array with player number in it. once player folds, their number is erased
    for i in range(len(self.playerNumbers)):
      if betArray[i] == -1:
        continue
      while True and self.playersPlaying > 1:
        if round == 1:
          ordering = self.bigBlindRight
        else:
          ordering = self.dealerRight
        choice = input('Player ' + str(ordering[i]) + ' (bet, call, check, or fold?): ')
        print(choice)
        if choice == 'bet': #raises bet
          betRaise = int(input('Player ' + str(ordering[i]) + ', how much would you like to raise?: '))
          self.pot += betRaise
          betArray[i] += betRaise
          break
        elif choice.lower() == 'call': #calls raised bet
          self.pot += betRaise
          betArray[i] = max(betArray)
          break
        elif choice.lower() == 'check': #accepts same bet
          break
        elif choice.lower() == 'fold':
          self.playersPlaying -= 1
          betArray[i] = -1
          break
        else: 
          print('Invalid choice, try again')
          choice = input('Player ' + str(ordering[i]) + ' (bet, call, check, or fold?): ')
        break
    #if someone raised after the first better, check new high bid index and recursively prompt players
    #build new array for players not yet asked to raise and iterate through bets
    highestBid = max(betArray)
    if round == 1:
      if highestBid != betArray[self.bigBlindIndex+1]:
        print ("correct this ", highestBid)
    else:
      if highestBid != betArray[self.dealerIndex+1]:
        print ("correct this", highestBid)

    print("Highest bid is ", highestBid)
    print(betArray)
    print(self.playersPlaying)

  #prints whats on the table
  def printTable (self,table):
    print('Table:', end=" ")
    for i in range(len(table)):
      print (str(table[i]), end=" ") 
    print("")
  
  #player roles/ordering
  def playerOrder (self, betArray, round):
    #player 1 is dealer, player 2 is small blind, player 3 is big blind
    self.roleArray = []
    self.dealerIndex = round - 1
    self.bigBlindIndex = self.dealerIndex + 2
    for i in range(self.num_players):
      if betArray[i] != -1:
        self.roleArray.append(i+1) #appends players still playing
      else:
        continue
    #orders [0][1][2] to be [dealer][small blind][big blind] indexes
    self.roleOrder = self.roleArray[self.dealerIndex:] + self.roleArray[:self.dealerIndex] #dealer start
    self.bigBlindRight = self.roleArray[self.bigBlindIndex+1:] + self.roleArray[:self.bigBlindIndex+1] #first better start
    self.dealerRight = self.roleArray[self.dealerIndex+1:] + self.roleArray[:self.dealerIndex+1] #small blind start
    print('Player ' + str(self.roleOrder[0]) + " is dealer.")
    print('Player ' + str(self.roleOrder[1]) + " is small blind.")
    print('Player ' + str(self.roleOrder[2]) + " is big blind.")

  # determine the type of each hand and print
  def hand (self):
    hand_type = []	# create a list to store type of hand
    hand_points = []	# create a list to store points for hand
    
    for j in range(len(self.all_hands)):
      sorted_hand = sorted (self.all_hands[j], reverse = True)
      if self.is_royal(sorted_hand)[0] > 0:
        value = self.is_royal(sorted_hand)
      elif self.is_straight_flush(sorted_hand)[0] > 0:
        value = self.is_straight_flush(sorted_hand)
      elif self.is_four_kind(sorted_hand)[0] > 0:
        value = self.is_four_kind(sorted_hand)
      elif self.is_full_house(sorted_hand)[0] > 0:
        value = self.is_full_house(sorted_hand)
      elif self.is_flush(sorted_hand)[0] > 0:
        value = self.is_flush(sorted_hand)
      elif self.is_straight(sorted_hand)[0] > 0:
        value = self.is_straight(sorted_hand)
      elif self.is_three_kind(sorted_hand)[0] > 0:
        value = self.is_three_kind(sorted_hand)
      elif self.is_two_pair(sorted_hand)[0] > 0:
        value = self.is_two_pair(sorted_hand)
      elif self.is_one_pair(sorted_hand)[0] > 0:
        value = self.is_one_pair(sorted_hand)
      else:
        value = self.is_high_card(sorted_hand)
        
      hand_points.append(value[0])
      hand_type.append(value[1])

    print('')
    for h in range(len(hand_type)):
      print ('Player ' + str(h + 1) + ' : ' + hand_type[h])
      
    # determine winner and print
    order_list = []
    for g in range(len(hand_points)):
      current_list = []
      current_list.append(hand_points[g])
      current_list.append(int(g+1))
      order_list.append(current_list)
    ordered_list = sorted(order_list, key = lambda x:(x[0]), reverse = True)

    #constructs win list
    win_list = [ordered_list[0]]
    for order in range(1,len(ordered_list)):
      if ordered_list[0][0] == ordered_list[order][0]:
        win_list.append(ordered_list[order])

    print('')
    if len(win_list) > 1:
      for w in range(len(win_list)):
        print('Player ' + str(win_list[w][1]) + ' ties.')
    else:
      print('Player ' + str(win_list[0][1]) + ' wins.')
    print('')
        
  # determine if a hand is a royal flush
  # takes as argument a list of 5 Card objects
  # returns a number (points) for that hand
  def is_royal (self, hand):
    same_suit = True
    for i in range (len(hand) - 1):
      same_suit = same_suit and (hand[i].suit == hand[i + 1].suit)

    if (not same_suit):
      return 0, ''

    rank_order = True
    for i in range (len(hand)):
      rank_order = rank_order and (hand[i].rank == 14 - i)

    if (not rank_order):
      return 0, ''

    points = 10 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3
    points = points + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1
    points = points + (hand[4].rank)

    return points, 'Royal Flush'

  #determine if hand is straight flush
  def is_straight_flush (self, hand):
    same_suit = True
    for i in range (len(hand) - 1):
      same_suit = same_suit and (hand[i].suit == hand[i + 1].suit)

    if (not same_suit):
      return 0, ''

    rank_order = True
    for i in range (len(hand)):
      rank_order = rank_order and (hand[i].rank ==  hand[0].rank - i)

    if (not rank_order):
      return 0, ''

    points = 9 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3
    points = points + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1
    points = points + (hand[4].rank)

    return points, 'Straight Flush'

  #determine if hand is four of a kind
  def is_four_kind (self, hand): #four of the same kind and one is different
    four_count = []
    count_four = 0
    same_rank = False
    for i in range (len(hand)):
      if (count_four < 4 and hand[i].rank == hand[2].rank):
        count_four += 1
        four_count.append(hand[i])
        if count_four == 4:
          same_rank = True
      else:
        c5 = hand[i]

    if (not same_rank):
      return 0, ''

    points = 8 * 15 ** 5 + (four_count[0].rank) * 15 ** 4 + (four_count[1].rank) * 15 ** 3
    points = points + (four_count[2].rank) * 15 ** 2 + (four_count[3].rank) * 15 ** 1
    points = points + (c5.rank)

    return points, 'Four of a Kind'

  #determine if hand is full house
  def is_full_house (self, hand): #3 of the same kind and 2 of the same kind
    three_count = []
    two_count = []
    count_three = 0
    same_rank = False

    for i in range (len(hand)):
      if (count_three < 3 and hand[i].rank == hand[2].rank):
        count_three += 1
        if count_three == 3:
          if ((hand[0].rank == hand[1].rank) and (hand[1].rank != hand[2].rank))\
              or ((hand[3].rank == hand[4].rank) and (hand[3].rank != hand[2].rank)):
            same_rank = True
    
    if (not same_rank):
      return 0, ''

    for i in range(len(hand)):
      if (hand[i].rank == hand[2].rank):
        three_count.append(hand[i])
      else:
        two_count.append(hand[i])
        
    points = 7 * 15 ** 5 + (three_count[0].rank) * 15 ** 4 + (three_count[1].rank) * 15 ** 3
    points = points + (three_count[2].rank) * 15 ** 2 + (two_count[0].rank) * 15 ** 1
    points = points + (two_count[1].rank)

    return points, 'Full House'

  #determine if hand is flush
  def is_flush (self, hand):
    same_suit = True
    for i in range (len(hand) - 1):
      same_suit = same_suit and (hand[i].suit == hand[i + 1].suit)

    if (not same_suit):
      return 0, ''
    
    points = 6 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3
    points = points + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1
    points = points + (hand[4].rank)

    return points, 'Flush'

  #determine if hand is straight
  def is_straight (self, hand):
    rank_order = True
    for i in range (len(hand)):
      rank_order = rank_order and (hand[i].rank ==  hand[0].rank - i)

    if (not rank_order):
      return 0, ''

    points = 5 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3
    points = points + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1
    points = points + (hand[4].rank)

    return points, 'Straight'

  #determine if hand is three of a kind
  def is_three_kind (self, hand):
    three_count = []
    two_count = []
    count_three = 0
    same_rank = False
    
    for i in range (len(hand)-1):
      for j in range (i+1,len(hand)):
        if (count_three < 3 and hand[i].rank == hand[j].rank):
          count_three += 1
          if count_three == 3:
            same_rank = True
            break
          
    if (not same_rank):
      return 0, ''

    for i in range(len(hand)):
      if (hand[i].rank == hand[2].rank):
        three_count.append(hand[i])
      else:
        two_count.append(hand[i])
    #two_count.sort(reverse = True)
    #for t in range(len(three_count)):
      #print(three_count[t])
    #for p in range(len(two_count)):
      #print(two_count[p])
    
    points = 4 * 15 ** 5 + (three_count[0].rank) * 15 ** 4 + (three_count[1].rank) * 15 ** 3
    points = points + (three_count[2].rank) * 15 ** 2 + (two_count[0].rank) * 15 ** 1
    points = points + (two_count[1].rank)

    return points, 'Three of a Kind'

  #determine if hand is two pair
  def is_two_pair (self, hand):
    pair = []
    odd = []
    count = 0
    two_pair = False
    for i in range (len(hand) - 1):
      if (count < 2 and hand[i].rank == hand[i + 1].rank):
        count += 1
        pair.append(hand[i])
        pair.append(hand[i+1])
        if count == 2:
          two_pair = True
          break
      
    if (not two_pair):
      return 0, ''

    for j in range (len(hand)):
      if hand[j] not in pair:
        odd.append(hand[j])
    
    pair.sort(reverse = True)  

    points = 3 * 15 ** 5 + (pair[0].rank) * 15 ** 4 + (pair[1].rank) * 15 ** 3
    points = points + (pair[2].rank) * 15 ** 2 + (pair[3].rank) * 15 ** 1
    points = points + (odd[0].rank)

    return points, 'Two Pair'

  # determine if a hand is one pair
  # takes as argument a list of 5 Card objects
  # returns the number of points for that hand
  def is_one_pair (self, hand):
    pair = []
    odd = []
    one_pair = False
    for i in range (len(hand) - 1):
      if (hand[i].rank == hand[i + 1].rank):
        pair.append(hand[i])
        pair.append(hand[i+1])
        one_pair = True

    if (not one_pair):
      return 0, ''

    for j in range (len(hand)):
      if hand[j] not in pair:
        odd.append(hand[j])
        
    odd.sort(reverse = True)

    points = 2 * 15 ** 5 + (pair[0].rank) * 15 ** 4 + (pair[1].rank) * 15 ** 3
    points = points + (odd[0].rank) * 15 ** 2 + (odd[1].rank) * 15 ** 1
    points = points + (odd[2].rank)

    return points, 'One Pair'

  #determines if a hand is a high card
  def is_high_card (self,hand):

    points = 1 * 15 ** 5 + (hand[0].rank) * 15 ** 4 + (hand[1].rank) * 15 ** 3
    points = points + (hand[2].rank) * 15 ** 2 + (hand[3].rank) * 15 ** 1
    points = points + (hand[4].rank)
      
    return points, 'High Card'
        
def main():
  # prompt the user to enter the number of players
  num_players = int (input ('Enter number of players: '))
  while ((num_players < 2) or (num_players > 6)):
    num_players = int (input ('Enter number of players: '))

  # create the Poker object
  game = Poker (num_players)

  # play the game
  game.play()

main()

