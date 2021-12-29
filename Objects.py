from math import cos, sin, pi
from random import randrange
import pygame

products = (
'Питание', 'Медикаменты', 'Алкоголь', 'Минералы', 'Роскошь', 'Техника', 'Оружие', 'Наркотики')
equipments = (1,)  # tuple. Add to main code


class Object(pygame.sprite.Sprite):
    def __init__(self, sprite, coords, *group):
        super().__init__(*group)
        self.coords = coords  # list
        self.image = sprite
        self.coords = coords  # list
        self.rect = self.image.get_rect()
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1]

    def render(self):
        pass


class Planet(Object):
    def __init__(self, sprite, coords, radius, speed, *group):
        global products, equipments
        self.center = coords.copy()
        self.grad = 0
        super().__init__(sprite, coords, *group)
        self.shop = []  # list
        self.market = {i: [randrange(70, 300), randrange(80, 200), randrange(70, 190)] for i in
                       products}  # name: number, purchase, selling
        self.radius = radius
        self.speed = (speed / self.radius) * (pi / 180)

    def update(self):
        self.coords[0] = self.center[0] + cos(self.grad) * self.radius
        self.coords[1] = self.center[1] + sin(self.grad) * self.radius
        self.rect.x = self.coords[0]
        self.rect.y = self.coords[1]
        self.grad += self.speed

    def market_items(self):  # increasing number of the products
        for i in self.market.keys():
            self.market[i][0] += 10


class Star(Object):
    def __init__(self, coords, image):
        super().__init__(coords, image)
        self.damage = 30

    def get_damage(self):
        return self.damage


class Station(Object):
    def __init__(self, coords, image):
        super().__init__(coords, image)
        self.shop = []  # list
        self.market = {i: [randrange(20, 100), randrange(90, 300), randrange(90, 330)] for i in
                       products}  # name: number, purchase, selling

    def market_items(self):  # increasing number of the products
        for i in self.market.keys():
            self.market[i][0] += 10
