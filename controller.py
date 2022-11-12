import pygame

class Controller:
    def __init__(self):
        self._left = [pygame.K_a, pygame.K_LEFT]
        self._right = [pygame.K_d, pygame.K_RIGHT]
        self._up = [pygame.K_w, pygame.K_UP]
        self._down = [pygame.K_s, pygame.K_DOWN]
        self._keys = None
        self._mouses = None

    def update(self):
        self._keys = pygame.key.get_pressed()
        self._mouses = pygame.mouse.get_pressed()
    
    @property
    def left(self):
        for k in self._left:
            if self._keys[k]:
                return True
        return False

    @property
    def right(self):
        for k in self._right:
            if self._keys[k]:
                return True
        return False

    @property
    def up(self):
        for k in self._up:
            if self._keys[k]:
                return True
        return False

    @property
    def down(self):
        for k in self._down:
            if self._keys[k]:
                return True
        return False

    @property
    def horizontal(self):
        return self.right - self.left

    @property
    def vertical(self):
        return self.down - self.up

    @property
    def direction(self):
        dir = pygame.math.Vector2(self.horizontal, self.vertical)
        if dir:
            dir.normalize_ip()
        return dir

    @property
    def mouse_left_down(self):
        return self._mouses[0]