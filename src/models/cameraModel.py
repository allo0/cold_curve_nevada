import pygame
from pygame.math import Vector2

from cold_curve_nevada.configs.appConf import Settings


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector2(200, 200)

    def custom_draw(self, players):
        # Calculate the average position of all players
        average_position = Vector2(0, 0)
        for player in players:
            average_position += Vector2(player.rect.center)

        if players:
            average_position /= len(players)

        # Update the offset based on the average position
        self.offset.x = average_position.x - Settings.SCREEN_WIDTH / 2
        self.offset.y = average_position.y - Settings.SCREEN_HEIGHT / 2

        for sprite in self:
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)