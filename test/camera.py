import pygame, sys
from random import randint

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Tree(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load('test/graphics/tree.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)


class Player(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load('test/graphics/pixil-frame-0.png').convert_alpha()
		self.rect = self.image.get_rect(center=pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP]:
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed

	def create_bullet(self, camera_pos):
		return Bullet(self.rect, camera_pos)
    		

class Bullet(pygame.sprite.Sprite):
	def __init__(self, player_pos, camera_pos):
		super().__init__()
		self.image = pygame.Surface((10, 10))
		self.image.fill((255, 0, 0))
		self.pos = pygame.math.Vector2(player_pos.center)
		self.rect = self.image.get_rect(center=self.pos)

		self.speed = 15
		self.vel = pygame.math.Vector2(pygame.mouse.get_pos()) + camera_pos - player_pos.center
		# self.vel += camera_pos - player_pos.center
		self.vel = self.vel.normalize() * self.speed
		
	def update(self):
		self.pos += self.vel
		self.rect.center = self.pos
		

class View:
	def __init__(self, rect, target=None):
		self.rect = rect
		self.target = target
		self.bg = pygame.image.load('test/graphics/ground.png').convert_alpha()
		self.bg_rect = self.bg.get_rect(topleft=(0, 0))
		self.sight_scale = 1

	def step(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_q]:
			self.sight_scale += 0.01
		if keys[pygame.K_e] and self.sight_scale > 0.2:
			self.sight_scale -= 0.01
		self.rect.width = SCREEN_WIDTH * self.sight_scale
		self.rect.height = SCREEN_HEIGHT * self.sight_scale

		if self.target:
			self.rect.center = self.target.rect.center

	def draw(self, group):
		# 확대/축소를 제거한 코드. 빠름.
		global screen
		screen.fill('#71ddee')
		clip_rect = self.bg_rect.clip(self.rect)
		screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
		inside_rect = clip_rect.move(-self.bg_rect.left, -self.bg_rect.top)
		screen.blit(self.bg, screen_rect, inside_rect)

		for sprite in sorted(group.sprites(), key=lambda sprite: sprite.rect.bottom):
			clip_rect = sprite.rect.clip(self.rect)
			screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
			inside_rect = clip_rect.move(-sprite.rect.left, -sprite.rect.top)
			screen.blit(sprite.image, screen_rect, inside_rect)

		# 확대/축소를 지원하는 코드. 다소 느림.
		# global screen
		# surf = pygame.Surface(self.rect.size)
		# surf.fill('#71ddee')
		# clip_rect = self.bg_rect.clip(self.rect)
		# screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
		# inside_rect = clip_rect.move(-self.bg_rect.left, -self.bg_rect.top)
		# surf.blit(self.bg, screen_rect, inside_rect)

		# for sprite in sorted(group.sprites(), key=lambda sprite: sprite.rect.bottom):
		# 	clip_rect = sprite.rect.clip(self.rect)
		# 	screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
		# 	inside_rect = clip_rect.move(-sprite.rect.left, -sprite.rect.top)
		# 	surf.blit(sprite.image, screen_rect, inside_rect)
		# 	pygame.transform.scale(surf, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)


class FPS:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Verdana", 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, (0, 0, 0))
 
    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, (0, 0, 0))
        display.blit(self.text, (10, 10))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
fps = FPS()

group = pygame.sprite.Group()
player = Player((640,360))
group.add(player)

view = View(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), player)

for i in range(20):
	random_x = randint(0,1000)
	random_y = randint(0,1000)
	group.add(Tree((random_x, random_y)))

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN:
			group.add(player.create_bullet(view.rect.topleft))
		if event.type == pygame.MOUSEWHEEL:
			view.sight_scale += event.y * 0.03

	view.step()
	view.draw(group)
	group.update()
	fps.render(screen)
	pygame.display.update()
	fps.clock.tick(60)
