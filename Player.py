from pygame import mouse

from Bullet import Bullet


class Player:
    def __init__(self, pos, color, screen):
        self.position = pos  # Rect
        self.color = color  # list
        self.screen = screen

    def move(self, side: list,):
        self.position = self.position.move(side)

    def shot(self):  # -> Bullet

        return Bullet(self.position.center, mouse.get_pos(), (0, 255, 255), self.screen, 15)
