import pygame


class Ship:
    def __init__(self, screen, coords, speed, xp=100, armor=0):
        self.screen = screen
        self.coords = coords
        self.speed = speed
        self.xp = xp
        self.armor = armor

    def get_coord(self):
        return self.coords

    def move(self, vert, hor):
        self.coords[0] += self.speed * hor
        self.coords[1] += self.speed * vert
        self.render()

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, pygame.Color('yellow'), (500, 500), 50)
        pygame.draw.circle(self.screen, pygame.Color('white'), tuple(self.coords), 25)
