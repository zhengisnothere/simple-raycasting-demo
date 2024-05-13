# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 20:16:31 2023

@author: Zheng Wei
"""

import pygame


class GUI:
  def __init__(self, x, y, width, height, color,font_size):
    self.color=color
    self.width=width
    self.height=height
    self.create_image(width,height,color)
    self.set_text('',font_size,(0,0,0))
    self.rect=self.image.get_rect()
    self.rect.topleft=(x,y)

  def create_image(self,width, height, color):
    self.image=pygame.Surface((width,height))
    self.image.fill(color)
    self.touched_image=pygame.Surface((width,height))
  
  def set_text(self,text,font_size,color):
    self.text=text
    self.font_size=font_size
    font=pygame.font.SysFont('arial',font_size)
    self.font_color=color
    self.text_image=font.render(text,1,color)

  def draw(self,screen):
    screen.blit(self.image,self.rect)
    tx=self.rect.x+self.width/2-self.text_image.get_width()/2
    ty=self.rect.y+self.height/2-self.text_image.get_height()/2
    screen.blit(self.text_image,(tx,ty))
    

class Slider(GUI):
  def __init__(self,name, x, y, width, height,font_size,value,min_v,max_v):
    super().__init__(x, y, width, height, (200,200,200), font_size)
    self.min_v,self.max_v=min_v,max_v
    self.value=value
    self.value_length=max_v-min_v
    self.create_slider(min_v,max_v)
    self.name=name

  def create_slider(self,min_v,max_v):
    self.slider_bg=pygame.Surface((self.width,20))
    self.slider_bg.fill(self.color)
    pygame.draw.line(self.slider_bg,(0,0,0),(self.width*0.1,self.height//2),(self.width*0.9,self.height//2),1)
    self.slider_bg_rect=self.slider_bg.get_rect(topleft=(self.rect.x,self.rect.y+self.height))
    self.slider_point=pygame.Surface((8,8))
    self.slider_point.fill((255,0,0))
    self.slider_point_rect=self.slider_point.get_rect()
    self.slider_point_rect.centerx=self.rect.x+self.width*0.1+(self.value-self.min_v-0.5)*self.width*0.8/self.value_length
    self.slider_point_rect.centery=self.rect.y+self.height+10

  def locate_slider_point(self,mx):
    self.slider_point_rect.centerx=min(self.rect.x+self.width*0.9,max(self.rect.x+self.width*0.1,mx))
    self.slider_point_rect.centery=self.rect.y+self.height+10
    self.value=int((self.slider_point_rect.centerx-self.rect.x-self.width*0.1)/(self.width*0.8/self.value_length)+0.5)+self.min_v
  
  def draw(self,screen):
    self.set_text(f'{self.name}: {self.value}',self.font_size,(0,0,0))
    super().draw(screen)
    screen.blit(self.slider_bg,self.slider_bg_rect)
    screen.blit(self.slider_point,self.slider_point_rect)

  def check_mouse_drag(self):
    mx,my=pygame.mouse.get_pos()
    if self.slider_point_rect.collidepoint((mx,my)):
      if pygame.mouse.get_pressed()[0]:
        self.locate_slider_point(mx)

class Check_box(GUI):
  def __init__(self,name, x, y, width, height, font_size,value):
    super().__init__(x, y, width, height, (200,200,200), font_size)
    self.name=name
    self.value=value
    self.create_check_box()
    self.last_tick_clicked=False

  def create_check_box(self):
    self.cb_bg=pygame.Surface((self.height,self.height))
    self.cb_bg.fill(self.color)
    self.cb_bg_rect=self.cb_bg.get_rect(topleft=(self.rect.x+self.width,self.rect.y))
    self.unchecked_box=pygame.Surface((20,20),pygame.SRCALPHA,32)
    pygame.draw.rect(self.unchecked_box,(0,0,0),(0,0,18,18),2)
    self.checked_box=pygame.Surface((20,20),pygame.SRCALPHA,32)
    pygame.draw.rect(self.checked_box,(0,0,0),(0,0,18,18),2)
    pygame.draw.lines(self.checked_box,(255,0,0),False,[(4,10),(6,14),(14,4)],3)
    self.check_box_rect=self.unchecked_box.get_rect()
    self.check_box_rect.center=self.cb_bg_rect.center
  
  def draw(self,screen):
    self.set_text(self.name,self.font_size,(0,0,0))
    super().draw(screen)
    screen.blit(self.cb_bg,self.cb_bg_rect)
    if self.value:
      screen.blit(self.checked_box,self.check_box_rect)
    else:
      screen.blit(self.unchecked_box,self.check_box_rect)

  def check_mouse_click(self):
    mx,my=pygame.mouse.get_pos()
    if self.check_box_rect.collidepoint((mx,my)):
      if pygame.mouse.get_pressed()[0]:
        if not self.last_tick_clicked:
          self.value=not self.value
          self.last_tick_clicked=True
      else:
        self.last_tick_clicked=False