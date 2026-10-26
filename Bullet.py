import math

from pygame import draw


class Bullet:
    def __init__(self, start_pos, end_pos, color, screen, speed_factor=100):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.progress = 1
        self.x = end_pos[0] - start_pos[0]
        self.y = end_pos[1] - start_pos[1]
        self.vec = self.x * math.sqrt(900 / ((self.x * self.x) + (self.y * self.y))), self.y * math.sqrt(
            900 / ((self.x * self.x) + (self.y * self.y)))
        self.speed_factor = speed_factor
        self.color = color
        self.screen = screen
        self.st = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) / self.speed_factor * self.progress, \
                  self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) / self.speed_factor * self.progress
        self.end = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) / self.speed_factor * (self.progress + 1), \
                   self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) / self.speed_factor * (self.progress + 1)

    def fly(self):
        self.st = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) / self.speed_factor * self.progress, \
                  self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) / self.speed_factor * self.progress
        self.end = self.st[0] + self.vec[0], self.st[1] + self.vec[1]

        self.progress += 1
        draw.line(self.screen, self.color, self.st, self.end, 7)
