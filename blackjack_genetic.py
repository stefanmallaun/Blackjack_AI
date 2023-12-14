import tkinter as tk
from tkinter import messagebox
import random
import numpy as np

class BlackjackGUI:
    def __init__(self, master, strategy):
        self.master = master
        self.master.title("Blackjack")
        
        self.money = 3000
        self.bet = 100
        self.strategy = strategy
        
        
        self.create_widgets()

    def create_widgets(self):
        self.money_label = tk.Label(self.master, text="Geld: $3000")
        self.money_label.pack()

        self.bet_label = tk.Label(self.master, text="Einsatz: $100")
        self.bet_label.pack()

        self.player_hand_label = tk.Label(self.master, text="Spielerhand: ")
        self.player_hand_label.pack()

        self.dealer_hand_label = tk.Label(self.master, text="Dealerhand: ")
        self.dealer_hand_label.pack()

        self.hit_button = tk.Button(self.master, text="Karte ziehen", command=self.hit)
        self.hit_button.pack()

        self.stand_button = tk.Button(self.master, text="Stehen", command=self.stand)
        self.stand_button.pack()

    def update_labels(self):
        self.money_label.config(text="Geld: ${}".format(self.money))
        self.bet_label.config(text="Einsatz: ${}".format(self.bet))
        self.player_hand_label.config(text="Spielerhand: {}".format(self.player_hand))
        self.dealer_hand_label.config(text="Dealerhand: {}".format(self.dealer_hand))

    def deal_initial_cards(self):
        self.deck = create_deck()
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]
        self.update_labels()

    def hit(self):
        self.player_hand.append(self.deck.pop())
        self.update_labels()

        player_score = calculate_score(self.player_hand)

        if player_score == 21 and len(self.player_hand) == 2:
            messagebox.showinfo("Blackjack", "Blackjack! Du gewinnst!")
            self.money += self.bet * 1.5
            self.play_again()
        elif player_score > 21:
            messagebox.showinfo("Überkauf", "Du hast überkauft. Du verlierst.")
            self.money -= self.bet
            self.play_again()

    def stand(self):
        while calculate_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())

        dealer_score = calculate_score(self.dealer_hand)
        player_score = calculate_score(self.player_hand)

        if dealer_score > 21:
            messagebox.showinfo("Gewinn", "Dealer hat überkauft. Du gewinnst!")
            self.money += self.bet
        elif player_score > dealer_score:
            messagebox.showinfo("Gewinn", "Du gewinnst!")
            self.money += self.bet
        elif player_score == dealer_score:
            messagebox.showinfo("Unentschieden", "Unentschieden")
        else:
            messagebox.showinfo("Verlust", "Du verlierst.")
            self.money -= self.bet

        self.play_again()

    def play_again(self):
        self.bet = 100
        self.update_labels()

        if self.money <= 0:
            messagebox.showinfo("Spiel vorbei", "Du hast kein Geld mehr. Spiel vorbei.")
            self.master.destroy()
        else:
            result = messagebox.askyesno("Nochmal spielen?", "Wollen Sie nochmal spielen?")
            if result:
                self.deal_initial_cards()
            else:
                self.master.destroy()

def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

def calculate_score(hand):
    score = 0
    num_aces = 0

    for card in hand:
        if card['rank'] in ['K', 'Q', 'J']:
            score += 10
        elif card['rank'] == 'A':
            num_aces += 1
        else:
            score += int(card['rank'])

    for _ in range(num_aces):
        if score + 11 <= 21:
            score += 11
        else:
            score += 1

    return score



def fitness(score, bet, remaining_cards):
    """
    Calculate the fitness of a strategy based on the current score, bet, and the number of remaining cards in the deck.
    """
    expected_value = 0
    num_possible_scenarios = 0

    for remaining_card in remaining_cards:
        player_score = score + int(remaining_card['rank'])  # Convert the rank to an integer
        if player_score <= 21:
            # If the player doesn't bust, the dealer has a 50% chance of winning or losing.
            # Therefore, we calculate the expected value based on the score difference between the player and the dealer.
            dealer_score = score + int(remaining_card['rank']) + 10  # Convert the rank to an integer
            expected_value += (player_score - dealer_score) / 2
            num_possible_scenarios += 1

    if num_possible_scenarios == 0:
        # If the player has already busted, the expected value is negative.
        expected_value = -bet

    return expected_value


def select(population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probabilities = [fitness / total_fitness for fitness in fitnesses]
    parent1 = random.choices(population, weights=selection_probabilities, k=1)[0]
    parent2 = random.choices(population, weights=selection_probabilities, k=1)[0]
    return parent1, parent2

def crossover(parent1, parent2):
    child = {}
    for key in parent1.keys():
        child[key] = random.choice([parent1[key], parent2[key]])
    return child

def mutate(strategy, mutation_rate):
    for key in strategy.keys():
        if random.random() < mutation_rate:
            strategy[key] = random.choice(['hit', 'stand', 'double'])
    return strategy

def auto_play(self):
        while not self.is_game_over():
            decision = self.strategy_decision()
            if decision == 'hit':
                self.hit()
            elif decision == 'stand':
                self.stand()
                
def is_game_over(self):
        return calculate_score(self.player_hand) >= 21 or calculate_score(self.dealer_hand) >= 17

def strategy_decision(self):
    return self.strategy['decision1']

def genetic_algorithm(population_size, generations, mutation_rate):
    # Initialize the population.
    population = [{'score': 0, 'bet': 100, 'remaining_cards': create_deck(), 'decision1': 'hit', 'decision2': 'stand'} for _ in range(population_size)]

    for generation in range(generations):
        # Calculate the fitness of each individual in the population.
        fitnesses = [fitness(strategy['score'], strategy['bet'], strategy['remaining_cards']) for strategy in population]

        # Select the best individual as the optimal strategy.
        optimal_strategy = population[np.argmax(fitnesses)]

        # Apply genetic operators to evolve the population.
        for i in range(population_size):
            # Select two parents from the population.
            parent1, parent2 = select(population, fitnesses)

            # Crossover to generate a new individual.
            child = crossover(parent1, parent2)

            # Mutate the new individual.
            child = mutate(child, mutation_rate)

            # Replace the least fit individual in the population with the new individual.
            population[np.argmin(fitnesses)] = child

    return optimal_strategy




if __name__ == "__main__":
    optimal_strategy = genetic_algorithm(population_size=10, generations=5, mutation_rate=0.1)

    root = tk.Tk()
    app = BlackjackGUI(root, optimal_strategy)
    app.deal_initial_cards()
    app.auto_play()
    root.mainloop()