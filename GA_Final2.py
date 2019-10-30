# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 20:54:56 2018

@author: Anwar Kamil
"""

import numpy
import math as mt

#Reference: https://towardsdatascience.com/genetic-algorithm-implementation-in-python-5ab67bb124a6
#The code in the link above has been edited.

def opt_func(position,identifier):
    fitness_score = 0.0
    #Sphere function implementation
    if identifier == "sp":
        for i in range(len(position)):
            x = position[i]
            fitness_score += (x ** 2)
    elif identifier == "ra": #Rastrigin function implementation
        for i in range(len(position)):
            x = position[i]
            fitness_score += (x**2) - (10 * mt.cos(2*mt.pi*x)) + 10
            
    elif identifier == "ro": #Rosenbrock function implementation
        for i in range(len(position)-1):
            x = position[i]
            next_x = position[i+1]
            fitness_score += 100 * (next_x - (x**2)) + ((1-x)**2)
            
    elif identifier == "we": #Weierstrass function impl
        a = 0.5
        b = 3
        k_max = 20
        fitness_score_1 = 0
        fitness_score_2 = 0
        #final_fitness = 0
        for i in range(len(position)):
            x = position[i]
            for j in range(0,k_max+1):
                fitness_score_1 += (a**j) * mt.cos((2*mt.pi*b**i)*(x+0.5))
                fitness_score_2 += (a**j) * mt.cos((2*mt.pi*b**i)*0.5)
        
            fitness_score += fitness_score_1 - ((len(position)) * fitness_score_2)
            
    elif identifier == "gr":#Greiwank function implementation
        fitness_score_1 = 0.0
        fitness_score_2 = 0.0
        for i in range(1, len(position)):
            x = position[i-1]
            fitness_score_1 += ((x ** 2)/4000)
            fitness_score_2 *= mt.cos(x/(numpy.sqrt(i)))+1
        fitness_score = fitness_score_1 - fitness_score_2
            
        
    return fitness_score

def evaluate_fitness(pop,identifier):

    # Calculating the fitness value of each solution in the current population.
    fitness=[]
    # The fitness function caulcuates the sum of products between each input and its corresponding weight.
    for i in pop:
        fitness.append(opt_func(i,identifier))

    return fitness



def tournament_selection(pop, fitness, tournament_size):

    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.

    parents = numpy.empty((tournament_size, pop.shape[1]))

    for parent_num in range(tournament_size):
        #best_fitness_idx = numpy.where(fitness == numpy.nanmin(fitness)) #This line is used only for rosenbrock function
        best_fitness_idx = numpy.where(fitness == numpy.min(fitness)) #For all functions other than Rosenbrock
        best_fitness_idx = best_fitness_idx[0][0]
        parents[parent_num, :] = pop[best_fitness_idx, :]
        fitness[best_fitness_idx] = 99999999999

    return parents



def two_point_crossover(parents, offspring_size):

    children = numpy.empty(offspring_size)

    # The point at which crossover takes place between two parents. Usually it is at the center.

    #crossover_point = numpy.uint8(offspring_size[1]/2)
    c = random.randint(0,9) #point1 for crossover
    d = random.randint(0,9) #point2 for crossover
    #print(c,d)
    if c==d:
        while c==d:
            c = random.randint(0,9) #point1 for crossover
            d = random.randint(0,9) #point2 for crossover
    
    #swapping
    if c > d:
        temp = c
        c = d
        d = temp


    index=0
    for k in range(tournament_size):

        # Index of the first parent to mate.

        parent1_idx = k%parents.shape[0]

        # Index of the second parent to mate.

        parent2_idx = (k+1)%parents.shape[0]

        #1st new offspring generated
        children[index, 0:c] = parents[parent1_idx, 0:c]
        children[index,c:d]=parents[parent2_idx,c:d]
        children[index,d:]=parents[parent1_idx,d:]

        #2nd new offspring generated
        children[index, 0:c] = parents[parent2_idx, 0:c]
        children[index,c:d]=parents[parent1_idx,c:d]
        children[index,d:]=parents[parent2_idx,d:]
        
        index = index + 2

    return children



def mutation(children_crossover):

    # Mutation changes a single gene in each offspring randomly.

    for idx in range(children_crossover.shape[0]):

        # The random value to be added to the gene.
        col=random.randint(0,9)
        random_value = numpy.random.uniform(-1.0, 1.0, 1)

        children_crossover[idx, col] = children_crossover[idx, col] -random_value

    return children_crossover




import matplotlib.pyplot as plt
import random

chromosome_length=10
pop_size = 20

tournament_size = 4

# Defining the population size.

pop_size = (pop_size,chromosome_length) # The population will have sol_per_pop chromosome where each chromosome has num_weights genes.

#Creating the initial population.

new_population = numpy.random.uniform(low=-4.0, high=4.0, size=pop_size)

print(new_population)

Fitness=[]

num_generations = 1000
identifier = "sp"

for generation in range(num_generations):
    
    #Calculating the fitness of each chromosome in the population.
    fitness_scores = evaluate_fitness(new_population,identifier)

    # Selecting the best parents in the population for crossover.
    parents = tournament_selection(new_population, fitness_scores, tournament_size)

    # Generating next generation using two point crossover.
    children_crossover = two_point_crossover(parents, offspring_size=(pop_size[0]-parents.shape[0], chromosome_length))

    # Adding some variations to the offsrping using random mutation operator.
    children_mutation = mutation(children_crossover)

    # Creating the new population which comprises of both the parents and offspring.
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = children_mutation

    # The best result in the current iteration.
    fit = evaluate_fitness(new_population,identifier)
    #best_match_idx = numpy.where(fit == numpy.nanmin(fit)) #only used for Rosenbrock
    best_match_idx = numpy.where(fit == numpy.min(fit)) # Used for all functions other than rosenbrock
    #Fitness.append(fit[best_match_idx[0][0]])
    Fitness.append(fit[best_match_idx[0][0]])
print(Fitness[-1])
plt.semilogy(Fitness)

