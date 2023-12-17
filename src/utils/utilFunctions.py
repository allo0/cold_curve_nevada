import math
import time

import pygame

from configs import logConf
from configs.entitiesConf import MISC

logger = logConf.logger


class Utils:

    @staticmethod
    def calculate_experience_custom(level):
        # experience=round(base_experience×(0.5×level 2+0.5×log(level+1)))
        return round(MISC["base_exp"] * (0.5 * level ** 2 + 0.5 * math.log(level + 1)))

    @staticmethod
    def calculate_experience_quadratic(level, exp):  # for the Unalive difficulty or something for fun
        # experience=round(base_experience×level 2)
        return round(exp * (level ** 2))

    @staticmethod
    def get_curr_time():
        return pygame.time.get_ticks() / 1000
