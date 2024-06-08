import string
from Evo import *

alphabet = string.ascii_letters + ' '
guess = list('lorem ipsum')

a = Population(100, alphabet, len(guess))

b = Evolution(fit_string(guess, lambda x: x),
                    rank_selection,
                    uniform_crossover,
                    mut_string(alphabet, 0.05),
                    eq_stop_condition(guess))

print(b.evolver(a))
