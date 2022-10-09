from instance import Instance

class Tree(Instance):
    def __init__(self, pos):
        super().__init__(pos)
        self.pos = pos