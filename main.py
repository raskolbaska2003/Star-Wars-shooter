import math
import random

import pygame.mouse

from Particles import Particles
from Bonus import Bonus
from Boss import Boss
from Player import Player, Bullet
from Values import *

run = True
# init player
player = Player(pygame.Rect(100, 100, player_size, player_size), (0, 255, 0), screen)


def main():
    global run, shoot_cd, boss_shoot_cd, bullets, boss_bullets, bonus, boss_cou, map_for_Bonus_objs, player

    # init image
    image = pygame.transform.scale(pygame.image.load('star_wars_2d_champ.png'), (50, 50))
    # void help
    help_image = pygame.transform.scale(pygame.image.load('help_to_shot.png'), (75, 75))
    invert_help_image = pygame.transform.flip(help_image, False, True)
    # get rect
    player_rect = image.get_rect()
    player_rect.center = player.position.center
    # get vector 0°
    x0, y0 = 100, 0
    # get enemy image
    enemy = pygame.image.load('death_star_2d.png')
    enemy = pygame.transform.scale(enemy, (200, 200))

    # init boss
    boss = Boss(pygame.Rect(random.randint(0, width-boss_size), random.randint(0, height-boss_size), boss_size, boss_size),
                hp=random.randint(10, 100),
                screen=screen)

    while run:

        # refresh
        if len(bonus) != 0: bonus_remove()
        refresh()
        clock.tick(60) #fps

        #get vector 1
        x1, y1 = pygame.mouse.get_pos()[0] - player_rect.center[0], -(pygame.mouse.get_pos()[1] - player_rect.center[1])

        # get event
        exit_check()

        # players movement
        player_movement(player)

        # rotate player
        player_rect.center = player.position.center
        try:
            angle = 57.29601 * math.acos(
                ((x0 * x1) + (y0 * y1)) / (math.sqrt(x0 ** 2 + y0 ** 2) * math.sqrt(x1 ** 2 + y1 ** 2)))
        except:
            pass
        if y1 < 0:
            x1 = -x1
            angle = 360 - angle


        # bonus place
        if len(map_for_Bonus_objs) != 0:
            obj = map_for_Bonus_objs[0]
            if check_is_in_circle(
                x1=obj.pos[0],
                y1=obj.pos[1],
                x2=player.position.center[0],
                y2=player.position.center[1],
                r=player_size
            ):
                bonus.append(obj.action())      # add bonus
                map_for_Bonus_objs.remove(obj)  # remove bonus from map
            else:
                pygame.draw.circle(screen, obj.color, (obj.pos[0], obj.pos[1]), 10) # draw bonus on map

        bullets = move_bullets(bullets)
        boss_bullets = move_bullets(boss_bullets)

        # draw player
        screen.blit(pygame.transform.rotate(image, angle), player_rect)

        #print particles
        for i in particles:
            i.move()
            if i.radius<=4:
                particles.remove(i)

        # replace boss
        if boss.hp <= 0:
            boss_cou += 1
            # generate bonus
            chance = random.randint(1, 5) # play with chance to generate bonus

            # generate particles
            for i in range(80):
                particles.append(Particles(circle=[screen, (random.choice((0,255)),random.choice((0,255)),random.choice((0,255))), list(boss.position.center), 6], speed=[random.randint(-10,10),random.randint(-10,10)]))

            # if the chance is 2 and there is no bonus on the map and no bonus in the list, generate bonus
            if chance == 2 and len(map_for_Bonus_objs) == 0 and len(bonus) == 0:
                bonus_generate()

            #generate boss position
            x, y = x_and_y_generate()

            # randomise new boss position
            # check if the boss is not too close to the player
            while (x - player.position.center[0] +50) ** 2 + (y - player.position.center[1] +50) ** 2 <= 300000:
                x, y = x_and_y_generate() #TODO
            # generate new boss
            boss = Boss(pygame.Rect(x, y, boss_size, boss_size),
                        hp=random.randint(10, 100), screen=screen)

        # boss shot
        if boss_shoot_cd < time.time():
            boss_bullets.append(boss.shot())

            boss_shoot_cd = time.time() + 1 / 10

        # check is boss shot player
        for i in boss_bullets:
            if check_is_in_circle(
                x1=player.position.center[0], 
                y1=player.position.center[1], 
                x2=i.end[0], 
                y2=i.end[1], 
                r=player_size / 2
            ):                
                # game over
                run = False


        
        # draw boss
        
        screen.blit(enemy, (boss.position.center[0] - boss_size / 2, boss.position.center[1] - boss_size / 2))
        # check if player is close to boss, if yes, draw boss hp in red, else draw in gray
        if      (
                boss.position.center[0] - player.position.center[0]) ** 2 + (
                boss.position.center[1] - player.position.center[1]) ** 2 < 300000:
            text = pygame.font.Font(None, 100) # set font size
            text = text.render(str(boss.hp), False, (255, 0, 0)) # set font color
            text_rect = text.get_rect() # get rect of text
            text_rect.center = boss.position.center # set rect center to boss center
            screen.blit(text, text_rect) # draw text on screen
            for i in bullets:
                # check if bullet is in boss circle, if yes, reduce boss hp and remove bullet
                if check_is_in_circle(
                    x1=boss.position.center[0], 
                    y1=boss.position.center[1], 
                    x2=i.end[0], 
                    y2=i.end[1], 
                    r=boss_size / 2
                ):
                    boss.hp -= player_damage
                    bullets.remove(i) 
        else:
            text = pygame.font.Font(None, 100)
            text = text.render(str(boss.hp), False, (200, 200, 200))
            text_rect = text.get_rect()
            text_rect.center = boss.position.center
            screen.blit(text, text_rect)



        # render time alive
        t_alive = pygame.font.Font(None, 30) # set font size
        t_alive = t_alive.render(f'time alive: {round(time.time() - time_alive, 2)}', False, (255, 0, 0)) # set font color
        t_alive_rect = t_alive.get_rect() # get rect of text
        t_alive_rect.center = (width // 2, t_alive_rect.bottom) # set rect center to time alive center
        screen.blit(t_alive, t_alive_rect) # draw text on screen

        # render boss cou
        txt = pygame.font.Font(None, 30)    # set font size
        txt = txt.render(f'Boss cou:{boss_cou}', False, (255, 0, 0))        # set font color
        txt_rect = txt.get_rect()
        txt_rect.center = (t_alive_rect.center[0], t_alive_rect.center[1] + t_alive_rect.bottom)    # set rect center to boss cou center
        screen.blit(txt, txt_rect) # draw text on screen

        # print_help_from_space
        if len(bonus) != 0:
            if bonus[0]['name'] == 'help_from_space' and bonus[0]['time'] > time.time():
                # print gun_1
                x_s, y_s = 10, 0 # get vector 0 grad
                x2, y2 = pygame.mouse.get_pos()[0] - help_image.get_width() // 2, -(pygame.mouse.get_pos()[1] - help_image.get_height() // 2) # get vector from gun to mouse

                print_help_to_shot(
                    image=help_image, 
                    x0=x_s, 
                    y0=y_s, 
                    x1=x2, 
                    y1=y2, 
                    pos=(0, 0), 
                    angle_plus=25
                )
                # print gun_2
                x2, y2 = pygame.mouse.get_pos()[0] - width + help_image.get_width() // 2, -(pygame.mouse.get_pos()[1]) + help_image.get_height() // 2 # get vector from gun to mouse
                print_help_to_shot(
                    image=invert_help_image, 
                    x0=x_s, 
                    y0=y_s, 
                    x1=x2, 
                    y1=y2, 
                    pos=(width - 100, 0), 
                    angle_plus=-25
                )
                # print gun_3

                x2, y2 = pygame.mouse.get_pos()[0] - width + help_image.get_width() // 2, -(pygame.mouse.get_pos()[1] - height + help_image.get_height() // 2) # get vector from gun to mouse
                print_help_to_shot(
                    image=invert_help_image, 
                    x0=x_s, 
                    y0=y_s, 
                    x1=x2, 
                    y1=y2, 
                    pos=(width - help_image.get_width(), height - help_image.get_height()), 
                    angle_plus=-30
                )

        pygame.display.flip()


def bonus_remove():
    global bonus, map_for_Bonus_objs
    if bonus[0]["time"] < time.time():
        bonus.remove(bonus[0])


def exit_check():
    global run, is_exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            is_exit = True


def check_is_in_circle(x1, y1, x2, y2, r):
    if (x2 - x1) ** 2 + (y2 - y1) ** 2 <= r * r:
        return True
    else:
        return False


def x_and_y_generate():
    return [random.randint(0, width-boss_size), random.randint(0, height-boss_size)]


def move_bullets(bullets_def):
    for i in bullets_def:
        if i.progress < i.speed_factor:
            i.fly()
        else:
            bullets_def.remove(i)
    return bullets_def


def print_help_to_shot(image, x0, y0, x1, y1, pos, angle_plus=0):
    global screen

    angle_1 = 57.29601 * math.acos(
        ((x0 * x1) + (y0 * y1)) / (math.sqrt(x0 ** 2 + y0 ** 2) * math.sqrt(x1 ** 2 + y1 ** 2)))
    if y1 < 0:
        x1 = -x1
        angle_1 = 360 - angle_1
    angle_1 += angle_plus
    screen.blit(pygame.transform.rotate(image, angle_1), pos)


def player_movement(player):
    global shoot_cd, bullets, grenade_cd
    key = pygame.key.get_pressed()
    if key[pygame.K_w] and player.position.center[1] > 10:
        player.move((0, -5))
    if key[pygame.K_a] and player.position.center[0] > 10:
        player.move((-5, 0))
    if key[pygame.K_s] and player.position.center[1] < height - 10:
        player.move((0, 5))
    if key[pygame.K_d] and player.position.center[0] < width - 10:
        player.move((5, 0))
    if key[pygame.K_SPACE]:
        player.position.center = pygame.mouse.get_pos()
    if key[pygame.K_g]:
        if grenade_cd < time.time():
            # generate bullets from the mouse position to the screen edges
            x, y = pygame.mouse.get_pos()
            bullets.append(Bullet((x, y), (0, 0), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width*0.25, 0), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width*0.5, 0), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width*0.75, 0), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width, 0), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width, height*0.25), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width, height*0.5), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width, height*0.75), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width, height), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width*0.25, height), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width*0.5, height), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width*0.75, height), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (width, height), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (0, height*0.25), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (0, height*0.5), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (0, height*0.75), (0, 255, 255), screen))
            bullets.append(Bullet((x, y), (0, height), (0, 255, 255), screen))
            grenade_cd = time.time() + 1 / 4
    if pygame.mouse.get_pressed()[0] and shoot_cd < time.time():
        try:
            bullets.append(player.shot())
            if len(bonus) != 0:
                if bonus[0]['name'] == 'triple_shot':
                    bullets.append(Bullet(player.position.center, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + 50), (0, 255, 255), screen, 15))
                    bullets.append(Bullet(player.position.center, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 50),(0, 255, 255), screen, 15))
        except Exception as e:
            pass
        fire_rate = 40 # amount of bullets per second
        shoot_cd = time.time() + 1 / fire_rate
        if len(bonus) != 0:
            if bonus[0]['name'] == 'help_from_space' and bonus[0]['time'] > time.time():
                # print bullet
                bullets.append(Bullet((37, 37), pygame.mouse.get_pos(), (0, 255, 0), screen, 20))
                bullets.append(Bullet((width - 37, 37), pygame.mouse.get_pos(), (0, 255, 0), screen, 20))
                bullets.append(Bullet((width - 37, height - 37), pygame.mouse.get_pos(), (0, 255, 0), screen, 20))


def refresh():
    screen.fill((0, 0, 0))


def bonus_generate():
    global map_for_Bonus_objs
    map_for_Bonus_objs.append(Bonus())


def game_over():
    global time_alive, boss_cou, screen
    screen.fill((0, 0, 0))
    # render game over
    t_game_over = pygame.font.Font(None, 100)
    t_game_over= t_game_over.render('Game Over', True, (255, 0, 0))
    t_game_over_rect = t_game_over.get_rect()
    t_game_over_rect.center = (width // 2, height // 2 - 100)
    screen.blit(t_game_over, t_game_over_rect)
    # render time alive
    t_alive = pygame.font.Font(None, 50)
    t_alive = t_alive.render(f'time alive: {round(time.time() - time_alive, 2)}', True, (255, 0, 0))
    t_alive_rect = t_alive.get_rect()
    t_alive_rect.center = (width // 2, height // 2)
    screen.blit(t_alive, t_alive_rect)
    # render boss count
    txt = pygame.font.Font(None, 50)
    txt = txt.render(f'Boss cou:{boss_cou}', True, (255, 0, 0))
    txt_rect = txt.get_rect()
    txt_rect.center = (width // 2, height // 2 + 50)
    screen.blit(txt, txt_rect)
    # render score
    txt = pygame.font.Font(None, 50)
    txt = txt.render(f'Score:{int((time.time() - time_alive) * boss_cou)}', True, (255, 0, 0))
    txt_rect = txt.get_rect()
    txt_rect.center = (width // 2, height // 2 + 100)
    screen.blit(txt, txt_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


if __name__ == '__main__':
    while is_exit != True:
        main()
        game_over()
        run = True
        #reset values
        particles = []
        bullets = []
        boss_bullets = []
        shoot_cd = time.time()
        grenade_cd = time.time()
        boss_shoot_cd = time.time()
        map_for_Bonus_objs = []
        boss_cou = 0
        time_alive = time.time()
    else:
        exit()
