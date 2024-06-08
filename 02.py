from Evo import *

alphabet = range(10)
guess = [0,0,0]

a = Population(100, alphabet, len(guess))

b = Evolution(fit_string(guess, lambda x: x),
                    rank_selection,
                    uniform_crossover,
                    mut_string(alphabet, 0.05),
                    eq_stop_condition(guess))

print(b.evolver(a))
