import uuid

import pygame

from cold_curve_nevada.configs import logConf
from cold_curve_nevada.configs.entitiesConf import GENERIC_CONFIG

logger = logConf.logger


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.__id = str(uuid.uuid4())[-12:]
        self.image = pygame.Surface((32, 32))  # Example placeholder image
        self.image.fill((255, 0, 0))  # Red square
        self.rect = self.image.get_rect()
        # TODO change the movement system to Vector2D
        self.rect.center = (x, y)
        self.__speed = GENERIC_CONFIG["speed"]
        self.__health = GENERIC_CONFIG["health"]
        self.__iframes = 0  # Number of iframes after being hit (0 means not invulnerable)
        self.__invincible = False  # Flag to track if the player is currently invincible
        # Cooldown for hit
        self.__hit_cooldown = 0  # Initialize the cooldown timer
        self.__hit_cooldown_duration = GENERIC_CONFIG["iframes"]  # Adjust this value as needed (in frames)

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        self.__speed = value

    @property
    def hit_cooldown(self):
        return self.__hit_cooldown

    @hit_cooldown.setter
    def hit_cooldown(self, value):
        self.__hit_cooldown = value

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        self.__health = value

    @property
    def hit_cooldown_duration(self):
        return self.__hit_cooldown_duration

    @hit_cooldown_duration.setter
    def hit_cooldown_duration(self, value):
        self.__hit_cooldown_duration = value

    @property
    def iframes(self):
        return self.__iframes

    @iframes.setter
    def iframes(self, value):
        self.__iframes = value

    @property
    def invincible(self):
        return self.__invincible

    @invincible.setter
    def invincible(self, value):
        self.__invincible = value

    def update(self):
        # Generic method, to be implemented by the subclasses
        if self.iframes > 0:
            self.iframes -= 1
            self.image.set_alpha(128)  # Make the player semi-transparent during iframes
        else:
            self.image.set_alpha(255)  # Reset transparency
            self.end_iframes()  # Call end_iframes when iframes are over

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

    def end_iframes(self):
        # Called when iframes are over
        self.invincible = False

    def hit(self):
        # Handle iframes only
        if not self.invincible:
            self.iframes = GENERIC_CONFIG["iframes"]
            self.invincible = True
            # Set the cooldown to prevent repeated hits
            self.hit_cooldown = self.hit_cooldown_duration

    def take_damage(self, damage):
        if not self.invincible and self.hit_cooldown == 0 and self.health > 0:
            self.health -= damage
            self.hit()
            logger.info(f"{self.id} current HP: {self.health}")
            return self.health
        else:
            return self.health
