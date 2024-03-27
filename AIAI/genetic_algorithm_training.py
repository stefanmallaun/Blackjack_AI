#Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import blackjack as bj
import genetic_algorithm as ga

# Adjustable Parameters
population_size = 400
max_generation = 30
simulation_turns = 100


#Data Recording
mean_fitness = np.empty(max_generation)


#Genetic Algorithm Evolution

#Initial Population
population = ga.create_population(population_size)
ga.fitness(population, simulation_turns)
mean_fitness[0] = population['fitness'].mean()
print(f"Generation:0    Mean Fitness:{population['fitness'].mean()}")

#Main Loop
for generation in range(1,max_generation):
    population['individual'] = ga.reproduction(ga.selection(population),population_size)
    ga.fitness(population,simulation_turns)
    mean_fitness[generation] = population['fitness'].mean()
    print(f"Generation:{generation}    Mean Fitness:{population['fitness'].mean()}")


solution = population['individual'][population['fitness'].idxmax()].strategy

#Write Solution to Excel Spreadsheet
writer = pd.ExcelWriter('Genetic Algorithm Strategy.xlsx')
solution[0].to_excel(writer,'Hard')
solution[1].to_excel(writer,'Soft')
writer.save()
