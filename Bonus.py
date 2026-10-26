import random
import time
from Values import width, height


class Bonus:
    def __init__(self, ):
        self.radius = 10

        def x_and_y_generate():
            return [random.randint(self.radius, width-self.radius), random.randint(self.radius, height-self.radius)]

        self.pos = x_and_y_generate()
        self.name = random.choice(('help_from_space', 'triple_shot'))
        color_choice = {
            'help_from_space': (0, 0, 255),
            'triple_shot':(0,255,255)
        }
        self.color = color_choice[self.name]

    def action(self):  # -> dict
        ret_dict = {}
        ret_dict['time'] = time.time() + 20
        ret_dict['name'] = self.name
        return ret_dict

