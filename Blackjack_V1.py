import tkinter as tk
from tkinter import messagebox
import random

class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")
        
        self.money = 3000
        self.bet = 100

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
            score += 11
            num_aces += 1
        else:
            score += int(card['rank'])
    while score > 21 and num_aces > 0:
        score -= 10
        num_aces -= 1
    return score

if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    app.deal_initial_cards()
    root.mainloop()
