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


class Scaner:
    def __init__(self, scan, price, mass, set=False):
        self.scan = scan
        self.price = price
        self.mass = mass
        self.set = set
