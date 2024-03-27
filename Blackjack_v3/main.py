import numpy as np
import random
import copy
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


class Game:
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4
        random.shuffle(self.deck)
        self.game_running = False
        self.cumulative_draw = 0
        self.best_player_score = 0

    def start_game(self, player_list):
        while len([p for p in player_list if not p.burn and not p.stop]) > 1:
            for player in [p for p in player_list if not p.burn and not p.stop]:
                if player.decision(self)[0] == 0:
                    player.stop_game()
                else:
                    self.cumulative_draw += player.draw(self.deck)
                if self.best_player_score < player.points:
                    self.best_player_score = player.points

        winner_table = [p for p in player_list if not p.burn]
        winner_table = sorted(winner_table, key=lambda x: 21 - x.points, reverse=True)

        if len(set([p.points for p in winner_table])) == 1 or not winner_table:
            return 'ko'
        else:
            return winner_table[0].name

class Player:
    def __init__(self, name, model=None):
        self.stop = False
        self.burn = False
        self.points = 0
        self.name = name
        self.model = model

    def decision(self, game_obj):
        x = np.array([self.points, game_obj.best_player_score, game.cumulative_draw]).reshape(1, 3)
        predicted_class = game_obj.model.predict_classes(x)
        return to_categorical(predicted_class, 2)[0]

    def stop_game(self):
        self.stop = True

    def draw(self, deck_game):
        card = deck_game.pop()
        self.points += card
        if card == 11 and self.points > 21:
            self.points -= 10
        if self.points > 21:
            self.burn = True
        return card

def create_model():
    model = Sequential()
    model.add(Dense(64, input_dim=3, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(2, activation='softmax'))

    model.compile(
        loss='categorical_crossentropy',
        optimizer='adam',
        metrics=['accuracy']
    )
    return model

def train_population(population, num_matches_per_individual=100, num_epochs=10, batch_size=10):
    best_and_mean_scores = []

    for i_n in range(num_epochs):
        fitness = []

        for ai in population:
            ai.model = create_model()

            game = Game()
            lucas = Player('Lucas')

            matches_won = 0

            for _ in range(num_matches_per_individual):
                ai.points = 0
                ai.stop = False

                x_train = np.array([
                    [ai.points, lucas.points, game.cumulative_draw]
                    for _ in range(num_epochs)
                ]).reshape(-1, 3)

                y_train = to_categorical(1 if lucas.points < 17 else 0, 2)

                ai.model.fit(
                    x_train,
                    y_train,
                    epochs=1,
                    batch_size=1,
                    verbose=0
                )

                if Lucas.game_running and ai.points < 17 and Lucas.best_player_score < 17:
                    ai.model.fit(
                        x_train,
                        y_train,
                        epochs=9,
                        batch_size=1,
                        verbose=0
                    )

                winner = game.start_game([ai, lucas])
                matches_won += 1 if winner == ai.name else 0

            fitness.append(matches_won / num_matches_per_individual * 100)

        mean_fitness = np.mean(fitness)
        best_fitness = max(fitness)

        print(
            f"Epoch {i_n+1} - Mean fitness: {mean_fitness} - Best fitness: {best_fitness}")

        best_and_mean_scores.append([best_fitness, mean_fitness])

    return best_and_mean_scores

def main():
    Lucas = Player('Lucas')
    population = [Player('AI') for _ in range(10)]

    best_and_mean_scores = train_population(population)

# Execute main
if __name__ == '__main__':
    main()