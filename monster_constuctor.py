import main
from monster import *

class MonsterConstuctor:
    def __init__(self):
        super().__init__()
        self.monster_list = ['Tree']
        self.pos = main.view.rect.center
        self.construtor_time = 0
        self.construtor_delay = 4

    def update(self):
        if self.construtor_time == self.construtor_delay:
            main.group.add(Tree((0,0)))
            self.construtor_time = 0
        self.construtor_time += 1
