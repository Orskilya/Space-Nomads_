class Hero:
    def __init__(self, ship, money, name):
        self.ship = ship
        self.money = money
        self.name = name
        self.score = 0

    def get_money(self):
        return self.money

    def money_change(self, amount):
        if self.money + amount > 1000000:
            self.money = 1000000
        else:
            self.money += amount

    def get_ship(self):
        return self.ship