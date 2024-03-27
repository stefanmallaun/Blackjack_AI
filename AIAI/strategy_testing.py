import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import blackjack as bj
import genetic_algorithm as ga


# Adjustable Test Parameters
N = 10000 #Number of turns
BA = 1 #Amount of cash bet each round ($)
Initial_Cash = 100000 #Starting amout of cash for the player ($)


#Defining/Importing Strategies

#Basic Strategy
#Hard Count Strategy
basic_strategy_hard = pd.read_excel(
    io = 'Basic Strategy.xlsx',
    sheet_name = 'Hard',
    index_col = 0,
    engine='openpyxl')
#Soft Count Strategy
basic_strategy_soft = pd.read_excel(
    io = 'Basic Strategy.xlsx',
    sheet_name = 'Soft',
    index_col = 0,
    engine='openpyxl')
#Total Strategy
basic_strategy = [basic_strategy_hard, basic_strategy_soft]

#Genetic Algorithm Strategy
#Hard Count Strategy
genetic_strategy_hard = pd.read_excel(
    io = 'Genetic Algorithm Strategy.xlsx',
    sheet_name = 'Hard',
    index_col = 0,
    engine='openpyxl')
#Soft Count Strategy
genetic_strategy_soft = pd.read_excel(
    io = 'Genetic Algorithm Strategy.xlsx',
    sheet_name = 'Soft',
    index_col = 0,
    engine='openpyxl')
#Total Strategy
genetic_strategy = [genetic_strategy_hard, genetic_strategy_soft]

#Random Strategy
#Hard Count Strategy
random_strategy_hard = pd.DataFrame(np.random.randint(0,2,size=(18,10)),index = [i for i in range(4,22)], columns = [n for n in range(2,12)])
#Soft Count Strategy
random_strategy_soft = pd.DataFrame(np.random.randint(0,2,size=(10,10)), index = [i for i in range(12,22)], columns = [n for n in range(2,12)])
#Total Strategy
random_strategy = [random_strategy_hard, random_strategy_soft]


basic_strategy_cash = np.empty(N, dtype = float)
genetic_strategy_cash = np.empty(N, dtype = float)
random_strategy_cash = np.empty(N, dtype = float)

strategy_dict = {
    'Basic Strategy': basic_strategy,
    'Genetic Strategy': genetic_strategy,
    'Random Strategy': random_strategy
}


for strategy_name, strategy in strategy_dict.items():
    #Instantiate Game Objects
    game_shoe = bj.Shoe(8) #Instantiate object of class Shoe (shoe of cards)
    game_shoe.shuffle() #Shuffle order of array game_shoe.cards
    player = bj.Player(Initial_Cash, strategy) #Instantiate object of class Player with a cash amount of 100$
    dealer = bj.Dealer() #Instantiate object of class Dealer
    entity_list = np.array([player,dealer]) #List of entities(objects of Player and Dealer class)

    #Game Logic
    for turn in range(N):

        #Refill Shoe when number of cards in shoe is low (below 50)
        if len(game_shoe.cards) < 50:
            shoe_add = bj.Shoe(8)
            shoe_add.shuffle()
            game_shoe.cards = np.append(game_shoe.cards,shoe_add.cards)

        #Clear hand and count of each entity in the game
        for entity in entity_list:
            entity.hand = np.array([], dtype = int)
            entity.count = 0

        #Placing of Bets
        player.make_bet(BA)

        #Dealing of Opening Hand + Update Count
        for cards in range(2):
            player.hit(game_shoe)
            dealer.hit(game_shoe)


        #Player's Turn
        while True:
            #Check for Blackjack in Opening Hand
            if len(player.hand) == 2 and player.count == 21:
                player.count = -2
                break
            #Soft Ace --> Hard Ace
            if 11 in player.hand and player.count>21:
                index = np.where(player.hand == 11)[0][0]
                player.hand[index] = player.hand[index] - 10
                player.count = np.sum(player.hand)
            #Player Decision (Hit/Stand)
            move = player.call_strategy(dealer.hand)
            #Player move: Hit
            if move == 1:
                #Deal the player a card & update count
                player.hit(game_shoe)
                #Check if player has a soft ace and if count has gone over 21
                if 11 in player.hand and player.count>21:
                    index = np.where(player.hand == 11)[0][0]
                    player.hand[index] = player.hand[index] - 10
                    player.count = np.sum(player.hand)
                #Bust if count is over 21
                if player.count > 21:
                    player.count = -1
                    break
            #Player move: Stand
            elif move == 0:
                break

        #Dealer's Turn
        while True:
            #Soft ace --> Hard ace
            if 11 in dealer.hand and dealer.count>21:
                index = np.where(dealer.hand == 11)[0][0]
                dealer.hand[index] = dealer.hand[index] - 10
                dealer.count = np.sum(dealer.hand)
            #Dealer Decision (Stand on soft 17)
            #Dealer move: Hit
            if dealer.count < 17:
                dealer.hit(game_shoe)
                #Check if dealer has a soft ace and if count has gone over 21
                if 11 in dealer.hand and dealer.count>21:
                    index = np.where(dealer.hand == 11)[0][0]
                    dealer.hand[index] = dealer.hand[index] - 10
                    dealer.count = np.sum(dealer.hand)
                #Bust if count is over 21
                if dealer.count > 21:
                    dealer.count = -1
                    break
            #Dealer move: Stand
            elif dealer.count >= 17:
                break


        #Payout
        if player.count == -2 and dealer.count != 21: #The player gets a Blackjack and the dealer does not: Win
            player.cash += 2.5 * player.bet
            player.bet = 0
        elif player.count == -1: #The player busts before the dealer: Loss
            player.bet = 0
        elif dealer.count == -1: #The dealer busts & the player does not: Win
            player.cash += 2 * player.bet
            player.bet = 0
        elif player.count == dealer.count: #The player and the dealer have the same count: Tie
            player.cash += player.bet
            player.bet = 0
        elif player.count > dealer.count: #The player has a higher count than the dealer: Win
            player.cash += 2 * player.bet
            player.bet = 0
        else: #The dealer has a higher count than the player: Loss
            player.bet = 0

        #Record Cash Time Series
        if strategy_name == 'Basic Strategy':
            basic_strategy_cash[turn] = player.cash
        elif strategy_name == 'Genetic Strategy':
            genetic_strategy_cash[turn] = player.cash
        elif strategy_name == 'Random Strategy':
            random_strategy_cash[turn] = player.cash


#Display Final Cash Amounts
print(f'Basic Strategy Final Cash: {basic_strategy_cash[-1]}')
print(f'Genetic Strategy Final Cash: {genetic_strategy_cash[-1]}')
print(f'Random Strategy Final Cash: {random_strategy_cash[-1]}')

#Plotting Cash versus Turn Graph
#plt.figure(figsize = [21,9], dpi = 300)

title_font = {
    'family': 'serif',
    'color': 'xkcd:black',
    'size': '20',
    'weight': 'bold'
}
label_font = {
    'family': 'serif',
    'color': 'xkcd:black',
    'size': '16',
    'weight': 'normal'
}

plt.title(label = 'Cash Amount versus Turn', fontdict = title_font)
plt.xlabel(xlabel = 'Turn', fontdict = label_font)
plt.ylabel(ylabel = 'Cash Amount', fontdict = label_font)

plt.plot(basic_strategy_cash, label = 'Basic Strategy')
plt.plot(genetic_strategy_cash, label = 'Genetic Algorithm Strategy')
plt.plot(random_strategy_cash, label = 'Random Strategy')

plt.legend()
plt.show()
