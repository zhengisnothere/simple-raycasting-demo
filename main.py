# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 16:19:58 2023

@author: Zheng Wei
"""
import pygame
import sys
import os

from raycaster_class_optimized import Raycaster
from player_class import Player
from grid_class import Grid_Map
import gui_class
import split_gif_to_frames

def load_gif():
  print('\nIf an error occurs, please rerun the file.')
  print('Running the file for the first time may take some time.')
  print('Loading...')
  if os.listdir('images/jinitaimei/') == []:
    split_gif_to_frames.extract_images('gif/jinitaimei_1.gif','images/jinitaimei/',12)
  if os.listdir('images/rickroll/') == []:
    split_gif_to_frames.extract_images('gif/rickroll.gif','images/rickroll/',12)
  print('Done.')

pygame.init()
load_gif()
tile_size = 20
map_size = 20
map_scr_w, map_scr_h = map_size * tile_size, map_size * tile_size
ray_scr_w, ray_scr_h = 400, 400
gui_scr_w,gui_scr_h=150,400
win_w, win_h = ray_scr_w+map_scr_w+gui_scr_w, max(ray_scr_h, map_scr_h)
map_screen = pygame.Surface((map_scr_w, map_scr_h))
ray_screen = pygame.Surface((ray_scr_w, ray_scr_h))
gui_screen = pygame.Surface((gui_scr_w, gui_scr_h))
window = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption('Raycaster')
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 15)

def clear_screens():
  window.fill((0,0,0))
  gui_screen.fill((255,255,255))
  map_screen.fill((0, 0, 0))
  ray_screen.fill((0, 0, 0))

def draw_text(screen, text, pos):
  text_image = font.render(text, 1, (0, 0, 0))
  screen.blit(text_image, pos)

def draw_gui():
  draw_text(gui_screen,str(round(clock.get_fps(),2)), (10, 5))
  show_setting_checkbox.draw(gui_screen)
  if show_setting_checkbox.value:
    res_slider.draw(gui_screen)
    fov_slider.draw(gui_screen)
    wall_h_slider.draw(gui_screen)
    render_dis_slider.draw(gui_screen)
    wall_texture_checkbox.draw(gui_screen)
    tile_texture_checkbox.draw(gui_screen)
    brightness_checkbox.draw(gui_screen)

def update_gui():
  show_setting_checkbox.check_mouse_click()
  if show_setting_checkbox.value:
    res_slider.check_mouse_drag()
    fov_slider.check_mouse_drag()
    wall_h_slider.check_mouse_drag()
    render_dis_slider.check_mouse_drag()
    wall_texture_checkbox.check_mouse_click()
    tile_texture_checkbox.check_mouse_click()
    brightness_checkbox.check_mouse_click()

def update_raycaster_setting():
  if show_setting_checkbox.value:
    raycaster.res=res_slider.value
    raycaster.fov=fov_slider.value
    raycaster.wall_height=wall_h_slider.value
    raycaster.max_distance=render_dis_slider.value
    raycaster.mode='texture wall' if wall_texture_checkbox.value else 'color wall'
    tile_group.draw_mode='texture' if tile_texture_checkbox.value else 'color'
    raycaster.bri_eff=brightness_checkbox.value

def draw_screens():
  window.blit(gui_screen,(0,0))
  window.blit(ray_screen, (gui_scr_w, 0))
  window.blit(map_screen, (gui_scr_w+ray_scr_w, 0))

tile_group = Grid_Map(tile_size,map_size)
raycaster = Raycaster()
player = Player(1.2,1.2)

show_setting_checkbox=gui_class.Check_box('Show Settings',10,30,90,30,13,True)
res_slider=gui_class.Slider('RES',10,80,120,20,15,4,1,20)
fov_slider=gui_class.Slider('FOV',10,130,120,20,15,66,30,120)
wall_h_slider=gui_class.Slider('Wall Height',10,180,120,20,13,19,10,30)
render_dis_slider=gui_class.Slider('Render Distance',10,230,120,20,11,8,1,30)
wall_texture_checkbox=gui_class.Check_box('Wall Texture',10,280,90,30,13,False)
tile_texture_checkbox=gui_class.Check_box('Tile Texture',10,320,90,30,14,False)
brightness_checkbox=gui_class.Check_box('Brightness Effect',10,360,90,30,10,True)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
  clear_screens()

  player.update(map_size)
  update_gui()
  update_raycaster_setting()

  draw_gui()
  tile_group.draw(map_screen,tile_size)
  raycaster.raycast(map_screen,ray_screen,player.dir,player.dir,player.pos,map_size,tile_size,tile_group)
  player.draw(map_screen,tile_size)

  draw_screens()
  
  pygame.display.flip()
  clock.tick(60)
