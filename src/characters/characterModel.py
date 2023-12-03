import uuid

import pygame

from cold_curve_nevada.configs.entitiesConf import GENERIC_CONFIG

# Base class for all characters (NPC or not) for the game
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.image = pygame.Surface((32, 32))  # Example placeholder image
        self.image.fill((255, 0, 0))  # Red square
        self.rect = self.image.get_rect()
        # TODO change the movement system to Vector2D
        self.rect.center = (x, y)
        self.speed = GENERIC_CONFIG["speed"]
        self.health = GENERIC_CONFIG["health"]

    def update(self):
        # Generic method, to be implemented by the subclasses
        pass
