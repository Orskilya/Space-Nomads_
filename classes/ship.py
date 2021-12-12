import pygame


class Ship:
    def __init__(self, sprite, coords, speed, xp=100, armor=0):
        self.coords = coords
        self.speed = speed
        self.xp = xp
        self.armor = armor
        self.sprite = sprite

    def get_coord(self):
        return self.coords

    def move(self, vert, hor):
        self.sprite.rect = self.sprite.rect.move(self.speed * hor, self.speed * vert)
        self.coords[0] += self.speed * hor
        self.coords[1] += self.speed * vert
