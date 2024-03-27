#Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import blackjack as bj

#Defining Genetic Algorithm Components
class Individual:
    def __init__(self,strategy):
        self.strategy = strategy
        self.fitness = 0

#Create randomized strategy
def create_strategy():
     hard = pd.DataFrame(np.random.randint(0,2,size=(18,10)),index = [i for i in range(4,22)], columns = [n for n in range(2,12)])
     soft = pd.DataFrame(np.random.randint(0,2,size=(10,10)), index = [i for i in range(12,22)], columns = [n for n in range(2,12)])
     return [hard,soft]

#Create population of N individuals with randomized strategies
def create_population(N):
    population_df = pd.DataFrame(columns = ['individual','fitness'])
    population_df['individual'] = [Individual(create_strategy()) for i in range(N)]
    return population_df

#Evaluate and record fitness of population
def fitness(population_df, simulation_turns):

    
    N = simulation_turns 
    BA = 1 
    Initial_Cash = 100000 

    for individual in population_df['individual']:
    # Spielobjekte instanziieren
        game_shoe = bj.Shoe(8)  # Instanz eines Kartendecks erstellen
        game_shoe.shuffle()  # Reihenfolge der Karten im Deck mischen
        player = bj.Player(Initial_Cash, individual.strategy)  # Instanz eines Spielers mit einem Startguthaben von 100,000 erstellen
        dealer = bj.Dealer()  # Instanz eines Dealers erstellen
        entity_list = np.array([player, dealer])  # Liste von Entitäten (Objekten der Klassen Player und Dealer)

        # Spiellogik
        for turn in range(N):

            # Deck auffüllen, wenn die Anzahl der Karten im Schuh niedrig ist (unter 50)
            if len(game_shoe.cards) < 50:
                shoe_add = bj.Shoe(8)
                shoe_add.shuffle()
                game_shoe.cards = np.append(game_shoe.cards, shoe_add.cards)

            # Hand und Zähler aller Entitäten im Spiel löschen
            for entity in entity_list:
                entity.hand = np.array([], dtype=int)
                entity.count = 0

            # Einsätze platzieren
            player.make_bet(BA)

            # Austeilen der Startkarten und Aktualisierung des Zählers
            for cards in range(2):
                player.hit(game_shoe)
                dealer.hit(game_shoe)

            # Zug des Spielers
            while True:
                # Überprüfen auf Blackjack in den Startkarten
                if len(player.hand) == 2 and player.count == 21:
                    player.count = -2
                    break
                # Weicher Ass --> Hartes Ass
                if 11 in player.hand and player.count > 21:
                    index = np.where(player.hand == 11)[0][0]
                    player.hand[index] = player.hand[index] - 10
                    player.count = np.sum(player.hand)
                # Spielerentscheidung (Karte nehmen/Stoppen)
                move = player.call_strategy(dealer.hand)
                # Spielerzug: Karte nehmen
                if move == 1:
                    # Spieler eine Karte geben und Zähler aktualisieren
                    player.hit(game_shoe)
                    # Überprüfen, ob Spieler ein weiches Ass hat und der Zähler über 21 liegt
                    if 11 in player.hand and player.count > 21:
                        index = np.where(player.hand == 11)[0][0]
                        player.hand[index] = player.hand[index] - 10
                        player.count = np.sum(player.hand)
                    # Überkaufen, wenn der Zähler über 21 liegt
                    if player.count > 21:
                        player.count = -1
                        break
                # Spielerzug: Stoppen
                elif move == 0:
                    break

            # Zug des Dealers
            while True:
                # Weiches Ass --> Hartes Ass
                if 11 in dealer.hand and dealer.count > 21:
                    index = np.where(dealer.hand == 11)[0][0]
                    dealer.hand[index] = dealer.hand[index] - 10
                    dealer.count = np.sum(dealer.hand)
                # Dealerentscheidung (Stehen auf weichem 17)
                # Dealerzug: Karte nehmen
                if dealer.count < 17:
                    dealer.hit(game_shoe)
                    # Überprüfen, ob der Dealer ein weiches Ass hat und der Zähler über 21 liegt
                    if 11 in dealer.hand and dealer.count > 21:
                        index = np.where(dealer.hand == 11)[0][0]
                        dealer.hand[index] = dealer.hand[index] - 10
                        dealer.count = np.sum(dealer.hand)
                    # Überkaufen, wenn der Zähler über 21 liegt
                    if dealer.count > 21:
                        dealer.count = -1
                        break
                # Dealerzug: Stoppen
                elif dealer.count >= 17:
                    break


            #Auszahlung
            if player.count == -2 and dealer.count != 21: #Spieler Blackjack - Dealer verliert
                player.cash += 2.5 * player.bet
                player.bet = 0
            elif player.count == -1: #Spiele Bust
                player.bet = 0
            elif dealer.count == -1: #Dealer Bust
                player.cash += 2 * player.bet
                player.bet = 0
            elif player.count == dealer.count: #Unentschieden
                player.cash += player.bet
                player.bet = 0
            elif player.count > dealer.count: #Spieler höheren Count
                player.cash += 2 * player.bet
                player.bet = 0
            else: #Niederlage
                player.bet = 0

        #Temporäre Fitnessstand speichern
        population_df['fitness'].loc[population_df['individual'] == individual] = player.cash - Initial_Cash
        population_df['fitness'] = pd.to_numeric(population_df['fitness'])

#Scores auswählen, welche am Besten sind
def selection(population_df):
    selected_individuals = []

    for i in range(population_df.shape[0]//4):
        tourney_set = population_df[4*i:4*i+4]
        selected_individuals.append(tourney_set['individual'][tourney_set['fitness'].idxmax()])

    return selected_individuals

# Input zwei Individuen und produziere zwei Kinder-Individuen
def crossover(parent_1, parent_2):
    # Zufällig generierte Slices für das Crossover
    x_slice = random.randint(2, 10)
    y_slice_hard = random.randint(4, 20)
    y_slice_soft = random.randint(12, 20)

    # Platzhaltervariablen für die Strategien der Nachkommen
    offspring_strategy_1 = [0, 0]
    offspring_strategy_2 = [0, 0]

    # Hard-Strategien der Nachkommen 
    offspring_strategy_1[0] = pd.concat([
        parent_1.strategy[0].loc[:, 2:x_slice].loc[4:y_slice_hard].join(parent_2.strategy[0].loc[:, x_slice + 1:11].loc[4:y_slice_hard]),
        parent_2.strategy[0].loc[:, 2:x_slice].loc[y_slice_hard + 1:21].join(parent_1.strategy[0].loc[:, x_slice + 1:11].loc[y_slice_hard + 1:21])
    ])
    offspring_strategy_2[0] = pd.concat([
        parent_2.strategy[0].loc[:, 2:x_slice].loc[4:y_slice_hard].join(parent_1.strategy[0].loc[:, x_slice + 1:11].loc[4:y_slice_hard]),
        parent_1.strategy[0].loc[:, 2:x_slice].loc[y_slice_hard + 1:21].join(parent_2.strategy[0].loc[:, x_slice + 1:11].loc[y_slice_hard + 1:21])
    ])

    # Soft-Strategien der Nachkommen
    offspring_strategy_1[1] = pd.concat([
        parent_1.strategy[1].loc[:, 2:x_slice].loc[12:y_slice_soft].join(parent_2.strategy[1].loc[:, x_slice + 1:11].loc[12:y_slice_soft]),
        parent_2.strategy[1].loc[:, 2:x_slice].loc[y_slice_soft + 1:21].join(parent_1.strategy[1].loc[:, x_slice + 1:11].loc[y_slice_soft + 1:21])
    ])
    offspring_strategy_2[1] = pd.concat([
        parent_2.strategy[1].loc[:, 2:x_slice].loc[12:y_slice_soft].join(parent_1.strategy[1].loc[:, x_slice + 1:11].loc[12:y_slice_soft]),
        parent_1.strategy[1].loc[:, 2:x_slice].loc[y_slice_soft + 1:21].join(parent_2.strategy[1].loc[:, x_slice + 1:11].loc[y_slice_soft + 1:21])
    ])

    # Rückgabe der Nachkommen-Individuen
    return [Individual(offspring_strategy_1), Individual(offspring_strategy_2)]

# Erzeuge eine Population von reproduzierten Individuen aus den ausgewählten Individuen der vorherigen Population
def reproduction(selected_individuals, population_size):
    next_generation = []

    # Schleife durch die Anzahl der benötigten reproduzierten Individuen
    for i in range(population_size // 8):
        parent_1 = selected_individuals[2 * i]
        parent_2 = selected_individuals[2 * i + 1]

        # Schleife durch die Anzahl der benötigten Crossover
        for n in range(4):
            # Führe Crossover durch und füge Nachkommen der nächsten Generation hinzu
            next_generation.extend(crossover(parent_1, parent_2))
    
    # Mische die nächste Generation zufällig
    random.shuffle(next_generation)

    # Rückgabe der nächsten Generation von Individuen
    return next_generation
