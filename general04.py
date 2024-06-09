import pygame

import random
import numpy as np
from Evo import *
from UI import *

class Forms:
    def __init__(self, dna):
        self.dna = DNA(dna.genes.copy())
        self.forms = Forms.parse_config(dna.genes)

    def draw(self, screen, delta=(0,0)):
        for form in self.forms:
            form.draw(screen, delta)
    
    def __str__(self):
        return '\n'.join(map(str, self.forms))
        
    def parse_config(configuration):
        forms = []

        if len(configuration) <= 4:
            return []
        
        delta = 255/maxGene
        tp = configuration.pop(0)
        r = configuration.pop(0) * delta
        g = configuration.pop(0) * delta
        b = configuration.pop(0) * delta

        [a,b,c] = np.linspace(0, maxGene, 3)

        if tp < b:
            # circle
            if len(configuration) < 3:
                return []
            radius = configuration.pop(0)/2
            x = configuration.pop(0)
            y = configuration.pop(0)
            forms.append(Circle((r, g, b), radius, (x, y)))
        elif tp < c:
            # rectangle
            if len(configuration) < 4:
                return []
            width = configuration.pop(0)
            height = configuration.pop(0)
            x = configuration.pop(0)
            y = configuration.pop(0)
            forms.append(Rectangle((r, g, b), width, height, (x, y)))
        else:
            # triangle
            if len(configuration) < 4:
                return []
            base = configuration.pop(0)
            height = configuration.pop(0)
            x = configuration.pop(0)
            y = configuration.pop(0)
            forms.append(Triangle((r, g, b), base, height, (x, y)))

        return forms + Forms.parse_config(configuration)

class ButtonFamily:
    def __init__(self, population, constructor, onClick):
        forms = []
        dnas = population.population

        for dna in dnas:
            forms.append(constructor(dna))

        w, h = 100, 100
        x = 30

        self.buttons = []
        for f in forms:
            self.buttons.append(Button(f, (x, 100), w, h, onClick))
            x += w + 50
        
    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def check_click(self, x, y):
        for button in self.buttons:
            button.check_click(x, y)

def gen_next_pop(chosen_one):
    chosen_dna = chosen_one.dna
    
    new_dnas = [mut_forms(chosen_dna) for i in range(popsize)]
    pop.population = new_dnas

    global b
    b = ButtonFamily(pop, Forms, gen_next_pop)

def ex1():

    while True:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                b.check_click(x, y)

        screen.fill((255, 255, 255))
        b.draw(screen)

        global mut_forms, slider, slideroutput

        slider_out = slider.getValue()
        slideroutput.setText(slider_out)
        mut_forms = mut_linear(maxGene, 0, slider_out, 10)



        pygame_widgets.update(events)
        pygame.display.flip()

        pygame.time.Clock().tick(200)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 300))
    pygame.display.set_caption("Forms Simulation")

    maxGene = 50
    popsize = 5

    slider = Slider(screen, 50, 10, 600, 20, min=0, max=1, step=0.01)
    slideroutput = TextBox(screen, 700, 10, 50, 50, fontSize=20)


    mut_forms = mut_linear(maxGene, 0, 0.2, 10)
    pop = Population(popsize, list(np.arange(0,maxGene,0.01)), 100)
    b = ButtonFamily(pop, Forms, gen_next_pop)


    ex1()

    pygame.quit()

