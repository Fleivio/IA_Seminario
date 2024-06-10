from Evo import *
import random


paths = {
    1: {2:2, 4:3, 5:6},
    2: {1:2, 3:4, 4:3},
    3: {2:4, 4:7, 5:3},
    4: {1:3, 2:3, 3:7, 5:3},
    5: {1:6, 3:3, 4:3}
}

def path_fitness(path):
    cost = 0
    path = [1] + path + [1]
    for i in range(len(path)-1):
        destinations = paths[path[i]]
        if path[i+1] in destinations:
            cost += destinations[path[i+1]]
        else:
            return 0
    return 1/cost

def print_best(pop):
    pop.sort(key=lambda x: x[1])
    best = pop[-1]
    print(best[0], 1/path_fitness(best[0]))

cities = [2,3,4,5]

pop = Population(0, [], 0)
pop.population = [random.sample(cities, len(cities)) for i in range(100)]


evo = Evolution(path_fitness,
         roulette_selection, 
         lambda x, y: (x, y), 
         mut_swap(0.5), 
         stagnation_stop_condition(10), 
         debug=print_best)

evo.evolver(pop)