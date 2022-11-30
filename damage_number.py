from instance import TemporaryInstance

class DamageNumber(TemporaryInstance):
    def __init__(self, pos, num, crit):
        super().__init__(pos)
        self.num = num
        self.crit = crit
        self.dur = crit * 50 + 30
    
    def update(self):
        super().update()