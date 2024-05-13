# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 11:01:42 2023

@author: Zheng Wei
"""
import pygame
import math


class Raycaster():

  def __init__(self):
    self.max_distance = 6
    self.fov = 80
    self.res = 4
    self.mode='color wall'
    self.wall_height=13
    self.bri_eff=True
    self.dv=0

  def draw_texture_line(self,screen,sp,ep,texture,texture_x,brightness,tile_size):
    sx,sy=sp
    ex,ey=ep
    tw=texture.get_width()
    ratio=tw/tile_size
    tx=min(max(0,texture_x*ratio),tw-1)
    tsy=0
    th=texture.get_height()
    # shader
    # tsy=int(th/2-math.sqrt((tw/2)**2-(tx-tw/2)**2))
    # th=th-tsy*2
    # hwh=abs((sy-ey)/2)
    # hsh=screen.get_height()/2
    # sy=hsh-hwh*math.sqrt(1-(tx/tw*2-1)**2)
    # ey=hsh+hwh*math.sqrt(1-(tx/tw*2-1)**2)
    #
    line=texture.subsurface(tx,tsy,1,th)
    height=abs(sy-ey)
    strech_line=pygame.transform.scale(line,(self.res,height))
    if self.bri_eff:
      strech_line.set_colorkey((0,0,0))
      strech_line.set_alpha(brightness)
    screen.blit(strech_line,(sx,sy))

  def draw_color_line(self,screen,sp,ep,h_v,brightness):
    sx,sy=sp
    ex,ey=ep
    if h_v=='h':
      color=(0,brightness,0)
    else:
      color=(brightness,0,0)
    pygame.draw.line(screen, color, (sx,sy),(ex,ey), self.res)
    
  
  def draw_wall_line(self,screen, scr_x, distance, h_v,texture,texture_x,tile_size):
    scr_w,scr_h=screen.get_size()
    draw_distance = distance
    half_wall_height = self.wall_height*self.dv/draw_distance/2
    draw_start_y = scr_h / 2 - half_wall_height
    draw_end_y = scr_h / 2 + half_wall_height
    if self.bri_eff:
      brightness = max(0,min(255,255-distance*255/self.max_distance/tile_size))
    else:
      brightness = 255
    if self.mode=='color wall':
      self.draw_color_line(screen,(scr_x,draw_start_y),
                           (scr_x,draw_end_y),h_v,brightness)
    elif self.mode=='texture wall':
      self.draw_texture_line(screen, (scr_x, draw_start_y),(scr_x, draw_end_y),texture,texture_x,brightness,tile_size)

  def single_ray(self,map_screen,ray_screen,scr_x,v_ray_dir,player_dir,player_pos,map_size,tile_size,map_group):
    v_ray_start=player_pos
    mapx,mapy=int(v_ray_start.x),int(v_ray_start.y)
    v_unit_step=pygame.math.Vector2(
      math.sqrt(1+(v_ray_dir.y/v_ray_dir.x)*(v_ray_dir.y/v_ray_dir.x)) if v_ray_dir.x!=0 else 1,
      math.sqrt(1+(v_ray_dir.x/v_ray_dir.y)*(v_ray_dir.x/v_ray_dir.y)) if v_ray_dir.y!=0 else 1)
    v_ray_length=pygame.math.Vector2(0,0)
    if v_ray_dir.x<0:
      stepx=-1
      v_ray_length.x=(v_ray_start.x-mapx)*v_unit_step.x
    else:
      stepx=1
      v_ray_length.x=(mapx+1-v_ray_start.x)*v_unit_step.x
    if v_ray_dir.y<0:
      stepy=-1
      v_ray_length.y=(v_ray_start.y-mapy)*v_unit_step.y
    else:
      stepy=1
      v_ray_length.y=(mapy+1-v_ray_start.y)*v_unit_step.y
    hit = False
    travel_distance=0
    h_v='h'
    texture_x=0
    side=0
    while not hit and 0<=mapx<=map_size-1 and 0<=mapy<=map_size-1 and travel_distance<=self.max_distance:
      if v_ray_length.x<v_ray_length.y:
        mapx+=stepx
        travel_distance=v_ray_length.x
        v_ray_length.x+=v_unit_step.x
        side=0
      else:
        mapy+=stepy
        travel_distance=v_ray_length.y
        v_ray_length.y+=v_unit_step.y
        side=1
      if 0<=mapx<=map_size-1 and 0<=mapy<=map_size-1:
        tile=map_group.matrix[mapy][mapx]
        if tile.type=='wall':
          hit=True
    v_intersection=v_ray_start+v_ray_dir*travel_distance
    pygame.draw.line(map_screen, (255,255,0),v_ray_start*tile_size,v_intersection*tile_size,1)
    if hit:
      pygame.draw.circle(map_screen, (255, 0, 0), v_intersection*tile_size, 2)
      h_v='h' if side==0 else 'v'
      texture=tile.texture
      if side==0:
        if v_ray_dir.x>0:
          texture_x=(v_intersection.y-tile.pos.y)*tile_size
        else:
          texture_x=(1+tile.pos.y-v_intersection.y)*tile_size
      else:
        if v_ray_dir.y>0:
          texture_x=(1-v_intersection.x+tile.pos.x)*tile_size
        else:
          texture_x=(v_intersection.x-tile.pos.x)*tile_size
      distance=v_ray_length.x-v_unit_step.x if side==0 else v_ray_length.y-v_unit_step.y
      distance*=tile_size
      distance*=math.cos(-math.atan2(v_ray_dir.y,v_ray_dir.x)-math.atan2(player_dir.y,player_dir.x))
      self.draw_wall_line(ray_screen,scr_x,distance,h_v,texture,texture_x,tile_size)

  def raycast(self,map_screen,ray_screen,v_ray_dir,player_dir,player_pos,map_size,tile_size,map_group):
    map_scr_w,map_scr_h=map_screen.get_size()
    ray_scr_w,ray_scr_h=ray_screen.get_size()
    ray_scr_x=0
    ray_num=ray_scr_w//self.res
    self.dv=ray_scr_w/2/math.tan(math.radians(self.fov/2))
    v_ray_dir=pygame.math.Vector2(0,0)
    for i in range(ray_num):
      dir=math.atan2(player_dir.y,player_dir.x)+math.atan((ray_scr_w/2-ray_scr_x)/self.dv)
      v_ray_dir.x=math.cos(dir)
      v_ray_dir.y=math.sin(-dir)
      v_ray_dir=v_ray_dir.normalize()
      self.single_ray(map_screen,ray_screen,ray_scr_x,v_ray_dir,player_dir,player_pos,map_size,tile_size,map_group)
      ray_scr_x+=self.res