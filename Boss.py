from Bullet import Bullet
from random import randint, choice
from Values import height,width

class Boss:
    def __init__(self, position, hp, screen):
        self.position  = position
        self.hp = hp
        self.screen = screen

    def shot(self):
        x=[]
        ch = choice(('left','top','bottom','right'))
        if ch == 'left':
            x = [0,randint(0,height)]
        elif ch == 'top':
            x = [randint(0,width),0]
        elif ch == 'bottom':
            x = [randint(0,width),height]
        elif ch == 'right':
            x = [width,randint(0,height)]
        return Bullet(self.position.center, x, (255, 0, 0), self.screen,100)