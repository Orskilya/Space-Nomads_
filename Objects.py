from random import randrange

products = ('Питание', 'Медикаменты', 'Алкоголь', 'Минералы', 'Роскошь', 'Техника', 'Оружие', 'Наркотики')
equipments = (1, )  # tuple. Add to main code


class Object:
    def __init__(self, coords, image):
        self.coords = coords  # list
        self.image = image

    def render(self):
        pass


class Planet(Object):
    def __init__(self, coords, image, radius):
        global products, equipments
        super().__init__(coords, image)
        self.shop = []  # list
        self.market = {i: [randrange(70, 300), randrange(80, 200)] for i in products}  # name: number, price
        self.radius = radius

    def move(self):
        pass

    def market_items(self):  # increasing number of the products
        for i in self.market:
            self.market[i][0] *= 1.1


class Star(Object):
    def __init__(self, coords, image):
        super().__init__(coords, image)
        self.damage = 30
