class Engine:
    def __init__(self, speed, jump, price, mass, setup=False):
        self.speed = speed
        self.jump = jump
        self.price = price
        self.mass = mass
        self.setup = setup

    def get_speed(self):
        return self.speed

    def get_jump(self):
        return self.jump

    def setup(self, setup):
        self.setup = setup


class FuelTank:
    def __init__(self, fuel, price, mass, setup=False):
        self.fuel = fuel
        self.price = price
        self.mass = mass
        self.setup = setup

    def get_fuel(self):
        return self.fuel

    def setup(self, setup):
        self.setup = setup


class Grab:
    def __init__(self, power, dist, price, mass, setup=False):
        self.power = power
        self.dist = dist
        self.price = price
        self.mass = mass
        self.setup = setup

    def get_power_dist(self):
        return self.power, self.dist

    def setup(self, setup):
        self.setup = setup


class Shield:
    def __init__(self, defend, price, mass, setup=False):
        self.defend = defend
        self.price = price
        self.mass = mass
        self.setup = setup

    def get_defend(self):
        return self.defend

    def setup(self, setup):
        self.setup = setup


class Locator:
    def __init__(self, dist, price, mass, setup=False):
        self.dist = dist
        self.price = price
        self.mass = mass
        self.setup = setup

    def setup(self, setup):
        self.setup = setup

    def get_dist(self):
        return self.dist


class Scanner:
    def __init__(self, scan, price, mass, setup=False):
        self.scan = scan
        self.price = price
        self.mass = mass
        self.setup = setup

    def setup(self, setup):
        self.setup = setup

    def get_scan(self):
        return self.scan


class Gun:
    def __init__(self, mass, price, setup=False):
        self.mass = mass
        self.type = (1, 0)
        self.price = price
        self.setup = setup

    def shoot(self):
        pass

    def get_mass(self):
        return self.mass

    def get_type(self):
        return self.type

    def setup(self, setup):
        self.setup = setup


class PhotonGun(Gun):
    def __init__(self, mass, price):
        super().__init__(mass, price)
        self.image = None
        self.damage = (5, 8)
        self.distance = 300
        self.price *= 0.1

    def get_image(self):
        return self.image


class LaserGun(Gun):
    def __init__(self, mass, price):
        super().__init__(mass, price)
        self.image = None
        self.damage = (9, 10)
        self.distance = 250
        self.price *= 0.2

    def get_image(self):
        return self.image


class Destructor(Gun):
    def __init__(self, mass, price):
        super().__init__(mass, price)
        self.image = None
        self.damage = (20, 25)
        self.distance = 200
        self.price *= 0.6

    def get_image(self):
        return self.image


class Catcher(Gun):
    def __init__(self, mass, price):
        super().__init__(mass, price)
        self.image = None
        self.damage = (2, 5)
        self.distance = 400
        self.speed_down = 0.1
        self.price *= 1

    def get_image(self):
        return self.image


class Absorber(Gun):
    def __init__(self, mass, price):
        super().__init__(mass, price)
        self.image = None
        self.damage = (50, 60)
        self.distance = 250
        self.price *= 1.5

    def get_image(self):
        return self.image


class TestGun:
    def __init__(self, bullet_image, groups, mass, price, setup=False):
        self.mass = mass
        self.type = (1, 0)
        self.price = price
        self.setup = setup
        self.bullet_image = bullet_image
        self.groups = groups

    def get_mass(self):
        return self.mass

    def get_type(self):
        return self.type

    def setup(self, setup):
        self.setup = setup
