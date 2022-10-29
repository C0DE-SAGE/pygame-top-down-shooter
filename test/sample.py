from dis import dis
from turtle import speed
import pygame
import sys
import math
import random

pygame.init()

display = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()

class Player:
	'''
	player setting
	'''
	def __init__(self, x, y, width, height, health):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.health = health
	def main(self, display):
		pygame.draw.rect(display, (255,0,0), (self.x, self.y, self.width, self.height))



class Enemy:
	'''
	Enemy setting
	'''
	def __init__(self, x, y, width, height, health):
		self.x = x
		self.y = y
		self.speed = 2
		self.width = width
		self.height = height
		self.health = health
	def main(self, display, player):
		pygame.draw.rect(display, (0,0,255), (display_scroll[0], display_scroll[1], self.width, self.height))



class PlayerBullet:
	'''
	Player bullet(attack)
	'''
	def __init__(self, x, y, mouse_x, mouse_y):
		self.x = x
		self.y = y
		self.mouse_x = mouse_x
		self.mouse_y = mouse_y
		self.speed = 15
		self.angle = math.atan2(y-mouse_y, x-mouse_x)
		self.x_vel = self.speed * math.cos(self.angle)
		self.y_vel = self.speed * math.sin(self.angle)
	def main(self, display):
		self.x -= int(self.x_vel)
		self.y -= int(self.y_vel)

		pygame.draw.circle(display, (0,0,0), (self.x, self.y), 5)


class ParticlePrinciple:
	def __init__(self):
		self.particles = []		# 파티클 배열 만듦

	def emit(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:					#particle안에 있는 객체들 direction쪽으로 pos 이동, 원 크기 -10씩
				particle[0][1] += particle[2][0]
				particle[0][0] += particle[2][1]
				particle[1] -= 0.2
				pygame.draw.circle(display,pygame.Color('White'), particle[0], int(particle[1]))

	def add_particles(self):
		pos_x = pygame.mouse.get_pos()[0]	# 마우스 x위치 반환
		pos_y = pygame.mouse.get_pos()[1]	# 마우스 y위치 변환
		radius = 10							# circle일 때 원 지름
		direction_x = random.randint(-3,3)	# -3~3사이 랜덤한 방향(x)
		direction_y = random.randint(-3,3)	# -3~3사이 랜덤한 방향(y)
		particle_circle = [[pos_x,pos_y],radius,[direction_x,direction_y]]
		self.particles.append(particle_circle)		#append

	def delete_particles(self):
		particle_copy = [particle for particle in self.particles if particle[1] > 0]	#파티클의 원사이즈가 0보다 작으면 삭제
		self.particles = particle_copy




player = Player(400,300,32,32,120)	  #x,y,width, height, health

enemy = Enemy(400,30,32,32,10)

display_scroll = [0,0]

player_bullets = []

while True: 
	display.fill((24,186,32))
	
	pygame.draw.rect(display, (255,0,0),(10,10, 250,5))
	pygame.draw.rect(display, (0,255,0),(10,10, player.health,5))

	mouse_x, mouse_y = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			pygame.QUIT
		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				player_bullets.append(PlayerBullet((player.x*2+player.width)/2, (player.y*2+player.height)/2, mouse_x, mouse_y))

	keys = pygame.key.get_pressed()

	pygame.draw.rect(display, (255,255,255),(100-display_scroll[0],100-display_scroll[1],16,16))

	if keys[pygame.K_a]:
		display_scroll[0] -= 5

		for bullet in player_bullets:
			bullet.x += 5
	if keys[pygame.K_d]:
		display_scroll[0] += 5

		for bullet in player_bullets:
			bullet.x -= 5
	if keys[pygame.K_w]:
		display_scroll[1] -= 5

		for bullet in player_bullets:
			bullet.y += 5
	if keys[pygame.K_s]:
		display_scroll[1] += 5

		for bullet in player_bullets:
			bullet.y -= 5

	player.main(display)
	enemy.main(display,player)

	for bullet in player_bullets:
		bullet.main(display)

	clock.tick(60)
	pygame.display.update()