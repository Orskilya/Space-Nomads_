from random import randint
import pygame

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
        self.rect.x = self.coord[0] - self.size[0] // 2
        self.rect.y = self.coord[1] - self.size[1] // 2
        # Values
        self.hull = hull
        self.armor = armor
        self.mass = hull
        self.equipment = equipment  # list of classes
        self.hold = list()
        self.space = hull
        self.keys = []

    def fly(self, key=None, par=None):
        if par == 'go':
            self.keys.append(key)
        elif par == 'stop':
            del self.keys[self.keys.index(key)]
        if pygame.K_s in self.keys:
            self.coord[1] += 100 / fps
            self.rect.y = self.coord[1] - self.size[1] // 2
        elif pygame.K_w in self.keys:
            self.coord[1] -= 100 / fps
            self.rect.y = self.coord[1] - self.size[1] // 2
        if pygame.K_a in self.keys:
            self.coord[0] -= 100 / fps
            self.rect.x = self.coord[0] - self.size[0] // 2
        elif pygame.K_d in self.keys:
            self.coord[0] += 100 / fps
            self.rect.x = self.coord[0] - self.size[0] // 2

    def update(self, event=None, par=None):
        if par == 'fly' or self.keys:
            if not event:
                self.fly()
            elif event.type == pygame.KEYDOWN:
                self.fly(event.key, 'go')
            else:
                self.fly(event.key, 'stop')

    def shoot(self):
        pass

    def death(self):
        pass

    def get_hull(self):
        return self.hull

    def get_damage(self, dmg):
        self.hull -= dmg + self.armor

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
    def __init__(self, sprite, coord, hull, armor, equipment, *group):
        super().__init__(sprite, coord, hull, armor, equipment, *group)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, randint(0, 1), 0, 0),  # guns
                               (1, randint(0, 1)),  # grab and shield
                               (1, randint(0, 1)),  # locator and scanner
                               randint(0, 1)]  # afterburner
        self.hull *= 0.9

        # equipment setting up
        for i in self.equipment:
            if not self.slot_equipment[i.get_type()[0]][i.get_type()[1]]:
                self.equipment.remove(i)
                self.hold.append(i)
                self.mass += i.get_mass()
                self.space -= i.get_mass()


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
        for i in self.equipment:
            self.equipment.remove(i)
            self.hold.append(i)
            self.mass += i.get_mass()
            self.space -= i.get_mass()
