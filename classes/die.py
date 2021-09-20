import random

class Die(object):

    def __init__(self): # default value of die
        self.value = -1
        self.need_roll = True

    def roll(self): # roll die method
        if self.need_roll:
            self.value = random.randint(1, 6)
            self.need_roll = False