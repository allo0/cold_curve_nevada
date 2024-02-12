# class CameraGroup(pygame.sprite.Group):
#     def __init__(self):
#         super().__init__()
#         self.display_surface = pygame.display.get_surface()
#         self.offset = Vector2(-100, -100)
#
#     def custom_draw(self, players):
#         # # Calculate the average position of all players
#         # average_position = Vector2(0, 0)
#         # for player in players:
#         #     average_position += Vector2(player.rect.center)
#         #
#         # if players:
#         #     average_position /= len(players)
#         #
#         # # Update the offset based on the average position
#         # self.offset.x = average_position.x - Settings.SCREEN_WIDTH / 2
#         # self.offset.y = average_position.y - Settings.SCREEN_HEIGHT / 2
#
#         for sprite in self:
#             offset_rect = sprite.rect.copy()
#             offset_rect.center -= self.offset
#             self.display_surface.blit(sprite.image, offset_rect)

import pygame
from pygame.math import Vector2

from configs.appConf import Settings
from configs.entitiesConf import DUNGEON


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = Vector2()

    def custom_draw(self, player):
        # Center the camera on the player
        self.offset.x = player.rect.centerx - Settings.SCREEN_WIDTH
        self.offset.y = player.rect.centery - Settings.SCREEN_WIDTH

        # Clamp the offset to prevent showing areas outside the dungeon
        self.offset.x = max(0, min(self.offset.x, DUNGEON['width'] * DUNGEON["tile"] - Settings.SCREEN_WIDTH))
        self.offset.y = max(0, min(self.offset.y, DUNGEON['height'] * DUNGEON["tile"] - Settings.SCREEN_HEIGHT))

        # Draw the sprites in the group with the offset
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):  # Sort for drawing order
            offset_rect = sprite.rect.copy()
            offset_rect.topleft -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    def draw_static(self, static_sprites):
        # Draw static sprites without any offset
        for sprite in static_sprites:
            self.display_surface.blit(sprite.image, sprite.rect)
