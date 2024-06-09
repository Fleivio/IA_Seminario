import pygame 

class Circle:
    def __init__(self, color, radius, position):
        self.color = color
        self.radius = radius
        self.position = position

    def __str__(self):
        return f'Circle: {self.color}, {self.radius}, {self.position}'

    def draw(self, screen, delta):
        pygame.draw.circle(screen, self.color, (self.position[0] + delta[0], self.position[1] + delta[1]), self.radius)

class Rectangle:
    def __init__(self, color, width, height, position):
        self.color = color
        self.width = width
        self.height = height
        self.position = position

    def __str__(self):
        return f'Rectangle: {self.color}, {self.width}, {self.height}, {self.position}'

    def draw(self, screen, delta):
        pygame.draw.rect(screen, self.color, (self.position[0] + delta[0], self.position[1] + delta[1], self.width, self.height))

class Triangle:
    def __init__(self, color, base, height, position):
        self.color = color
        self.base = base
        self.height = height
        self.position = position

    def __str__(self):
        return f'Triangle: {self.color}, {self.base}, {self.height}, {self.position}'

    def draw(self, screen, delta):
        x, y = self.position
        x += delta[0]
        y += delta[1]
        pygame.draw.polygon(screen, self.color, [(x, y), (x + self.base, y), (x + self.base / 2, y - self.height)])

class Button:
    def __init__(self, content, position, w, h, onClick):
        self.content = content
        self.position = position
        self.onClick = onClick
        self.w = w
        self.h = h

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), (self.position[0], self.position[1], self.w, self.h))
        self.content.draw(screen, self.position + (self.w/2, self.h/2))

    def check_click(self, x, y):
        if (x > self.position[0] and x < self.position[0] + self.w and \
               y > self.position[1] and y < self.position[1] + self.h):
            self.onClick(self.content)