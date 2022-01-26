from math import cos, sin, pi
from random import randrange, choice
import pygame
import math
from Equipments import Engine, FuelTank, Grab, Shield, PhotonGun, Absorber, Destructor

fps = 60

products = ('product', 'medicine', 'alchogol', 'luxury', 'tech', 'weapon')
goods_shop = ('FuelTank', 'Engine', 'Grab', 'Shield', 'PhotonGun', 'Destructor', 'Absorber')


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
        self.rect = self.rect.move(coord[0] - self.size[0] // 2, coord[1] - self.size[1] // 2)
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


class Planet(Object):
    def __init__(self, sheet, columns, rows, size, coord, radius, speed, grad, *group):
        super().__init__(sheet, columns, rows, size, coord, *group)
        global products, goods_shop
        self.grad = grad
        self.radius = radius
        self.center = coord.copy()
        self.angular_speed = (speed / self.radius) * (pi / 180)
        self.shop = self.make_shop()
        self.market = {i: [randrange(100, 300), randrange(80, 200), randrange(70, 190)] for i in
                       products}  # name: number, purchase, selling
        self.count = 0
        self.images_speed = 6

    def update(self, **kwargs):
        self.coord[0] = self.center[0] + cos(self.grad) * self.radius - self.size[0] // 2
        self.coord[1] = self.center[1] + sin(self.grad) * self.radius - self.size[1] // 2
        self.rect.x = self.coord[0]
        self.rect.y = self.coord[1]
        self.grad += self.angular_speed
        if self.count == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
            self.mask = pygame.mask.from_surface(self.image)
        self.count = (self.count + 1) % self.images_speed

    def market_items(self):  # increasing number of the products
        for i in self.market.keys():
            self.market[i][0] += 10

    def products(self):
        return self.market

    def get_shop(self):
        return self.shop

    def shop_change(self, index):
        self.shop.pop(index)

    def shopping(self, index):
        return self.shop[index]

    def make_shop(self):
        shop = [[eval(f'{product}({randrange(0, 4)})') for _ in range(randrange(1, 4))] for
         product in goods_shop]
        normal_shop = list()
        for i in shop:
            i.sort(key=lambda x: x.tier)
            normal_shop.extend(i)
        return normal_shop

    def __str__(self):
        return 'Планета'

    def get_market(self):
        return self.market

    def market_change(self, item, number, selling=False):
        if selling:
            self.market[item][0] += number
        else:
            self.market[item][0] -= number


class Star(Object):
    def __init__(self, sheet, columns, rows, size, coord, *group):
        super().__init__(sheet, columns, rows, size, coord, *group)
        self.damage = 30
        self.count = 0
        self.images_speed = 5

    def get_damage(self):
        return self.damage

    def update(self, **kwargs):
        if self.count == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.image = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
            self.mask = pygame.mask.from_surface(self.image)
        self.count = (self.count + 1) % self.images_speed


class Station(Object):
    def __init__(self, sheet, columns, rows, size, coord, *group):
        global products, goods_shop
        super().__init__(sheet, columns, rows, size, coord, *group)
        self.shop = self.make_shop()

        self.market = {i: [randrange(20, 100), randrange(90, 300), randrange(90, 330)] for i in
                       products}  # name: number, purchase, selling

    def __str__(self):
        return 'station'

    def market_items(self):  # increasing number of the products
        for i in self.market.keys():
            self.market[i][0] += 10

    def get_shop(self):
        return self.shop

    def shop_change(self, index):
        self.shop.pop(index)

    def products(self):
        return self.market

    def make_shop(self):
        shop = [[eval(f'{product}({randrange(0, 3)})') for _ in range(randrange(1, 3))] for
         product in goods_shop]
        # t3 equipment generation
        for i in range(7):
            shop[i].append(eval(goods_shop[i] + '(3)'))
        normal_shop = list()
        for i in shop:
            i.sort(key=lambda x: x.tier)
            normal_shop.extend(i)
        return normal_shop

    def shopping(self, index):
        return self.shop[index]
