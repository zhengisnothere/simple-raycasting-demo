# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 16:20:18 2023

@author: Zheng Wei
"""

import pygame


class Player():

  def __init__(self,x,y):
    self.image = pygame.Surface((4, 4))
    self.image.fill((255, 0, 0))
    self.dir = pygame.math.Vector2(1, -1)
    self.speed = 0.06
    self.rotate_speed=3
    self.pos=pygame.math.Vector2(x,y)

  def draw(self,screen,tile_size):
    screen.blit(self.image, self.pos*tile_size)
    self.draw_dir(screen,tile_size)

  def collison(self, map_group):
    pass

  def movement(self, map_size):
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
      self.pos.x += self.dir.x * self.speed
      self.pos.y -= self.dir.y * self.speed
    elif key[pygame.K_s]:
      self.pos.x += -self.dir.x * self.speed
      self.pos.y -= -self.dir.y * self.speed
    if key[pygame.K_d]:
      self.pos.x += self.dir.y * self.speed
      self.pos.y -= -self.dir.x * self.speed
    elif key[pygame.K_a]:
      self.pos.x += -self.dir.y * self.speed
      self.pos.y -= self.dir.x * self.speed
    self.pos.x = max(0, min(map_size, self.pos.x))
    self.pos.y = max(0, min(map_size, self.pos.y))

  def rotate(self):
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
      self.dir.rotate_ip(self.rotate_speed)
    elif key[pygame.K_RIGHT]:
      self.dir.rotate_ip(-self.rotate_speed)
      

  def draw_dir(self, screen,tile_size):
    front_x = self.pos.x*tile_size + self.dir.x * 20
    front_y = self.pos.y*tile_size - self.dir.y * 20
    pygame.draw.line(screen, (0, 0, 255), self.pos*tile_size,
                     (front_x, front_y))

  def update(self,map_size):
    self.rotate()
    self.movement(map_size)
