import tkinter as tk
from tkinter import messagebox
import random
import Blackjack_V1

class BlackjackAI:
    def __init__(self):
        self.q_values = {}

    def get_q_value(self, state):
        return self.q_values.get(state, 0)

    def update_q_value(self, state, new_value):
        current_value = self.get_q_value(state)
        self.q_values[state] = current_value + new_value

    def get_state(self, player_hand, dealer_hand):
        # Vereinfachte Darstellung des Spielzustands
        return (tuple(player_hand), dealer_hand[0])

    def choose_action(self, player_hand, dealer_hand):
        state = self.get_state(player_hand, dealer_hand)
        # Implementiere hier deine Strategie basierend auf Q-Learning oder anderen Ansätzen
        # Diese einfache Version wählt zufällig zwischen 'hit' und 'stand'
        return random.choice(['hit', 'stand'])

class BlackjackAI_GUI(Blackjack_V1.BlackjackGUI):
    def __init__(self, master, ai):
        super().__init__(master)
        self.ai = ai

    def play_ai_turn(self):
        action = self.ai.choose_action(self.player_hand, [self.dealer_hand[0]])
        if action == 'hit':
            self.hit()
        elif action == 'stand':
            self.stand()

    def deal_initial_cards(self):
        super().deal_initial_cards()
        # Füge hier die Initialisierung für die KI hinzu, falls erforderlich

def play_multiple_games(num_games):
    for _ in range(num_games):
        root = tk.Tk()
        app = BlackjackAI_GUI(root, BlackjackAI())
        app.deal_initial_cards()
        app.play_ai_turn()
        root.mainloop()

if __name__ == "__main__":
    num_games = 5  # Ändere dies auf die gewünschte Anzahl von Spielen
    play_multiple_games(num_games)
