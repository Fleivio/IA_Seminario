import pygame
import random
from Evo import * 

class Creature:
    MAX_SPEED = 5
    MAX_RADIUS = 20
    MAX_HEALTH = 20000
    MAX_FEAR = 10
    MAX_HUNGER = 50
    MAX_AGGRESSIVENESS = 10

    RANDOM_GENE_BIAS = 1000
    GENE_COUNT = 6

    def __init__(self, genes, position):
        self.genes = genes.copy()
        self.parse_genes(genes)
        self.position = position

    def parse_genes(self, genes):

        def scale_to_max(value, max):
            return value * max / Creature.RANDOM_GENE_BIAS

        self.radius = scale_to_max(max(2, genes.pop(0)), Creature.MAX_RADIUS)
        self.speed = scale_to_max(genes.pop(0), Creature.MAX_SPEED)
        self.health = scale_to_max(max(20, genes.pop(0)), Creature.MAX_HEALTH)
        self.fear = scale_to_max(genes.pop(0), Creature.MAX_FEAR)
        self.hunger = scale_to_max(genes.pop(0), Creature.MAX_HUNGER)
        self.aggressiveness = scale_to_max(genes.pop(0), Creature.MAX_AGGRESSIVENESS)
        self.max_health = self.health

    def take_damage(self, damage):
        self.health -= damage

        if self.is_dead():
            Ecosystem.remove_creature(self)        

    def update(self):
        self.move()
        self.predate()
        self.health -= max(self.radius, 10)

        if self.is_dead():
            Ecosystem.remove_creature(self)

    def is_dead(self):
        if self.health <= 0:
            self.health = 0
            return True

    def eat(self, food):
        self.health += food

        if self.health > self.max_health:
            self.health = self.max_health

        r = random.random()
        if r < 0.1:
            Ecosystem.add_creature(self.reproduce())

    def predate(self):
        for creature in Ecosystem.pop:
            if creature == self:
                continue
            if circle_is_inside(creature, self):
                if self.radius > creature.radius:
                    Ecosystem.remove_creature(creature)
                    self.eat(creature.health)

    def __str__(self):
        return f"Creature {self.radius, self.speed, self.health, self.position}"

    def reproduce(self):
        position = (self.position[0] + random.choice([-self.radius, self.radius]),
                    self.position[1] + random.choice([-self.radius, self.radius]))
        def mut(c):
            # c = mut_linear(Creature.RANDOM_GENE_BIAS, 0, 0.8, 10)(c)
            c = mut_string(range(0, Creature.GENE_COUNT), 0.1)(c)
            return c
        return Creature(mut(self.genes.copy()), position)

    def draw(self):
        r = round(255 * (self.aggressiveness / Creature.MAX_AGGRESSIVENESS))
        g = round(255 * (self.max_health / Creature.MAX_HEALTH))
        b = round(255 * (self.speed / Creature.MAX_SPEED))
        pygame.draw.circle(screen, (r,g,b), self.position, self.radius)

    def random_creature():
        def randint():
            return random.randint(1, Creature.RANDOM_GENE_BIAS)
        return Creature([randint() for _ in range(Creature.GENE_COUNT)],
                         (random.randint(0, screen_width), random.randint(0, screen_height)))

    def movement_direction(self):
        sight_range = 100

        closest_food = None
        closest_smaller_creature = None
        closest_bigger_creature = None

        food_distance = sight_range
        for food in Ecosystem.food:
            distance = point_distance(self.position, food.position)
            if distance < food_distance:
                food_distance = distance
                closest_food = food
        
        weaker_distance = sight_range
        stronger_distance = sight_range
        for creature in Ecosystem.pop:
            if abs(creature.radius - self.radius) < 3:
                continue

            distance = point_distance(self.position, creature.position)

            if creature.radius < self.radius and distance < weaker_distance:
                weaker_distance = distance
                closest_smaller_creature = creature

            elif creature.radius > self.radius and distance < stronger_distance:
                stronger_distance = distance
                closest_bigger_creature = creature

        option = random.choices(['F', 'P', 'R'], 
                                weights=[self.hunger, self.fear, self.aggressiveness])[0]
        
        if option == 'F' and closest_food:
            return (closest_food.position[0] - self.position[0], closest_food.position[1] - self.position[1])
        elif option == 'P' and closest_smaller_creature:
            return (closest_smaller_creature.position[0] - self.position[0], closest_smaller_creature.position[1] - self.position[1])
        elif option == 'R' and closest_bigger_creature:
            return (self.position[0] - closest_bigger_creature.position[0], self.position[1] - closest_bigger_creature.position[1])
        else:
            return (random.randint(-1, 1), random.randint(-1, 1))

    def move(self):
        direction = self.movement_direction()
        norm = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
        if norm == 0:
            return

        direction = (direction[0] * self.speed / norm, direction[1] * self.speed / norm)

        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])

class Food:
    def __init__(self, color, radius, position):
        self.color = color
        self.radius = radius
        self.position = position
        
    def __str__(self):
        return f"Food {self.color, self.position}"

    def draw(self):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
    

def circle_collision(circle1, circle2):
    return (circle1.position[0] - circle2.position[0]) ** 2 + (circle1.position[1] - circle2.position[1]) ** 2 < (circle1.radius + circle2.radius) ** 2

def point_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def circle_is_inside(c1, c2):
    return point_distance(c1.position, c2.position) + c1.radius < c2.radius

class Ecosystem:
    FOOD_AMOUNT = 50

    def setup(initial_population):
        Ecosystem.pop = initial_population
        Ecosystem.food = [Ecosystem.gen_new_food() for _ in range(Ecosystem.FOOD_AMOUNT)]

    def gen_new_food():
        return Food((255, 0, 0), 2, (random.randint(0, screen_width), random.randint(0, screen_height)))

    def update():
        for creature in Ecosystem.pop:
            creature.update()
            Ecosystem.food_consumption(creature)

    def draw():
        for creature in Ecosystem.pop:
            creature.draw()
        for food in Ecosystem.food:
            food.draw()

        if random.random() < 0.8:
            Ecosystem.food.append(Ecosystem.gen_new_food())

    def add_creature(creature):
        Ecosystem.pop.append(creature)

    def remove_creature(creature):
        if creature in Ecosystem.pop:
            Ecosystem.pop.remove(creature)

    def food_consumption(creature):
        for food in Ecosystem.food:
            if circle_collision(creature, food):
                creature.eat(10)
                if food in Ecosystem.food:
                    Ecosystem.food.remove(food)
                    # Ecosystem.food.append(Ecosystem.gen_new_food())


def run():
    population = [Creature.random_creature() for _ in range(50)]
    Ecosystem.setup(population)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((255, 255, 255))
        Ecosystem.update()
        Ecosystem.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(40)



screen_width = 800
screen_height = 600

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rocket Simulation")

run()

pygame.quit()
