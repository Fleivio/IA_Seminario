
from forms import *

class Face:
    def __init__(self, dna):
        self.dna = dna.copy()
        self.phenotype = Face.parse_config(dna)

    def parse_config(configuration):
        forms = []
        maxGene = 50 
        delta = 255/maxGene

        color = (configuration.pop(0) * delta, configuration.pop(0) * delta, configuration.pop(0) * delta)
        radius = configuration.pop(0)/4
        x = configuration.pop(0)
        y = configuration.pop(0)
        left_eye = Circle(color, radius, (x, y))

        forms.append(left_eye)

        color = (configuration.pop(0) * delta, configuration.pop(0) * delta, configuration.pop(0) * delta)
        radius = configuration.pop(0)/4
        x = configuration.pop(0)
        y = configuration.pop(0)
        right_eye = Circle(color, radius, (x, y))

        forms.append(right_eye)

        color = (configuration.pop(0) * delta, configuration.pop(0) * delta, configuration.pop(0) * delta)
        width = configuration.pop(0)
        height = configuration.pop(0)
        x = configuration.pop(0)
        y = configuration.pop(0)
        mouth = Rectangle(color, width, height, (x, y))

        forms.append(mouth)

        return forms

    def draw(self, screen, delta=(0,0)):
        for form in self.phenotype:
            form.draw(screen, delta)

# fc = Face(list(range(100, 155)))


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

def gen_next_faces(chosen_one):
    chosen_dna = chosen_one.dna
    
    new_dnas = [mut_forms(chosen_dna) for i in range(popsize)]
    pop.population = new_dnas


    global b
    b = ButtonFamily(pop, Face, gen_next_faces)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((900, 300))
    pygame.display.set_caption("Forms Simulation")

    popsize = 6
    maxGene = 50

    mut_forms = mut_linear(maxGene, 0, 0.3, 10)
    slider = Slider(screen, 50, 10, 600, 20, min=0, max=1, step=0.01)
    slideroutput = TextBox(screen, 700, 10, 50, 50, fontSize=20)


    pop = Population(popsize, list(np.arange(0,maxGene,0.01)), 100)
    b = ButtonFamily(pop, Face, gen_next_faces)


    ex1()

    pygame.quit()
