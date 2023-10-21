import pygame
from configs.appConf import Settings
from pygame.math import Vector2


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.diplay_surface = pygame.display.get_surface()
        self.offset = Vector2(200, 200)

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - Settings.SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - Settings.SCREEN_HEIGHT / 2
        for sprite in self:
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.diplay_surface.blit(sprite.image, offset_rect)
