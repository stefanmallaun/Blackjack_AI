import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import logistic
import pandas as pd
import copy
from random import shuffle, sample
import random



matchs = []

for x in range(100):
    jogo = Game()
    lucas = First_strategy('Lucas')
    miura = Player('Miura')
    sergio = Second_strategy('Sergio')
    
    matchs.append(jogo.start_game([lucas, miura, sergio]))

print len([m for m in matchs if m == 'Miura'])
print matchs
