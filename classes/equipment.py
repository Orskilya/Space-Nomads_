class Engine:
    def __init__(self, speed, jump, price, weight, set=False):
        self.speed = speed
        self.jump = jump
        self.price = price
        self.weight = weight
        self.set = set


class FuelTank:
    def __init__(self, fuel, price, weight, set=False):
        self.fuel = fuel
        self.price = price
        self.weight = weight
        self.set = set
