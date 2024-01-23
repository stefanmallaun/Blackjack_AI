

class Game:
    def __init__(self):
        self.deck =  4* range(1,11)
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
        