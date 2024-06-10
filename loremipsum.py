import string
from Evo import *

def print_best(pop):
    pop.sort(key=lambda x: x[1])
    best = pop[-1]
    print(best[0])

alphabet = string.ascii_letters + ' '
guess = list('lorem ipsum')

a = Population(100, alphabet, len(guess))

b = Evolution(fit_string(guess, lambda x: x),
                    roulette_selection,
                    k_point_crossover(2),
                    mut_string(alphabet, 0.05),
                    eq_stop_condition(guess),
                    debug=print_best)

print(b.evolver(a))
