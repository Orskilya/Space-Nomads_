import pygame


class Engine:
    def __init__(self, speed, jump, price, mass, set=False):
        self.speed = speed
        self.jump = jump
        self.price = price
        self.mass = mass
        self.set = set


class FuelTank:
    def __init__(self, fuel, price, mass, set=False):
        self.fuel = fuel
        self.price = price
        self.mass = mass
        self.set = set


class Grab:
    def __init__(self, power, dist, price, mass, set=False):
        self.power = power
        self.dist = dist
        self.price = price
        self.mass = mass
        self.set = set


class Shield:
    def __init__(self, defend, price, mass, set=False):
        self.defend = defend
        self.price = price
        self.mass = mass
        self.set = set


class Locator:
    def __init__(self, dist, price, mass, set=False):
        self.dist = dist
        self.price = price
        self.mass = mass
        self.set = set


class Scanner:
    def __init__(self, scan, price, mass, set=False):
        self.scan = scan
        self.price = price
        self.mass = mass
        self.set = set


class Gun:
    def __init__(self, mass, price):
        self.mass = mass
        self.type = (1, 0)
        self.price = price

    def shoot(self):
        pass

    def get_mass(self):
        return self.mass

    def get_type(self):
        return self.type


class PhotonGun(Gun):
    def __init__(self, mass, price):
        super().__init__(mass, price)
        self.shoot_animation = None
        self.damage = (5, 8)
        self.distance = 300
        self.price *= 0.1

    def get_animation(self):
        return self.shoot_animation


class LaserGun(Gun):
    def __init__(self, mass, price):
        super().__init__(mass, price)
        self.shoot_animation = None
        self.damage = (9, 10)
        self.distance = 250
        self.price *= 0.2

    def get_animation(self):
        return self.shoot_animation


class Destructor(Gun):
    def __init__(self, mass, price):
        super().__init__(mass, price)
        self.shoot_animation = None
        self.damage = (20, 25)
        self.distance = 200
        self.price *= 0.6

    def get_animation(self):
        return self.shoot_animation


class Catcher(Gun):
    def __init__(self, mass, price):
        super().__init__(mass, price)
        self.shoot_animation = None
        self.damage = (2, 5)
        self.distance = 400
        self.speed_down = 0.1
        self.price *= 1

    def get_animation(self):
        return self.shoot_animation


class Absorber(Gun):
    def __init__(self, mass, price):
        super().__init__(mass, price)
        self.shoot_animation = None
        self.damage = (50, 60)
        self.distance = 250
        self.price *= 1.5

    def get_animation(self):
        return self.shoot_animation
