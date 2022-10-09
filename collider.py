import pygame
import ww

class Collider:
    CELL_SIZE = 50
    CELL_NUM = 100

    def __init__(self):
        self.debug = 0
        self.reset()

    def __call__(self, a: pygame.sprite.Sprite, b: pygame.sprite.Sprite):
        if a not in self.registered:
            self.register(a)
        if b not in self.registered:
            self.register(b)
        
        return (a, b) in self.collided


    def reset(self):
        self.debug = 0
        self.registered = set()
        self.collided = set()
        self.checked = set()
        self.grid = [[[] for _ in range(Collider.CELL_NUM)] for _ in range(Collider.CELL_NUM)]

    def register(self, sprite: pygame.sprite.Sprite):
        self.debug += 1
        self.registered.add(sprite)
        pos = pygame.math.Vector2(ww.view.target.pos)
        pos.x -= Collider.CELL_NUM / 2 * Collider.CELL_SIZE
        pos.y -= Collider.CELL_NUM / 2 * Collider.CELL_SIZE
        rect = sprite.rect.move(-pos)

        l = rect.left + rect.width * 0.1
        r = rect.left + rect.width * 0.9
        t = rect.top + rect.height * 0.6
        b = rect.bottom
        
        l = int(l // Collider.CELL_SIZE)
        r = int(r // Collider.CELL_SIZE)
        t = int(t // Collider.CELL_SIZE)
        b = int(b // Collider.CELL_SIZE)
        l = max(0, l)
        r = min(r, Collider.CELL_NUM - 1)
        t = max(0, t)
        b = min(b, Collider.CELL_NUM - 1)

        for i in range(l, r + 1):
            for j in range(t, b + 1):
                for e in self.grid[i][j]:
                    if self.collide(sprite, e):
                        self.collided.add((sprite, e))
                        self.collided.add((e, sprite))
                self.grid[i][j].append(sprite)

                hp_rect = sprite.rect
                clip_rect = hp_rect.clip(ww.view.rect)
                clip_rect.width = 10
                clip_rect.height = 10
                pygame.draw.rect(ww.screen, (128 * (l % 2), 128 * (t % 2), 0), clip_rect.move(-ww.view.rect.left, -ww.view.rect.top), 3)

    def collide(self, a: pygame.sprite.Sprite, b:pygame.sprite.Sprite):
        return a.rect.colliderect(b.rect)