import time

import pygame


pygame.init()

is_exit=False
player_damage=1
player_size=25
boss_size = 200
particles=[]

size = width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Star Wars')
pygame.display.set_icon(pygame.transform.rotate(pygame.image.load('star_wars_2d_champ.png'), 90))
clock = pygame.time.Clock()
bullets = []
boss_bullets = []
shoot_cd = time.time()
grenade_cd=time.time()
boss_shoot_cd = time.time()
bonus = [{'name': 'help_from_space', 'time': time.time() + 5}]
map_for_Bonus_objs = []
boss_cou = 0
time_alive = time.time()
