from Bullet import Bullet


class Engine:
    def __init__(self, tier):
        self.engines_img = ['engine0.png', 'engine1.png', 'engine2.png', 'engine3.png']
        self.names = ['Diving Engine', 'Splash Engine', 'Graviton Engine', 'Stancer Engine']
        self.tier = tier
        self.type = (0, 0)

        # features
        self.name = self.names[self.tier]
        self.speed = 300 + 150 * self.tier
        self.jump = 15 + self.tier
        self.price = 800 + 1000 * self.tier
        self.mass = 20 + 5 * self.tier
        self.img = self.engines_img[self.tier]

    def get_img(self):
        return self.img

    def get_mass(self):
        return self.mass

    def get_speed(self):
        return self.speed

    def get_features(self):
        return {'speed': self.speed, 'jump': self.jump, 'tier': self.tier}

    def get_type(self):
        return self.type

    def get_price(self):
        return self.price

    def get_name(self):
        return self.name


class FuelTank:
    def __init__(self, tier):
        self.fuel_tank_img = ['fueltank0.png', 'fueltank1.png', 'fueltank2.png', 'fueltank3.png']
        self.names = ['Hyper Liquid Fuel', 'Proto Bubbly Fuel', 'Endocluster Fuel', 'Gyroscopic Fuel']
        self.tier = tier
        self.type = (0, 1)

        self.mass = 15 + 5 * self.tier
        self.name = self.names[self.tier]
        self.fuel = 15 + self.tier
        self.price = 500 + 1000 * self.tier
        self.img = self.fuel_tank_img[self.tier]

    def get_img(self):
        return self.img

    def get_features(self):
        return {'fuel': self.fuel, 'tier': self.tier}

    def get_mass(self):
        return self.mass

    def get_type(self):
        return self.type

    def get_price(self):
        return self.price

    def get_name(self):
        return self.name


class Grab:
    def __init__(self, tier):
        self.grab_img = ['grab0.png', 'grab1.png', 'grab2.png', 'grab3.png']
        self.names = ['Activator Grab', 'Touch Grab', 'Erymetroid Grab', 'Optowave Grab']
        self.tier = tier
        self.type = (2, 0)

        self.name = self.names[self.tier]
        self.power = 20 + self.tier * 15
        self.dist = 100 + self.tier * 25
        self.price = 900 + 1100 * self.tier
        self.mass = 20 + 5 * self.tier
        self.img = self.grab_img[self.tier]

    def get_img(self):
        return self.img

    def get_features(self):
        return {'power': self.power, 'dist': self.dist, 'tier': self.tier}

    def get_type(self):
        return self.type

    def get_mass(self):
        return self.mass

    def get_price(self):
        return self.price

    def get_name(self):
        return self.name


class Shield:
    def __init__(self, tier):
        self.shield_img = ['shield0.png', 'shield1.png', 'shield2.png', 'shield3.png']
        self.names = ['Reticulate Shield', 'Polygonal Grab', 'Zonal Shield', 'Ultraplasm shield']
        self.tier = tier
        self.type = (2, 1)

        self.name = self.names[self.tier]
        self.defend = 5 + 15 * self.tier
        self.price = 1500 + 1500 * self.tier
        self.mass = 30 + 10 * self.tier
        self.img = self.shield_img[self.tier]

    def get_defend(self):
        return self.defend

    def get_img(self):
        return self.img

    def get_features(self):
        return {'defend': self.defend, 'tier': self.tier}

    def get_type(self):
        return self.type

    def get_mass(self):
        return self.mass

    def get_price(self):
        return self.price

    def get_name(self):
        return self.name


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


class PhotonGun:
    def __init__(self, tier, groups=None, bullet_image=None):
        self.img = 'photongun.png'
        self.tier = tier
        if bullet_image:
            self.bullet_image = bullet_image
        self.bullet_size = (50, 50)
        self.groups = groups
        self.type = (1, 0)

        self.name = 'Photon Gun'
        self.damage = (5 + self.tier, 10 + self.tier)
        self.distance = 500 + self.tier * 25
        self.price = 700 + self.tier * 100
        self.mass = 11 + 3 * self.tier
        self.bullet_speed = 500 + self.tier * 250
        self.bullets = []

    def __str__(self):
        return 'photon'

    def get_img(self):
        return self.img

    def get_features(self):
        return {'damage': self.damage, 'distance': self.distance, 'tier': self.tier}

    def get_type(self):
        return self.type

    def get_mass(self):
        return self.mass

    def set_bullet_img(self, image):
        self.bullet_image = image

    def set_groups(self, *args):
        self.groups = args

    def shoot(self, start_coord, owner, target_coord):
        self.bullets.append(Bullet(self.bullet_image, start_coord, owner, target_coord,
                                   self.bullet_speed, self.distance, self.damage, self.groups[0],
                                   self.groups[1]))

    def get_price(self):
        return self.price

    def get_name(self):
        return self.name

    def get_size(self):
        return self.bullet_size


class Destructor:
    def __init__(self, tier, groups=None, bullet_image=None):
        self.img = 'destructor.png'
        self.tier = tier
        if bullet_image:
            self.bullet_image = bullet_image
        self.bullet_size = (50, 40)
        self.groups = groups
        self.type = (1, 0)

        self.name = 'Destructor'
        self.damage = (20 + round(self.tier * 3.3), 25 + round(self.tier * 3.3))
        self.distance = 700 + self.tier * 50
        self.price = 5000 + self.tier * 2000
        self.mass = 30 + 15 * self.tier
        self.bullet_speed = 1000 + self.tier * 250
        self.bullets = []

    def __str__(self):
        return 'destructor'

    def get_img(self):
        return self.img

    def get_features(self):
        return {'damage': self.damage, 'distance': self.distance, 'tier': self.tier}

    def get_type(self):
        return self.type

    def get_mass(self):
        return self.mass

    def set_bullet_img(self, image):
        self.bullet_image = image

    def set_groups(self, *args):
        self.groups = args

    def shoot(self, start_coord, owner, target_coord):
        self.bullets.append(Bullet(self.bullet_image, start_coord, owner, target_coord,
                                   self.bullet_speed, self.distance, self.damage, self.groups[0],
                                   self.groups[1]))

    def get_price(self):
        return self.price

    def get_name(self):
        return self.name

    def get_size(self):
        return self.bullet_size


class Absorber:
    def __init__(self, tier, groups=None):
        self.img = 'absorber.png'
        self.tier = tier
        self.bullet_image = 'absorber_bullet.png'
        self.bullet_size = (10, 10)
        self.groups = groups
        self.type = (1, 0)

        self.name = 'Absorber'
        self.damage = (50 + round(self.tier * 13.3), 60 + round(self.tier * 13.3))
        self.distance = 400 - round(self.tier * 16.6)
        self.price = 10000 + 10000 * self.tier
        self.mass = 50 + 50 * self.tier

    def __str__(self):
        return 'absorber'

    def get_img(self):
        return self.img

    def get_features(self):
        return {'damage': self.damage, 'distance': self.distance, 'tier': self.tier}

    def get_type(self):
        return self.type

    def get_mass(self):
        return self.mass

    def set_bullet_img(self, image):
        self.bullet_image = image

    def set_groups(self, *args):
        self.groups = args

    def get_price(self):
        return self.price

    def get_name(self):
        return self.name

    def get_size(self):
        return self.bullet_size
