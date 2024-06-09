import numpy as np
import math
import pygame
from Evo import *

class Transform:
    def __init__(self, position, velocity, acceleration):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.array(acceleration, dtype=float)

    def applyForce(self, force):
        self.acceleration += force

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration = 0

    def square_distance(self, other):
        x = other[0]
        y = other[1]
        return (self.position[0] - x) ** 2 + (self.position[1] - y) ** 2

    def __str__(self):
        return f"Position: {self.position}, Rotation: {self.rotation}"

class Sprite:
    def __init__(self, f):
        self.draw = f

class Rocket:
    def __init__(self, location, thruster):
        self.transform = Transform(location, [0, 0], [0, 0])
        self.thruster = thruster

        def draw(screen):
            width = 10
            height = 30
            color = (255, 255, 255) 

            angle = math.atan2(self.transform.velocity[1], self.transform.velocity[0]) + math.pi / 2

            top_vertex = np.array([0, -height / 2])
            left_vertex = np.array([-width / 2, height / 2])
            right_vertex = np.array([width / 2, height / 2])

            rotation_matrix = np.array([
                [math.cos(angle), -math.sin(angle)],
                [math.sin(angle), math.cos(angle)]
            ])
            top_vertex = np.dot(rotation_matrix, top_vertex)
            left_vertex = np.dot(rotation_matrix, left_vertex)
            right_vertex = np.dot(rotation_matrix, right_vertex)

            top_vertex += self.transform.position
            left_vertex += self.transform.position
            right_vertex += self.transform.position

            # Desenhar o triângulo
            pygame.draw.polygon(screen, color, [top_vertex, left_vertex, right_vertex])

        self.sprite = Sprite(draw)

    def update(self):
        self.thruster.apply(self)
        self.transform.update()

    def __str__(self):
        return str(self.transform)

    def draw(self, screen):
        self.sprite.draw(screen)

class Thruster:
    def __init__(self, forces=[0,1]):
        self.forces = []

        for i in range(0, len(forces), 2):
            self.forces.append(np.array([forces[i], forces[i + 1]]))

        self.current_force = 0

    def apply(self, rocket):
        rocket.transform.applyForce(self.forces[self.current_force])
        self.current_force = (self.current_force + 1) % len(self.forces)

class Obstacle:
    def __init__(self, top_left, bottom_right):
        self.top_left = np.array(top_left)
        self.bottom_right = np.array(bottom_right)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (*self.top_left, *self.bottom_right))

    def check_collision(self, rocket):
        x = rocket.transform.position[0]
        y = rocket.transform.position[1]
        return x > self.top_left[0] and x < self.top_left[0] + self.bottom_right[0] and \
               y > self.top_left[1] and y < self.top_left[1] + self.bottom_right[1]


def fitness(goal, obstacles, initial_position):
    def simulation(thrustGene):
        thrust = Thruster(thrustGene)
        rocket = Rocket(location=initial_position, thruster=thrust)

        size = len(thrust.forces)

        for i in range(size):

            rocket.update()

            for obstacle in obstacles:
                if obstacle.check_collision(rocket):
                    return 0.5/rocket.transform.square_distance(goal)
            
            if rocket.transform.position[0] < 0 or rocket.transform.position[0] > 800 or \
               rocket.transform.position[1] < 0 or rocket.transform.position[1] > 600:
                return 0.5/rocket.transform.square_distance(goal)

            if rocket.transform.position[0] < goal[0] + goal_radius and rocket.transform.position[0] > goal[0] - goal_radius and \
               rocket.transform.position[1] < goal[1] + goal_radius and rocket.transform.position[1] > goal[1] - goal_radius:
                return 10

        return 1/rocket.transform.square_distance(goal) + 1

    return simulation

def debug_all(goal, obstacles, screen, initial_position):
    def simulate(individuals):
        individuals = list(map(lambda x: x[0], individuals))

        rockets = []

        for dna in individuals:
            thrust = Thruster(dna.genes)
            rockets.append(Rocket(location=initial_position, thruster=thrust))

        size = len(rockets[0].thruster.forces)

        for _ in range(size):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 0, 0))

            for rocket in rockets:
                rocket.draw(screen)
                
                for obstacle in obstacles:
                    if obstacle.check_collision(rocket):
                        if rocket in rockets:
                            rockets.remove(rocket)
                        continue

                if rocket.transform.position[0] < 0 or rocket.transform.position[0] > 800 or \
                    rocket.transform.position[1] < 0 or rocket.transform.position[1] > 600:
                    if rocket in rockets:
                        rockets.remove(rocket)
                    continue

                if rocket.transform.position[0] < goal[0] + goal_radius and rocket.transform.position[0] > goal[0] - goal_radius and \
                   rocket.transform.position[1] < goal[1] + goal_radius and rocket.transform.position[1] > goal[1] - goal_radius:
                    continue

                rocket.update()

            for obstacle in obstacles:
                obstacle.draw(screen)

            pygame.draw.circle(screen, (255, 0, 0), goal, goal_radius)

            pygame.display.flip()
            pygame.time.Clock().tick(200)
        
    return simulate
    
goal_radius = 20

def example1():
    alphabet = list(np.arange(-2,2,0.01))
    initial_pop = Population(100, alphabet, 400)

    obs = [Obstacle([100, 300], [500, 50])]
    initial_position = [400, 500]
    goal_position = [250, 100]

    fit_f = fitness(goal_position, obs, initial_position)
    simulation = debug_all(goal_position, obs, screen, initial_position)

    b = Evolution(fit_f,
                    roulette_selection,
                    uniform_crossover,
                    mut_string(alphabet, 0.05),
                    lambda x: False,
                    simulation)

    b.evolver(initial_pop)


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rocket Simulation")

example1()

pygame.quit()



