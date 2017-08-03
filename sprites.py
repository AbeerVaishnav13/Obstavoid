import pygame
from settings import *

Vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
	def __init__(self, game, image_string):
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.lives = 5
		self.image = pygame.image.load(image_string)
		self.image = pygame.transform.scale(self.image, PLAYER_SIZE)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, HEIGHT/2)
		self.pos = Vec(WIDTH/2, HEIGHT)
		self.vel = Vec(0, 0)
		self.acc = Vec(0, 0)


	def update(self):
		self.acc = Vec(0, 0)
		self.vel = (0, PLAYER_VEL_Y)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.acc.x = PLAYER_ACC_X
		if keys[pygame.K_LEFT]:
			self.acc.x = -PLAYER_ACC_X

		self.acc[0] += self.vel[0] * PLAYER_FRICTION

		self.vel += self.acc
		self.pos += self.vel + (self.acc/2)

		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH

		self.rect.midbottom = self.pos


class Obstacle(pygame.sprite.Sprite):
	"""docstring for Obstacle"""
	def __init__(self, x, y, w, h, image_string):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image_string)
		self.image = pygame.transform.scale(self.image, (int(w), int(h)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.active = True

	def de_activate(self):
		self.image.fill(RED)
		self.active = False

class Background(pygame.sprite.Sprite):
	"""docstring for Background"""
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("images/dungeon.png")
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
