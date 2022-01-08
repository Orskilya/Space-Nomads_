from random import randint
import pygame
from Objects import Bullet

difficult = 50
fps = 60


class Ship(pygame.sprite.Sprite):
    def __init__(self, sprite, coord, hull, armor, equipment, *group):
        # Work with sprite
        super().__init__(*group)
        self.image = sprite
        self.coord = coord  # list
        self.rect = self.image.get_rect()
        self.size = self.rect.size
        self.coord[0] -= self.size[0] // 2
        self.coord[1] -= self.size[1] // 2
        self.rect.x = self.coord[0]
        self.rect.y = self.coord[1]
        # Values
        self.hull = hull
        self.armor = armor
        self.mass = hull
        self.equipment = equipment  # list of classes
        self.hold = list()
        self.space = hull
        self.keys = []
        self.mask = pygame.mask.from_surface(self.image)
        self.bullets = []

    def fly(self):
        pass

    def update(self):
        pass

    def shoot(self):
        pass

    def death(self):
        pass

    def get_hull(self):
        return self.hull

    def get_damage(self, dmg):
        self.hull -= dmg - self.armor

    def overmass(self):
        return 'Ваш корабль не может поднять столько груза!'


class WarriorShip(Ship):
    def __init__(self, sprite, coord, hull, armor, equipment, *group):
        super().__init__(sprite, coord, hull, armor, equipment, *group)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, 1, 1, randint(0, 1)),  # guns
                               (randint(0, 1), 1),  # grab and shield
                               (1, randint(0, 1)),  # locator and scanner
                               randint(0, 1)]  # afterburner
        self.armor += 2

        # equipment setting up
        for i in self.equipment:
            if not self.slot_equipment[i.get_type()[0]][i.get_type()[1]]:
                self.equipment.remove(i)
                self.hold.append(i)
                self.mass += i.get_mass()
                self.space -= i.get_mass()


class PirateShip(Ship):
    def __init__(self, sprite, coord, hull, armor, equipment, *group):
        super().__init__(sprite, coord, hull, armor, equipment, *group)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, 1, randint(0, 1), 0),  # guns
                               (1, randint(0, 1)),  # grab and shield
                               (1, 1),  # locator and scanner
                               1]  # afterburner
        self.mass *= 0.75
        self.hull *= 0.8

        # equipment setting up
        for i in self.equipment:
            if not self.slot_equipment[i.get_type()[0]][i.get_type()[1]]:
                self.equipment.remove(i)
                self.hold.append(i)
                self.mass += i.get_mass()
                self.space -= i.get_mass()


class CargoShip(Ship):
    def __init__(self, sprite, coord, hull, armor, equipment, *group):
        super().__init__(sprite, coord, hull, armor, equipment, *group)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, randint(0, 1), 0, 0, 0),  # guns
                               (randint(0, 1), 0),  # grab and shield
                               (1, 0),  # locator and scanner
                               0]  # afterburner
        self.hull *= 1.5

        # equipment setting up
        for i in self.equipment:
            if not self.slot_equipment[i.get_type()[0]][i.get_type()[1]]:
                self.equipment.remove(i)
                self.hold.append(i)
                self.mass += i.get_mass()
                self.space -= i.get_mass()


class NomadShip(Ship):
    def __init__(self, sprite, coord, hull, armor, equipment, camera, scree_size, *group):
        super().__init__(sprite, coord, hull, armor, equipment, *group)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, randint(0, 1), 0, 0),  # guns
                               (1, randint(0, 1)),  # grab and shield
                               (1, randint(0, 1)),  # locator and scanner
                               randint(0, 1)]  # afterburner
        self.hull *= 0.9

        # equipment setting up
        # for i in self.equipment:
        #    if not self.slot_equipment[i.get_type()[0]][i.get_type()[1]]:
        #        self.equipment.remove(i)
        #        self.hold.append(i)
        #        self.mass += i.get_mass()
        #        self.space -= i.get_mass()
        self.camera = camera
        self.rect.x = scree_size[0] // 2 - self.size[0] // 2
        self.rect.y = scree_size[1] // 2 - self.size[1] // 2

    def fly(self, key=None, par=None):
        self.dx = 0
        self.dy = 0
        if par == 'go':
            if key in [pygame.K_s, pygame.K_w, pygame.K_a, pygame.K_d]:
                self.keys.append(key)
        elif par == 'stop':
            del self.keys[self.keys.index(key)]
        if pygame.K_s in self.keys:
            self.coord[1] += 300 // fps
            self.dy = -(300 // fps)
            self.camera.update(self)
        elif pygame.K_w in self.keys:
            self.coord[1] -= 300 // fps
            self.dy = 300 // fps
            self.camera.update(self)
        if pygame.K_a in self.keys:
            self.coord[0] -= 300 // fps
            self.dx = 300 // fps
            self.camera.update(self)
        elif pygame.K_d in self.keys:
            self.coord[0] += 300 // fps
            self.dx = -(300 // fps)
            self.camera.update(self)

    def update(self, event=None, par=None, **kwargs):
        if par == 'shoot':
            self.shoot(event.pos)
        elif par == 'fly' or self.keys:
            if not event:
                self.fly()
            elif event.type == pygame.KEYDOWN:
                self.fly(event.key, 'go')
            else:
                self.fly(event.key, 'stop')

    def shoot(self, tarjet):
        gr = self.equipment[0].groups
        self.bullets.append(
            Bullet(self.equipment[0].bullet_image,
                   [self.rect.x + self.size[0] // 2, self.rect.y + self.size[1] // 2], self, tarjet,
                   400, 2000, 100, gr[0], gr[1]))


class Kristalid(Ship):
    def __init__(self, sprite, coord, hull, armor, equipment, *group):
        super().__init__(sprite, coord, hull, armor, equipment, *group)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, 1, 1, 1),  # guns
                               (1, 1),  # grab and shield
                               (1, 1),  # locator and scanner
                               1]  # afterburner
        self.hull *= difficult
        self.armor += round(difficult / 100)

        # equipment setting up
        # for i in self.equipment:
        #     self.equipment.remove(i)
        #     self.hold.append(i)
        #     self.mass += i.get_mass()
        #     self.space -= i.get_mass()
        self.shoot_time = 0
        self.first = True

    def fly(self, hero_coord, distance):
        x = abs(hero_coord[0] - self.rect.x)
        y = abs(hero_coord[1] - self.rect.y)
        t = distance / (200 // fps)
        s_x = x / t
        s_y = y / t
        if self.rect.x > hero_coord[0]:
            self.rect.x -= s_x
        else:
            self.rect.x += s_x
        if self.rect.y > hero_coord[1]:
            self.rect.y -= s_y
        else:
            self.rect.y += s_y

    def update(self, hero_coord):
        if self.first:
            self.first = False
            self.start_point = [self.rect.x, self.rect.y]
        distance = ((hero_coord[0] - self.rect.x) ** 2 + (hero_coord[1] - self.rect.y) ** 2) ** 0.5
        if 0 < distance <= 500:
            self.fly(hero_coord, distance)
            # self.shoot_time = (self.shoot_time + 1) % (fps // 3)
            # if self.shoot_time == 0:
            #     self.shoot(hero_coord)
        else:
            if self.rect.x != self.start_point[0] and self.rect.y != self.start_point[1]:
                distance = ((self.start_point[0] - self.rect.x) ** 2 + (
                            self.start_point[1] - self.rect.y) ** 2) ** 0.5
                self.fly(self.start_point, distance)

    def shoot(self, hero_coord):
        gr = self.equipment[0].groups
        tarjet = hero_coord
        self.bullets.append(
            Bullet(self.equipment[0].bullet_image,
                   [self.rect.x + self.size[0] // 2, self.rect.y + self.size[1] // 2], self, tarjet,
                   1000, 2000, 100, gr[0], gr[1]))

    def __str__(self):
        return 'Кристалид'
