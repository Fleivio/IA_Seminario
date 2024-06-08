import random


class DNA:
    def __init__(self, genes):
        self.genes = genes

    def fitness(self, f):
        return f(self.genes)

    def __str__(self):
        return str(self.genes)

    def __repr__(self):
        return str(self.genes)

class Population:
    def __init__(self, size, genes, size_dna):
        def randDNA():
            return [random.choice(genes) for _ in range(size_dna)]

        self.population = [DNA(randDNA()) for _ in range(size)]

    def paired_fitness(self, f):
        fits = [i.fitness(f) for i in self.population]
        total = max(sum(fits), 1)
        return [(i, j / total) for (i, j) in zip(self.population, fits)]

    def best_individual(self, f): 
        return max(self.paired_fitness(f), key=lambda x: x[1])[0]

class Evolution():
    def __init__(self, fitness, selection, crossover, mutation, stop_condition):
        self.fitness = fitness
        self.mutation = mutation
        self.selection = selection
        self.crossover = crossover
        self.stop_condition = stop_condition

    def evolver(self, population):
        generations = 0
        while self.stop_condition(population.best_individual(self.fitness)) == False:
            ind_and_fitness = population.paired_fitness(self.fitness)
            mating_pool = self.selection(ind_and_fitness)

            offspring = []
            for p1, p2 in mating_pool:
                offspring += self.crossover(p1, p2)

            mut_offspring = [self.mutation(i) for i in offspring]
            
            population.population = mut_offspring
            generations += 1

        return generations

def fit_string (string, f):
    return \
    lambda x, string=string, f=f: f(sum(1 for i, j in zip(x, string) if i == j))

def mut_string (genes, rate):
    def mut(indiviual):
        return DNA([random.choice(genes) if random.random() < rate else i for i in indiviual.genes])

    return mut

# SELECTORS

def rank_selection(population):
    population.sort(key=lambda x: x[1])
    total = len(population)

    for i in range(total):
        population[i] = (population[i][0], 2 * (i + 1) / (total * (total + 1)))

    return roulette_selection(population)

def roulette_selection(population):
    total = len(population)
    matings = []

    def select_one():
        r = random.random()
        acc = 0
        for i in range(total):
            if r < (population[i][1] + acc):
                return population[i][0]
            else:
                acc += population[i][1]

    for i in range(round(total/2)):
        matings.append((select_one(), select_one()))
    
    return matings

def tournament_selection(size, probability):
    # seleciona uma amostra aleatoria de tamanho size da população
    def sample(population):
        return random.sample(population, min(size, len(population)))

    # adiciona o fator aleatorio: se for menor que a probabilidade, seleciona o melhor, senão, seleciona um aleatorio
    def random_selection(sample):
        if random.random() < probability:
            return max(sample, key=lambda x: x[1])[0]
        else:
            return random.choice(sample)[0]

    def selection(population):
        total = len(population)
        matings = []

        for i in range(round(total/2)):
            first = random_selection(sample(population))
            second = random_selection(sample(population))
            matings.append((first, second))

        return matings

    return selection

# CROSSOVERS

def one_point_crossover(p1, p2):
    point = random.randint(0, len(p1.genes))
    f1 = p1.genes[:point] + p2.genes[point:]
    f2 = p2.genes[:point] + p1.genes[point:]

    return DNA(f1), DNA(f2)

def k_point_crossover(points):
    def crossover(p1, p2):
        f1 = DNA(p1.genes)
        f2 = DNA(p2.genes)

        for _ in range(points):
            f1, f2 = one_point_crossover(f1, f2)

        return f1, f2

    return crossover

def uniform_crossover(p1, p2):
    f1 = [i if random.random() < 0.5 else j for i, j in zip(p1.genes, p2.genes)]
    f2 = [i if random.random() < 0.5 else j for i, j in zip(p1.genes, p2.genes)]

    return DNA(f1), DNA(f2)

# CONDIÇÕES DE PARADA

def eq_stop_condition(string):
    def stop(best_individual):
        print(best_individual)
        # input()
        return best_individual.genes == string

    return stop