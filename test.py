import math

import pygame
from Values import *
run=True
def main():
    global run
    image = pygame.image.load('help_to_shot.png')
    image  = pygame.transform.flip(pygame.transform.scale(image,(75,75)),False,True)

    player = image
    player_rect = player.get_rect()
    player_rect.center = (600,360)



    cou=0
    t_time = time.time()+1
    while run:
        clock.tick(60)
        cou+=1
        x0,y0 = 100,0
        x1,y1 = pygame.mouse.get_pos()[0]-player_rect.center[0] ,  -(pygame.mouse.get_pos()[1]-player_rect.center[1])


        for i in pygame.event.get():
            if i.type == 256:
                exit()
        screen.fill(0)
        pygame.draw.circle(screen, (0, 255, 0), (600, 360), 10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            player_rect = player_rect.move(0,10)
        if keys[pygame.K_a]:
            player_rect = player_rect.move(-10,0)
        if keys[pygame.K_w]:
            player_rect = player_rect.move(0,-10)
        if keys[pygame.K_d]:
            player_rect = player_rect.move(10,0)

        angle =  57.29601*math.acos(((x0*x1)+(y0*y1))/(math.sqrt(x0**2+y0**2)*math.sqrt(x1**2+y1**2)))

        if y1<0:
            x1=-x1
            angle=360-angle
        angle+=-25
        print(f'vector:({x1},{y1}), angle = {angle}')
        print(angle)
        player = pygame.transform.rotate(image, (angle))

        screen.blit(pygame.transform.rotate(image, angle),player_rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()