from math import cos, sin
from random import randrange
import pygame

products = (
'Питание', 'Медикаменты', 'Алкоголь', 'Минералы', 'Роскошь', 'Техника', 'Оружие', 'Наркотики')
equipments = (1,)  # tuple. Add to main code


class Object:
    def __init__(self, coords, image):
        self.coords = coords  # list
        self.image = image

    def render(self):
        pass


class Planet(Object):
    def __init__(self, coords, image, radius, distance, w):
        global products, equipments
        super().__init__(coords, image)
        self.shop = []  # list
        self.market = {i: [randrange(70, 300), randrange(80, 200), randrange(70, 190)] for i in
                       products}  # name: number, purchase, selling
        self.radius = radius
        self.distance = distance
        self.w = w  # angular velocity of the planet rotation

    def move(self, t):
        x = self.distance * cos(self.w * t)
        y = self.distance * sin(self.w * t)
        return x, y

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
