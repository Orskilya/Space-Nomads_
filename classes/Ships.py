from random import randint
import pygame


class Ship:
    def __init__(self, screen, sprite, speed, coords, hull, armor, mass):
        self.screen = screen
        self.coords = coords  # list
        self.hull = hull
        self.armor = armor
        self.mass = mass
        self.speed = speed
        # Sprite
        self.sprite = sprite

    def get_coord(self):
        return self.coords

    def fly(self, vert, hor):
        self.coords[0] += self.speed * hor
        self.coords[1] += self.speed * vert
        self.render()

    def render(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.circle(self.screen, pygame.Color('yellow'), (500, 500), 50)
        pygame.draw.circle(self.screen, pygame.Color('white'), tuple(self.coords), 25)

    def shoot(self, guns):
        pass

    def death(self):
        pass


class WarriorShip(Ship):
    def __init__(self, sprite, coords, hull, armor, mass):
        super().__init__(sprite, coords, hull, armor, mass)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, 1, 1, randint(0, 1)),  # guns
                               (randint(0, 1), 1),  # grab and shield
                               (1, randint(0, 1)),  # locator and scanner
                               randint(0, 1)]  # afterburner
        self.armor += 2


class PirateShip(Ship):
    def __init__(self, sprite, coords, hull, armor, mass):
        super().__init__(sprite, coords, hull, armor, mass)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, 1, randint(0, 1), 0),  # guns
                               (1, randint(0, 1)),  # grab and shield
                               (1, 1),  # locator and scanner
                               1]  # afterburner
        self.mass *= 0.75
        self.hull *= 0.8


class CargoShip(Ship):
    def __init__(self, sprite, coords, hull, armor, mass):
        super().__init__(sprite, coords, hull, armor, mass)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, randint(0, 1), 0, 0, 0),  # guns
                               (randint(0, 1), 0),  # grab and shield
                               (1, 0),  # locator and scanner
                               0]  # afterburner
        self.hull *= 1.5


class NomadShip(Ship):
    def __init__(self, sprite, coords, hull, armor, mass):
        super().__init__(sprite, coords, hull, armor, mass)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, randint(0, 1), 0, 0),  # guns
                               (1, randint(0, 1)),  # grab and shield
                               (1, randint(0, 1)),  # locator and scanner
                               randint(0, 1)]  # afterburner
        self.hull *= 0.9
