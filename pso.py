# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 04:31:22 2018

@author: Anwar Kamil
"""
import copy    
import sys
import random
import math
import numpy    

import matplotlib.pyplot as plt 

#Ref: https://jamesmccaffrey.wordpress.com/2015/06/09/particle-swarm-optimization-using-python/
#Changes have been made to the code provided in the link above.
def show_vector(vector):
    for i in range(len(vector)):
        if i % 8 == 0: # 8 columns
            print("\n", end="")
        if vector[i] >= 0.0:
            print(' ', end="")
    print("%.4f" % vector[i], end="") # 4 decimals
    print(" ", end="")
    print("\n")

#My code
def find_fitness(position,identifier):
    fitness_score = 0.0
    if identifier == "ra": #Rastrigin function impl
        for i in range(len(position)):
            x = position[i]
            fitness_score += (x * x) - (10 * math.cos(2 * math.pi * x)) + 10
    elif identifier =="sp": #Sphere function impl
        for i in range(len(position)):
            x = position[i]
            fitness_score += (x ** 2)
    elif identifier =="gr": #Greiwank function impl
        fitness_score_1 = 0.0
        fitness_score_2 = 0.0
        for i in range(1, len(position)):
            x = position[i-1]
            fitness_score_1 += ((x ** 2)/4000)
            fitness_score_2 *= math.cos(x/(numpy.sqrt(i)))+1
        fitness_score = fitness_score_1 - fitness_score_2
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
                fitness_score_1 += (a**j) * math.cos((2*math.pi*b**i)*(x+0.5))
                fitness_score_2 += (a**j) * math.cos((2*math.pi*b**i)*0.5)
        
            fitness_score += fitness_score_1 - ((len(position)) * fitness_score_2)
    elif identifier == "ro":
        for i in range(len(position)-1):
            x = position[i]
            next_x = position[i+1]
            fitness_score += 100 * (next_x - (x**2)) + ((1-x)**2)
        
            
    return fitness_score
#Includes some of my code & some from reference
class Particle:
    def __init__(self, dim, minx, maxx, seed):
        self.randnum = random.Random()
        self.position = [0.0 for i in range(dim)]
        self.velocity = [0.0 for i in range(dim)]
        self.best_part_pos = [0.0 for i in range(dim)]
        for i in range(dim):
            self.position[i] = ((maxx - minx) *self.randnum.random() + minx)
            self.velocity[i] = ((maxx - minx) *self.randnum.random() + minx)
        self.fitness_score = find_fitness(self.position,identifier) # curr error
        self.best_part_pos = copy.copy(self.position)
        self.best_part_fitness = self.fitness_score # best error
def Solve(max_epochs, n, dim, minx, maxx, identifier):
    rnd = random.Random(0)
    # create n random particles
    swarm = [Particle(dim, minx, maxx, i) for i in range(n)]
    best_swarm_pos = [0.0 for i in range(dim)] # not necess.
    best_swarm_fitness = sys.float_info.max # swarm best
    for i in range(n): # check each particle
        if swarm[i].fitness_score < best_swarm_fitness:
            best_swarm_fitness = swarm[i].fitness_score
            best_swarm_pos = copy.copy(swarm[i].position)
    epoch = 0
    w = 0.729    # inertia/ the weight with which we multiply the velocity at each iteration/epoch
    cognitive = 1.49445 #the constant for optimizing the particle's position & velocity to reach local minima
    social = 1.49445 # the constant for optimizing the swarm's position & velocity to reach global minima
    #identifier = "sp"
    Fitness=[]
    while epoch < max_epochs:
        Fitness.append(best_swarm_fitness)
        if epoch % 10 == 0 and epoch > 1:
            print("Iteration = " + str(epoch) +", best fitness = %.3f" % best_swarm_fitness)
        for i in range(n): # process each particle
         # compute new velocity of curr particle
            for k in range(dim):
                r1 = rnd.random()    # randomizations
                r2 = rnd.random()
                swarm[i].velocity[k] = ( (w * swarm[i].velocity[k]) +(cognitive * r1 * (swarm[i].best_part_pos[k] -swarm[i].position[k])) +  (social * r2 * (best_swarm_pos[k] -swarm[i].position[k])) ) 
            if swarm[i].velocity[k] < minx:
                swarm[i].velocity[k] = minx
            elif swarm[i].velocity[k] > maxx:
                swarm[i].velocity[k] = maxx
      # compute new position using new velocity
        for k in range(dim):
            swarm[i].position[k] += swarm[i].velocity[k]
 
      # compute error of new position
        swarm[i].fitness_score = find_fitness(swarm[i].position,identifier)
      # Checking if new position is best fit for a particular particle
        if swarm[i].fitness_score < swarm[i].best_part_fitness:
            swarm[i].best_part_fitness = swarm[i].fitness_score
            swarm[i].best_part_pos = copy.copy(swarm[i].position)
      # checking if new position is best fit overall in swarm
        if swarm[i].fitness_score < best_swarm_fitness:
            best_swarm_fitness = swarm[i].fitness_score
            best_swarm_pos = copy.copy(swarm[i].position)
   
    # for-each particle
        epoch += 1
  # while
    plt.plot(Fitness)
    print(best_swarm_fitness)
    return best_swarm_pos
# end Solve
print("Particle swarm optimization\n")
dim = 3
identifier = "sp"
num_particles = 15
max_epochs = 1000
print("Number of particles = " + str(num_particles))
print("Number of Iterations    = " + str(max_epochs))

best_position = Solve(max_epochs, num_particles,dim, -10.0, 10.0,identifier)

print("\nBest solution found:")
show_vector(best_position)
fitness = find_fitness(best_position,identifier)