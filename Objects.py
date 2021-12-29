from math import cos, sin, pi
from random import randrange
import pygame

products = (
'Питание', 'Медикаменты', 'Алкоголь', 'Минералы', 'Роскошь', 'Техника', 'Оружие', 'Наркотики')
equipments = (1,)  # tuple. Add to main code


class Object(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, size, coord, *group):
        super().__init__(*group)
        self.coord = coord  # list
        self.size = size
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.rect = self.rect.move(coord[0], coord[1])

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


class Planet(Object):
    def __init__(self, sheet, columns, rows, size, coord, radius, speed, *group):
        super().__init__(sheet, columns, rows, size, coord, *group)
        global products, equipments
        self.grad = 0
        self.radius = radius
        self.center = coord.copy()
        self.speed = (speed / self.radius) * (pi / 180)
        self.shop = []  # list
        self.market = {i: [randrange(70, 300), randrange(80, 200), randrange(70, 190)] for i in
                       products}  # name: number, purchase, selling
        self.count = 0
        self.speed_1 = 5

    def update(self):
        self.coord[0] = self.center[0] + cos(self.grad) * self.radius
        self.coord[1] = self.center[1] + sin(self.grad) * self.radius
        self.rect.x = self.coord[0]
        self.rect.y = self.coord[1]
        self.grad += self.speed

        if self.count == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.count = (self.count + 1) % self.speed_1

    def market_items(self):  # increasing number of the products
        for i in self.market.keys():
            self.market[i][0] += 10


class Star(Object):
    def __init__(self, coord, image):
        super().__init__(coord, image)
        self.damage = 30

    def get_damage(self):
        return self.damage


class Station(Object):
    def __init__(self, coord, image):
        super().__init__(coord, image)
        self.shop = []  # list
        self.market = {i: [randrange(20, 100), randrange(90, 300), randrange(90, 330)] for i in
                       products}  # name: number, purchase, selling

    def market_items(self):  # increasing number of the products
        for i in self.market.keys():
            self.market[i][0] += 10
