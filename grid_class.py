# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 19:21:02 2023

@author: Zheng Wei
"""

import random
import pygame
from math import floor
import os


image_names=['genshin','identity_v','jinitaimei','rickroll','john_carmack','minecraft_logo','soul_knight','pixel_wall','landscape','missing_texture']
image_sets=[]
for name in image_names:
  if name in ['jinitaimei','rickroll']:
    set=[]
    directory = os.listdir('images/'+name)
    sorted_dir = sorted(directory, key=lambda fn:int(fn.split('.')[0]))
    for file_name in sorted_dir:
      filepath = 'images/'+name+'/'+file_name
      set.append(pygame.image.load(filepath))
    image_sets.append(set)
  else:
    image_sets.append(pygame.image.load('images/'+name+'.png'))
    

class Grid_Map:

  def __init__(self, tile_size, map_size):
    self.create_map(tile_size, map_size)
    self.draw_mode='color'

  def create_map(self, tile_size, map_size):
    self.matrix=[]
    for y in range(map_size):
      row=[]
      for x in range(map_size):
        image_name=random.choice(image_names)
        if image_name in ['jinitaimei','rickroll']:
          image_type='video'
        else:
          image_type='image'
        image_set=image_sets[image_names.index(image_name)]
        if x==0 or y==0 or x==map_size-1 or y==map_size-1:
          row.append(Grid('wall',image_type,image_set,tile_size,x,y))
        else:
          wall_type=random.choice(['blank','blank','blank','wall','blank','blank','blank'])
          row.append(Grid(wall_type,image_type,image_set,tile_size,x,y))
      self.matrix.append(row)
  
  def draw(self, screen,tile_size):
    for row in self.matrix:
      for grid in row:
        grid.draw(screen,self.draw_mode,tile_size)

class Grid():

  def __init__(self, type,image_type,image_set, size, index_x, index_y):
    self.index_x = index_x
    self.index_y = index_y
    self.type = type
    self.image_type = image_type
    if type == 'wall':
      self.load_image(image_type,image_set,size)
    else:
      self.image = pygame.Surface((size, size), pygame.SRCALPHA, 32)
      self.color_tile=pygame.Surface((size,size),pygame.SRCALPHA, 32)
    self.pos=pygame.math.Vector2(index_x,index_y)

  def load_image(self,image_type,image_set,size):
    self.color_tile=pygame.Surface((size,size))
    self.color_tile.fill((200,200,200))
    if image_type=='image':
      self.texture=image_set
      self.image = pygame.transform.scale(self.texture, (size, size))
    elif image_type=='video':
      self.animation_index=0
      self.animation_set=image_set
      self.animation_speed=0.25
      self.map_image_set=[pygame.transform.scale(i,(size,size)) for i in self.animation_set]
      self.texture=self.animation_set[self.animation_index]
      self.image=self.map_image_set[self.animation_index]

  def animate(self):
    self.animation_index+=self.animation_speed
    if self.animation_index>=len(self.animation_set):
      self.animation_index=0
    self.texture=self.animation_set[floor(self.animation_index)]
    self.image=self.map_image_set[floor(self.animation_index)]
  
  def draw(self, screen,draw_mode,tile_size):
    if self.type=='wall' and self.image_type=='video':
      self.animate()
    if draw_mode=='color':
      screen.blit(self.color_tile,self.pos*tile_size)
    else:
      screen.blit(self.image, self.pos*tile_size)
