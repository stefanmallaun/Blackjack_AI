# Importieren der Bibliotheken
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# Definieren der Komponenten der Blackjack-Simulation
class Shoe:  
    def __init__(self, deck_num):
        self.deck_num = deck_num
        self.cards = np.array(deck_num * [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7,
                                           8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11])

    # Methode: Mischen der Reihenfolge jeder Karte im Schuh (jede Ganzzahl im Array)
    def shuffle(self):
        np.random.shuffle(self.cards)

    # Methode: Eine Karte austeilen
    def deal_card(self):
        # Gibt den Kartenwert oben im Schuh (Index = 0) zurück und löscht dann die Karte aus dem Schuh
        card = self.cards[0]
        self.cards = np.delete(self.cards, 0)
        return card

class Player:
    # Methode: Initialisieren von Instanzvariablen für die Klasse Player
    def __init__(self, cash, strategy):
        self.cash = cash
        #strategy: Liste von 2 Einträgen, die Hard- und Soft-Strategie-DataFrames enthalten
        self.strategy = strategy
        self.bet = 0
        self.hand = np.array([], dtype=int)
        self.count = 0

    # Methode: Strategie aufrufen
    def call_strategy(self, dealer_hand):
        if 11 in self.hand:
            return self.strategy[1].at[self.count, dealer_hand[0]]
        else:
            return self.strategy[0].at[self.count, dealer_hand[0]]

    # Methode: Eine Wette platzieren
    def make_bet(self, bet_amount):
        self.bet += bet_amount
        self.cash -= bet_amount

    # Methode: Dem Spieler erlauben, eine weitere Karte zu nehmen (eine weitere Karte zu ihrer Hand hinzufügen) aus einem bestimmten
    def hit(self, shoe):
        self.hand = np.append(self.hand, shoe.deal_card())
        self.count = np.sum(self.hand)

class Dealer:
    # Methode: Initialisieren von Instanzvariablen für ein Objekt der Klasse Dealer
    def __init__(self):
        #hand: NumPy-Array von Ganzzahlen, die die Werte der Karten für die Hand des Dealers repräsentieren
        self.hand = np.array([], dtype=int)
        self.count = 0

    def hit(self, shoe):
        self.hand = np.append(self.hand, shoe.deal_card())
        self.count = np.sum(self.hand)
