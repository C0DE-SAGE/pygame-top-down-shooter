import pygame, sys
from random import randint
from math import atan2, degrees, pi

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Tree(pygame.sprite.Sprite):
	def __init__(self, pos):
		super().__init__()
		self.image = pygame.image.load('test/graphics/tree.png').convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.speed = 1

	def update(self):
		direction = pygame.math.Vector2(self.rect.center) - player.rect.center
		direction = direction.normalize()
		self.rect.center += direction * self.speed
		if pygame.sprite.spritecollide(self, pygame.sprite.GroupSingle(player), False, pygame.sprite.collide_mask):
			self.kill()


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, health):
		super().__init__()
		self.health = health
		self.image = pygame.image.load('test/graphics/pixil-frame-0.png').convert_alpha()
		self.rect = self.image.get_rect(center=pos)
		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.attack_time = 0
		self.attack_delay = 5

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_w]:
			self.direction.y = -1
		elif keys[pygame.K_s]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_d]:
			self.direction.x = 1
		elif keys[pygame.K_a]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		if pygame.mouse.get_pressed()[0] and self.attack_time == 0:
			group.add(Bullet(self.rect, view.rect.topleft, 20))
			self.attack_time = self.attack_delay

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed
		self.attack_time = max(self.attack_time - 1, 0)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, player_pos, camera_pos, duration_limit):
		super().__init__()
		self.duration_limit = duration_limit
		self.dura = 0
		self.pos = pygame.math.Vector2(player_pos.center)
		self.image = pygame.image.load('test/graphics/bullet.png').convert_alpha()
		self.rect = self.image.get_rect(center=self.pos)

		dx = pygame.math.Vector2(pygame.mouse.get_pos())[0] - player_pos.center[0]
		dy = pygame.math.Vector2(pygame.mouse.get_pos())[1] - player_pos.center[1]
		rads = atan2(-dy, dx)
		rads %= 2 * pi
		degs = degrees(rads)

		self.image = pygame.transform.rotate(self.image, degs)

		self.speed = 15
		self.vel = pygame.math.Vector2(pygame.mouse.get_pos()) + camera_pos - player_pos.center
		# self.vel += camera_pos - player_pos.center
		self.vel = self.vel.normalize() * self.speed

	def update(self):
		self.pos += self.vel
		self.rect.center = self.pos
		self.mask = pygame.mask.from_surface(self.image)
		self.player_mask = pygame.mask.from_surface(player.image)
		if self.dura <= self.duration_limit:
			self.dura += 1
		else:
			self.kill()

		if pygame.sprite.spritecollide(self, tree_group, True, pygame.sprite.collide_mask):
			self.kill()


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
		# ??????/????????? ????????? ??????. ??????.
		# global screen
		# screen.fill('#71ddee')
		# clip_rect = self.bg_rect.clip(self.rect)
		# screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
		# inside_rect = clip_rect.move(-self.bg_rect.left, -self.bg_rect.top)
		# screen.blit(self.bg, screen_rect, inside_rect)

		# for sprite in sorted(group.sprites(), key=lambda sprite: sprite.rect.bottom):
		#	 clip_rect = sprite.rect.clip(self.rect)
		#	 screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
		#	 inside_rect = clip_rect.move(-sprite.rect.left, -sprite.rect.top)
		#	 screen.blit(sprite.image, screen_rect, inside_rect)

		# ??????/????????? ???????????? ??????. ?????? ??????.
		global screen
		surf = pygame.Surface(self.rect.size)
		surf.fill('#71ddee')
		clip_rect = self.bg_rect.clip(self.rect)
		screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
		inside_rect = clip_rect.move(-self.bg_rect.left, -self.bg_rect.top)
		surf.blit(self.bg, screen_rect, inside_rect)

		for sprite in sorted(group.sprites(), key=lambda sprite: sprite.rect.bottom):
			clip_rect = sprite.rect.clip(self.rect)
			screen_rect = clip_rect.move(-self.rect.left, -self.rect.top)
			inside_rect = clip_rect.move(-sprite.rect.left, -sprite.rect.top)
			surf.blit(sprite.image, screen_rect, inside_rect)
			pygame.transform.scale(surf, (SCREEN_WIDTH, SCREEN_HEIGHT), screen)


class FPS:
	def __init__(self):
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("Verdana", 20)
		self.text = self.font.render(str(self.clock.get_fps()), True, (0, 0, 0))

	def render(self, display):
		self.text = self.font.render(str(round(self.clock.get_fps(), 2)), True, (0, 0, 0))
		display.blit(self.text, (10, 10))


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
fps = FPS()

group = pygame.sprite.Group()
player = Player((640, 360), 120)
player_group = pygame.sprite.GroupSingle(player)
group.add(player_group)

view = View(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), player)

# for i in range(20):
# 	random_x = randint(0,1000)
# 	random_y = randint(0,1000)
# 	group.add(Tree((random_x, random_y)))

# tree_group = pygame.sprite.Group()
# group.add(tree_group)

tree_group = pygame.sprite.Group()

for i in range(20):
	random_x = randint(0, 1000)
	random_y = randint(0, 1000)
	tree_group.add(Tree((random_x, random_y)))

group.add(tree_group)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
		if event.type == pygame.MOUSEWHEEL:
			view.sight_scale += event.y * 0.03

	view.step()
	view.draw(group)
	group.update()
	fps.render(screen)
	pygame.display.update((0, 0, 1280, 720))
	fps.clock.tick(60)