from random import randint
import pygame

difficult = 1
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
        self.hold = {'product': 100, 'medicine': 100, 'alchogol': 100, 'luxury': 100, 'tech': 100, 'weapon': 100}
        self.space = hull
        self.keys = []
        self.mask = pygame.mask.from_surface(self.image)

    def death(self):
        pass

    def get_hull(self):
        return self.hull

    def get_space(self):
        return self.space

    def change_space(self, new_mass, old_mass):
        self.space -= new_mass
        self.space += old_mass

    def get_damage(self, dmg):
        self.hull -= dmg - self.armor
        if self.hull <= 0:
            self.kill()

    def reload(self):
        pass

    def get_hold(self):
        return self.hold

    def hold_upgraide(self, item, number=0, add=True):
        if add:
            self.hold[item] += number
        else:
            self.hold[item] = number


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
                               (1, randint(0, 1), 0),  # guns
                               (randint(0, 1), 0),  # grab and shield
                               (1, 0),  # locator and scanner
                               0]  # afterburner
        self.hull *= 1.5


class NomadShip(Ship):
    def __init__(self, images, coord, hull, armor, equipment, camera, scree_size, *group):
        super().__init__(images[8], coord, hull, armor, equipment, *group)
        self.slot_equipment = [[1, 1],  # engine and fuel tank
                               [1, 1, randint(0, 1), 0, 0],  # guns
                               [1, 1],  # grab and shield
                               [1, randint(0, 1)]]  # locator and scanner
        self.camera = camera
        self.rect.x = scree_size[0] // 2 - self.size[0] // 2
        self.rect.y = scree_size[1] // 2 - self.size[1] // 2
        self.equipment_setting()
        self.death_flag = False
        self.end_jump = False
        self.images = images
        self.cur_frame = 0

    def fly(self, key=None, par=None):
        speed = self.slot_equipment[0][0].get_speed()
        self.dx = 0
        self.dy = 0
        if par == 'go':
            if key in [pygame.K_s, pygame.K_w, pygame.K_a, pygame.K_d]:
                self.keys.append(key)
                self.cur_frame = None
        elif par == 'stop':
            if key in self.keys:
                del self.keys[self.keys.index(key)]
        if pygame.K_s in self.keys:
            self.coord[1] += speed // fps
            self.dy = -(speed // fps)
            self.camera.update(self)
            self.cur_frame = 4
        elif pygame.K_w in self.keys:
            self.coord[1] -= speed // fps
            self.dy = speed // fps
            self.camera.update(self)
            self.cur_frame = 0
        if pygame.K_a in self.keys:
            self.coord[0] -= speed // fps
            self.dx = speed // fps
            self.camera.update(self)
            if self.cur_frame == 0:
                self.cur_frame = 1
            elif self.cur_frame == 4:
                self.cur_frame = 3
            else:
                self.cur_frame = 2
        elif pygame.K_d in self.keys:
            self.coord[0] += speed // fps
            self.dx = -(speed // fps)
            self.camera.update(self)
            if self.cur_frame == 0:
                self.cur_frame = 7
            elif self.cur_frame == 4:
                self.cur_frame = 5
            else:
                self.cur_frame = 6

    def __str__(self):
        return 'Корабль героя'

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
        if self.keys:
            self.image = self.images[self.cur_frame]
        else:
            self.image = self.images[self.cur_frame + 8]
        if not self.end_jump and self.slot_equipment[0][0].tier == 3 and \
                self.slot_equipment[0][1] != 1 \
                and self.slot_equipment[0][1].tier == 3:
            self.end_jump = True
        self.reload()

    def shoot(self, target):
        self.slot_equipment[1][0].shoot(
            [self.rect.x + self.size[0] // 2, self.rect.y + self.size[1] // 2], self, target)

    def equipment_setting(self):
        for i in self.equipment:
            e_type = i.get_type()
            if self.slot_equipment[e_type[0]][e_type[1]] != 0:
                self.slot_equipment[e_type[0]][e_type[1]] = i
                self.space -= i.get_mass()

    def new_equipment(self, item):
        i1, i2 = item.get_type()
        self.slot_equipment[i1][i2] = item

    def get_damage(self, dmg):
        self.hull -= dmg - dmg * self.slot_equipment[2][1].get_defend() // 100 - self.armor
        if self.hull <= 0:
            self.death_flag = True

    def get_equipment(self, type):
        return self.slot_equipment[type[0]][type[1]]

    def repair(self):
        self.hull = 500

    def reload(self):
        if self.slot_equipment[1][0] != 1 and self.slot_equipment != 0:
            self.slot_equipment[1][0].reloading()


class Kristalid(Ship):
    def __init__(self, sprite, coord, hull, armor, equipment, hero, *group):
        super().__init__(sprite, coord, hull, armor, equipment, *group)
        self.slot_equipment = [[1, 1],  # engine and fuel tank
                               [1, 1, 1, 1, 1],  # guns
                               [1, 1],  # grab and shield
                               [1, 1]]  # locator and scanner
        self.hull *= difficult
        self.armor += round(difficult / 100)
        self.shoot_time = 0
        self.first = True
        self.equipment_setting()
        self.hero = hero  # Для добавления денег и уничтожений

    def __str__(self):
        return 'Кристалид'

    def fly(self, hero_coord, distance):
        speed = self.slot_equipment[0][0].get_speed()
        x = abs(hero_coord[0] - self.rect.x)
        y = abs(hero_coord[1] - self.rect.y)
        t = distance / (speed // fps)
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
        if 0 < distance <= 1000:
            self.fly(hero_coord, distance)
            if self.slot_equipment[1][0] != 1:
                if self.slot_equipment[1][0].distance >= distance:
                    self.shoot(hero_coord)
        else:
            if self.rect.x != self.start_point[0] and self.rect.y != self.start_point[1]:
                distance = ((self.start_point[0] - self.rect.x) ** 2 + (
                        self.start_point[1] - self.rect.y) ** 2) ** 0.5
                self.fly(self.start_point, distance)
        self.reload()

    def shoot(self, hero_coord):
        self.slot_equipment[1][0].shoot(
            [self.rect.x + self.size[0] // 2, self.rect.y + self.size[1] // 2], self, hero_coord)

    def equipment_setting(self):
        for i in self.equipment:
            e_type = i.get_type()
            if self.slot_equipment[e_type[0]][e_type[1]] != 0:
                self.slot_equipment[e_type[0]][e_type[1]] = i
                self.space -= i.get_mass()

    def get_damage(self, dmg):
        self.hull -= dmg - self.armor
        if self.hull <= 0:
            self.kill()
            self.hero.destroy_enemy()

    def reload(self):
        if self.slot_equipment[1][0] != 1 and self.slot_equipment != 0:
            self.slot_equipment[1][0].reloading()
