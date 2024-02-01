import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import logistic
import pandas as pd
import copy
from random import shuffle, sample
import random
from tqdm import tqdm

# Die Klasse "Game" repräsentiert den Spielzustand und die Funktionalität
class Game:
    def __init__(self):
        # Initialisiere ein Kartendeck und mische es
        self.deck = list(range(1, 11)) * 4
        shuffle(self.deck)
        self.game_running = False
        self.cumulative_draw = 0
        self.best_player_score = 0

    # Methode, um das Spiel mit einer Liste von Spielern zu starten
    def start_game(self, player_list):
        while len([p for p in player_list if p.burn == False and p.stop == False]) > 1:
            for player in [p_t for p_t in player_list if p_t.burn == False and p_t.stop == False]:
                if player.decision(self)[0] == 0:
                    player.stop_game()
                else:
                    self.cumulative_draw += player.draw(self.deck)
                if self.best_player_score < player.points:
                    self.best_player_score = player.points

        winner_table = [p_e for p_e in player_list if p_e.burn == False]
        winner_table = sorted(winner_table, key=lambda x: 21 - x.points)

        if set([p_end.points for p_end in winner_table]) == 1 or not winner_table:
            return 'ko'
        else:
            return winner_table[0].name

# Die Klasse "Player" repräsentiert einen Spieler mit grundlegenden spielbezogenen Funktionen
class Player:
    def __init__(self, name):
        self.stop = False
        self.burn = False
        self.points = 0
        self.name = name
        self.neural_network = None

    # Entscheidungsfunktion des Spielers (hier zufällig zwischen 0 und 1)
    def decision(self, game_obj):
        out = sample([0, 1], 1)
        return out

    # Beendet das Spiel für den Spieler
    def stop_game(self):
        self.stop = True

    # Zieht eine Karte für den Spieler vom Deck und aktualisiert Punkte und Burn-Status
    def draw(self, deck_game):
        card = deck_game.pop()
        self.points += card
        if self.points > 21:
            self.burn = True
        return card

# Die Klasse "First_strategy" erbt von "Player" und implementiert eine einfache Strategie
class First_strategy(Player):
    def decision(self, game_obj):
        if self.points < 15:
            return [1]
        else:
            return [0]

# Die Klasse "Second_strategy" erbt von "Player" und implementiert eine andere einfache Strategie
class Second_strategy(Player):
    def decision(self, game_obj):
        return [1]

# Die Klasse "Network" repräsentiert ein einfaches neuronales Netzwerk für Entscheidungen
class Network:
    def __init__(self, input_number=2):
        self.l_1 = np.random.uniform(-1, 1, [10, input_number])
        self.l_2 = np.random.uniform(-1, 1, [10, 10])
        self.l_end = np.random.uniform(-1, 1, [1, 10])
        self.layers_stack = [self.l_1, self.l_2, self.l_end]

    # Sigmoid-Aktivierungsfunktion
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    # Vorwärtsdurchlauf durch das neuronale Netzwerk
    def forward(self, input_value):
        res_l1 = np.array([self.sigmoid(l1_s) for l1_s in input_value.dot(self.l_1.T)])
        res_l2 = np.array([self.sigmoid(l2_s) for l2_s in res_l1.dot(self.l_2.T)])
        res_end = np.array([self.sigmoid(l_r) for l_r in res_l2.dot(self.l_end.T)])
        return res_end

    # Mutation einer Gewichtung in einer Schicht
    def mutate(self, layer):
        index_to_mutate = [np.random.randint(layer.shape[0]), np.random.randint(layer.shape[1])]
        layer[index_to_mutate[0], index_to_mutate[1]] += np.random.uniform(-0.01, 0.01)

    # Mutation aller Gewichtungen in allen Schichten
    def mutate_all_layers(self):
        for l in self.layers_stack:
            self.mutate(l)

# Die Klasse "Neural_strategy" erbt von "Player" und implementiert einen Spieler mit neuronalem Netzwerk
class Neural_strategy(Player):
    def decision(self, game_obj):
        best_rank_player = game_obj.best_player_score
        output_array = self.neural_network.forward(
            np.array([self.points, best_rank_player, game_obj.cumulative_draw])
        )
        rounded_output_array = np.round(output_array)
        result = [int(rounded_value) for rounded_value in rounded_output_array]
        return result

    # Initialisiert die Aktivität des neuronalen Netzwerks
    def init_neural_activity(self):
        self.neural_network = Network(input_number=3)

    # Setzt den Status des Spielers zurück
    def reset_status(self):
        self.stop = False
        self.burn = False
        self.points = 0

# Liste zur Speicherung der Ergebnisse jedes Spiels
matchs = []

# Simulation von 100 Spielen
for x in range(100):
    # Initialisiere ein Spiel und Spieler mit verschiedenen Strategien
    jogo = Game()
    lucas = First_strategy('Lucas')
    miura = Player('Miura')
    sergio = Second_strategy('Sergio')

    # Starte das Spiel mit den festgelegten Spielern
    matchs.append(jogo.start_game([lucas, miura, sergio]))

# Gib die Anzahl der Siege von 'Miura' aus und die Ergebnisse aller Spiele
print(len([m for m in matchs if m == 'Miura']))
print(matchs)

# Simulation eines genetischen Algorithmus zur Schulung von neuronalen Netzwerkspielern
best_and_mean_scores = []
p_size = 500
population = [Neural_strategy('AI') for n in range(0, p_size)]

# Initialisiere die Gewichtungen des neuronalen Netzwerks für jeden Spieler in der Population
[p.init_neural_activity() for p in population]

# Führe den genetischen Algorithmus für 10 Iterationen aus
for i_n in range(10):
    fitness = []
    for ai in tqdm(population):
        matchs = []
        f = 0
        for x in range(60):
            jogo = Game()
            lucas = First_strategy('Lucas')
            matchs.append(jogo.start_game([ai, lucas]))
            ai.reset_status()
        f = 100 * (len([m for m in matchs if m == 'AI']) / float(len(matchs)))
        fitness.append(f)

    higher_fitness = sorted([[f, p_f] for f, p_f in zip(fitness, population)], key=lambda s: s[0])
    print('Iteration MEAN:', np.mean([v[0] for v in higher_fitness]))
    loss_str = 'Best value: {}'.format(str(higher_fitness[-1][0]))
    best_and_mean_scores.append([higher_fitness[-1][0], np.mean([v[0] for v in higher_fitness])])
    itr_str = 'Iteration: {}'.format(str(i_n))
    print(itr_str, loss_str)
    best_creatures = higher_fitness[-10:]
    population = [copy.deepcopy(random.choice(best_creatures)[1]) for i in range(0, p_size)]
    [p_m.neural_network.mutate_all_layers() for p_m in population]

# DataFrame zur Speicherung der besten und durchschnittlichen Ergebnisse
df_training = pd.DataFrame(best_and_mean_scores, columns=['best_result', 'mean_result'])

# Plot der durchschnittlichen Ergebnisse über den Iterationen
plt.plot(df_training['mean_result'], color='red', lw=2)
plt.title('Durchschnitt % der gewonnenen Spiele pro Iteration')
plt.xlabel('Iterationsnummer')
plt.show()

# Plot der besten Ergebnisse über den Iterationen
plt.plot(df_training['best_result'], color='blue', lw=2)
plt.title('% der gewonnenen Spiele - NUR BESTE ERGEBNISSE')
plt.xlabel('Iterationsnummer')
plt.show()
