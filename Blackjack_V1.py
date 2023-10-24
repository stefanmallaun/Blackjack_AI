import random

# Funktion zum Erstellen eines Kartendecks
def create_deck():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

# Funktion zum Berechnen der Punktzahl einer Hand
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

# Hauptspiel
def play_blackjack():
    money = 3000
    bet = 100
    again = True

    while again:
        deck = create_deck()
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        while True:
            player_score = calculate_score(player_hand)
            dealer_score = calculate_score(dealer_hand)

            print(f"Deine Hand: {player_hand}, Punktzahl: {player_score}")
            print(f"Hand des Dealers: [{dealer_hand[0]}, ?]")

            if player_score == 21 and len(player_hand) == 2:
                print("Blackjack! Du gewinnst!")
                money += bet*1,5
                break
            elif dealer_score == 21 and len(dealer_hand) == 2:
                print("Dealer hat Blackjack. Du verlierst.")
                money -= bet
                break
            elif player_score > 21:
                print("Du hast überkauft. Du verlierst.")
                money -= bet
                break
            elif dealer_score > 21:
                print("Dealer hat überkauft. Du gewinnst!")
                money += bet
                break

            action = input("Möchtest du eine weitere Karte ziehen? Ja oder Nein: ").lower()
            if action == 'ja':
                player_hand.append(deck.pop())
            else:
                while dealer_score < 17:
                    dealer_hand.append(deck.pop())
                    dealer_score = calculate_score(dealer_hand)

                print(f"Hand des Dealers: {dealer_hand}, Punktzahl: {dealer_score}")
                if dealer_score > 21:
                    print("Dealer hat überkauft. Du gewinnst!")
                    money += bet
                elif player_score > dealer_score:
                    print("Du gewinnst!")
                    money += bet
                else:
                    print("Du verlierst.")
                    money -= bet
                break

        again = input("Wollen Sie nochmal spielen? (True/False) ").lower() == 'true'
    
    print("Your final Money is: %s" % money)

play_blackjack()
