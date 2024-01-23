import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import logistic
import pandas as pd
import copy
from random import shuffle, sample
import random
from tqdm import tqdm

class Game:
    def __init__(self):
        self.deck =  list(range(1,11)) * 4
        shuffle(self.deck)
        self.game_running = False
        self.cumulative_draw = 0 
        self.best_player_score = 0
    def start_game(self, player_list):
        while  len([p for p in player_list if p.burn == False and p.stop == False]) > 1:
            for player in [p_t for p_t in player_list if p_t.burn == False and p_t.stop == False]:
                #print player.name,player.points
                if player.decision(self)[0] == 0:
                    player.stop_game()
                else:
                    self.cumulative_draw += player.draw(self.deck)
                if self.best_player_score < player.points:
                    self.best_player_score = player.points
        #print [[p_e.name, p_e.points] for p_e in player_list]
        winner_table =  [p_e for p_e in player_list if p_e.burn == False]
        winner_table = sorted(winner_table, key = lambda x : 21 - x.points)
        #print [p_e.points for p_e in winner_table] 
        #print 'Game ended...'
        
         
        if set([p_end.points for p_end in winner_table]) == 1 or not winner_table:
            #print 'ko'
            return 'ko'
        else:
            #print 'ganhador',   winner_table[0].name 
            return winner_table[0].name
        
        
class Player:
    def __init__(self, name):
        self.stop = False
        self.burn = False
        self.points = 0
        self.name = name
        self.neural_network = None
    def decision(self, game_obj):
        
        out = sample([0,1], 1) # the output shoud be [0] or [1]
        #print out 
        return out  # random behavior
    
    def stop_game(self):
        #print self.name, 'Stop'
        self.stop = True
    def draw(self, deck_game):
        
        card = deck_game.pop()
        #print self.name, 'comprou card', card
        self.points += card
        if self.points > 21:
            self.burn = True
            #print self.name, 'BURNEDD!'
        return card
            
class First_strategy(Player):
    def decision(self, game_obj):
        if self.points < 15:
            return [1]
        else:
            return [0]
    
class Second_strategy(Player):
    def decision(self, game_obj):
        return [1]


matchs = []

for x in range(100):
    jogo = Game()
    lucas = First_strategy('Lucas')
    miura = Player('Miura')
    sergio = Second_strategy('Sergio')
    
    matchs.append(jogo.start_game([lucas, miura, sergio]))

print (len([m for m in matchs if m == 'Miura']))
print (matchs)


class Network:
    def __init__(self, input_number = 2):
        self.l_1 = np.random.uniform(-1,1, [10,input_number])

        self.l_2 = np.random.uniform(-1,1,[10,10])
        self.l_end = np.random.uniform(-1,1,[1,10])
        self.layers_stack = [self.l_1 , self.l_2 , self.l_end]
    
    
    def sigmoid (self, x): return 1/(1 + np.exp(-x))
    
    def foward(self, input_value):
        #print input_value
        res_l1 =  np.array([self.sigmoid(l1_s) for l1_s in      input_value.dot(self.l_1.T)])
        res_l2 = np.array([ self.sigmoid(l2_s)  for l2_s in     res_l1.dot(self.l_2.T)])
        res_end = np.array([self.sigmoid (l_r) for l_r in       res_l2.dot(self.l_end.T)])
        #print res_end
        return res_end
    
    def mutate(self, layer):
        index_to_mutate = [np.random.randint(layer.shape[0]), np.random.randint(layer.shape[1])]
        #print 'mutate',  np.random.uniform(-1, 1)
        layer[index_to_mutate[0], index_to_mutate[1]] += np.random.uniform(-0.01, 0.01)
        
        
    def mutate_all_layers(self):
        for l in self.layers_stack:
            self.mutate(l)


class Neural_strategy(Player):
    def decision(self, game_obj):
        best_rank_player = game_obj.best_player_score
        #print best_rank_player
        #print  [self.neural_network.foward(np.array([ self.points, best_rank_player ,game_obj.cumulative_draw]))]
        # Assuming self.neural_network.forward() returns a NumPy array
        output_array = self.neural_network.foward(np.array([self.points, best_rank_player, game_obj.cumulative_draw]))
        # Round each element of the array
        rounded_output_array = np.round(output_array)
        # Convert each rounded value to an integer and wrap it in a list
        result = [int(rounded_value) for rounded_value in rounded_output_array]

        return result


    def init_neural_activity(self):
        self.neural_network = Network(input_number = 3)
    def reset_status(self):
        self.stop = False
        self.burn = False
        self.points = 0
        
        
best_and_mean_scores = []
p_size= 500
population = [Neural_strategy('AI') for n in range(0,p_size)]

[p.init_neural_activity() for p in population] #starting network random weights


for i_n in range(10):
    fitness = []
    for ai in tqdm(population):
        matchs = []
        f = 0
        for x in range(60):
            jogo = Game()
            lucas = First_strategy('Lucas')
            matchs.append(jogo.start_game([ ai, lucas]))
            ai.reset_status()
        #print matchs
        f =  100 * (len([m for m in matchs if m == 'AI'])/float(len(matchs)))
        #print f 
        fitness.append(f)
    higher_fitness = sorted( [[f, p_f] for f , p_f in zip(fitness, population)], key=lambda s: s[0])
    print ('Iteration MEAN:', np.mean([v[0] for v in higher_fitness]))
    loss_str= 'Best value: {}'.format(str(higher_fitness[-1][0]))
    best_and_mean_scores.append([higher_fitness[-1][0], np.mean([v[0] for v in higher_fitness])])
    itr_str = 'Iteration: {}'.format( str(i_n))
    print (itr_str, loss_str)
    #print [ h[0] for h in  higher_fitness[-5:]]
    best_creatures = higher_fitness[-10:]
    #print [float(b_c) for b_c in best_creatures]
    population = [copy.deepcopy(random.choice(best_creatures)[1]) for i in range(0, p_size)]
    [p_m.neural_network.mutate_all_layers() for p_m in population]
    
    
df_training = pd.DataFrame(best_and_mean_scores, columns=['best_result', 'mean_result'])


plt.plot(df_training['mean_result'], color= 'red', lw=2)
plt.title('Mean % of won games by iteraction')
plt.xlabel('Iteraction number')
plt.show()


plt.plot(df_training['best_result'], color= 'blue', lw=2)
plt.title('% of won games BEST RESULTS only')
plt.xlabel('Iteraction number')
plt.show()