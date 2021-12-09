from random import randint


class Ship:
    def __init__(self, image, coords, hull, armor, mass):
        self.image = image
        self.coords = coords  # list
        self.hull = hull
        self.armor = armor
        self.mass = mass

    def draw(self, screen):
        pass

    def fly(self, coords, speed):
        pass

    def shoot(self, guns):
        pass

    def death(self):
        pass


class WarriorShip(Ship):
    def __init__(self, image, coords, hull, armor, mass):
        super().__init__(image, coords, hull, armor, mass)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, 1, 1, randint(0, 1)),  # guns
                               (randint(0, 1), 1),  # grab and shield
                               (1, randint(0, 1)),  # locator and scanner
                               randint(0, 1)]  # afterburner
        self.armor += 2


class PirateShip(Ship):
    def __init__(self, image, coords, hull, armor, mass):
        super().__init__(image, coords, hull, armor, mass)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, 1, randint(0, 1), 0),  # guns
                               (1, randint(0, 1)),  # grab and shield
                               (1, 1),  # locator and scanner
                               1]  # afterburner
        self.mass *= 0.75
        self.hull *= 0.8


class CargoShip(Ship):
    def __init__(self, image, coords, hull, armor, mass):
        super().__init__(image, coords, hull, armor, mass)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, randint(0, 1), 0, 0, 0),  # guns
                               (randint(0, 1), 0),  # grab and shield
                               (1, 0),  # locator and scanner
                               0]  # afterburner
        self.hull *= 1.5


class NomadShip(Ship):
    def __init__(self, image, coords, hull, armor, mass):
        super().__init__(image, coords, hull, armor, mass)
        self.slot_equipment = [(1, 1),  # engine and fuel tank
                               (1, 1, randint(0, 1), 0, 0),  # guns
                               (1, randint(0, 1)),  # grab and shield
                               (1, randint(0, 1)),  # locator and scanner
                               randint(0, 1)]  # afterburner
        self.hull *= 0.9
