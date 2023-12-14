import tkinter as tk
from tkinter import messagebox
import random
import Blackjack_V1
import numpy as np
from deap import base, creator, tools, algorithms

from blackjack_genetic import genetic_algorithm

class BlackjackAI:
    
    def __init__(self, strategy):
        self.q_values = {}
        self.gamma = 0.9
        self.epsilon = 0.1
        self.alpha = 0.1

    def get_state(self, player_hand, dealer_hand):
        # Vereinfachte Darstellung des Spielzustands
        return (tuple(player_hand), dealer_hand[0])

    def get_q_value(self, state):
        if state not in self.q_values:
            self.q_values[state] = {'hit': 0, 'stand': 0}
        return self.q_values[state]

    def update_q_values(self, old_state, action, reward, new_state):
        future_q_value = self.get_q_value(new_state)['hit' if action == 'hit' else 'stand']
        current_q_value = self.get_q_value(old_state)[action]

        self.q_values[old_state][action] = current_q_value + self.alpha * (reward + self.gamma * future_q_value - current_q_value)

    def choose_action(self, player_hand, dealer_hand):
        state = self.get_state(player_hand, dealer_hand)

        if random.random() < self.epsilon:
            return random.choice(['hit', 'stand'])
        else:
            return self.strategy['decision1']  # Use the strategy decision instead of Q-values

        
    def get_reward(self, player_hand, dealer_hand):
        if self.check_winner(player_hand, dealer_hand) == 'player':
            return 1
        elif self.check_winner(player_hand, dealer_hand) == 'dealer':
            return -1
        else:
            return 0
        
    def check_winner(self, player_hand, dealer_hand):
        player_total = sum(player_hand)
        dealer_total = sum(dealer_hand)

        if player_total > 21:
            return 'dealer'
        elif dealer_total > 21:
            return 'player'
        elif player_total > dealer_total:
            return 'player'
        elif dealer_total > player_total:
            return 'dealer'
        else:
            return 'tie'
class BlackjackAI_GUI(Blackjack_V1.BlackjackGUI):
    def __init__(self, master, strategy):
        ai = BlackjackAI(strategy)
        super().__init__(master, self.play_ai_turn, ai)
        self.ai = ai

    def play_ai_turn(self):
        old_state = self.ai.get_state(self.player_hand, [self.dealer_hand[0]])
        action = self.ai.choose_action(self.player_hand, [self.dealer_hand[0]])

        if action == 'hit':
            self.hit()
        elif action == 'stand':
            self.stand()

        reward = self.get_reward(self.player_hand, self.dealer_hand)
        new_state = self.ai.get_state(self.player_hand, [self.dealer_hand[0]])

        self.ai.update_q_values(old_state, action, reward, new_state)

    def deal_initial_cards(self):
        super().deal_initial_cards()
        # Füge hier die Initialisierung für die KI hinzu, falls erforderlich

def play_multiple_games(num_games, optimal_strategy):
    for _ in range(num_games):
        root = tk.Tk()
        app = BlackjackAI_GUI(root, optimal_strategy)
        app.deal_initial_cards()
        root.mainloop()

if __name__ == "__main__":
    num_games = 5
    optimal_strategy = genetic_algorithm(population_size=10, generations=5, mutation_rate=0.1)
    play_multiple_games(num_games, optimal_strategy)
