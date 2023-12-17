import math

import pygame

from configs import logConf
from configs.entitiesConf import PLAYER_CONFIG

logger = logConf.logger


class AoE_Zone(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self._radius = PLAYER_CONFIG["aoe_radius"]
        self._damage = PLAYER_CONFIG["aoe_damage"]
        self._attack_speed = PLAYER_CONFIG["aoe_attack_speed"]
        self.image = pygame.Surface((2 * self._radius, 2 * self._radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255, 32),
                           (self._radius, self._radius),
                           self._radius)
        self.rect = self.image.get_rect(center=player_rect.center)
        self._last_attack_time = 0  # Track the time of the last attack

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

    @property
    def last_attack_time(self):
        return self._last_attack_time

    @last_attack_time.setter
    def last_attack_time(self, value):
        self._last_attack_time = value

    @property
    def attack_speed(self):
        return self._attack_speed

    @attack_speed.setter
    def attack_speed(self, value):
        self._attack_speed = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self._update_image()

    def _update_image(self):
        self.image = pygame.Surface((2 * self._radius, 2 * self._radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255, 32),
                           (self._radius, self._radius),
                           self._radius)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, player_rect):
        self.rect.center = player_rect.center

    def can_attack(self, current_time):
        # Check if enough time has passed since the last attack
        time_since_last_attack = current_time - self.last_attack_time
        attack_interval = 1 / self.attack_speed  # In seconds
        return time_since_last_attack >= attack_interval


class RotatingLine(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        super().__init__()
        self.angle = 0
        self.line_radius = 500  # Adjust as needed
        self.image = pygame.Surface((2 * self.line_radius, 2), pygame.SRCALPHA)
        pygame.draw.line(self.image, (255, 255, 255, 255), player_rect.center, (500, 500), 2)

        self.rect = self.image.get_rect(center=player_rect.center)

    def update(self, player_rect):
        # Clear the image to redraw the lines
        self.image.fill((0, 0, 0, 0))  # Use a small alpha value for transparency

        for radius in range(10, 200 + 1, 10):
            # Calculate the position of the rotating tracer line
            tracer_length = radius - 5  # Adjust as needed
            tracer_angle = self.angle
            tracer_x = player_rect.center[0] + tracer_length * math.cos(tracer_angle)
            tracer_y = player_rect.center[1] + tracer_length * math.sin(tracer_angle)

            # Draw the rotating tracer line
            pygame.draw.line(self.image, (255, 255, 255, 255), player_rect.center, (tracer_x, tracer_y), 2)

        # Update the rect attribute of the Sprite class
        self.rect.center = player_rect.center
        self.angle += 0.02  # Adjust the rotation speed as needed
