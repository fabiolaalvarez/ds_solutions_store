import random


class Product:
    def __init__(self, name: str, price: int = 10,
                 weight: int = 20, flammability: float = 0.5,
                 identifier: int = random.randint(1000000, 9999999)):
        self.name = name
        self.price = price
        self.weight = weight
        self.flammability = flammability
        self.identifier = identifier

    def stealability(self):
        steal = self.price / self.weight
        if steal < 0.5:
            return 'Not so stealable...'
        elif 0.5 <= steal < 1.0:
            return 'Kinda stealable.'
        else:
            return 'Very stealable!'

    def explode(self):
        exp = self.flammability * self.weight
        if exp < 10:
            return '...fizzle'
        elif 10 <= exp < 50:
            return '...boom!'
        else:
            return'...BABOOM!!'


class BoxingGlove(Product):
    def __init__(self, name: str, weight: int = 10):
        super().__init__(name)
        self.weight = weight

    def punch(self):
        if self.weight < 5:
            print('That tickles.')
        elif 5 <= self.weight < 15:
            print('Hey that hurt!')
        else:
            print('OUCH!')

    def explode(self):
        print("...it's a glove")
