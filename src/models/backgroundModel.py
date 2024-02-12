import random

import pygame

from configs.assetsConf import TERRAIN
from configs.entitiesConf import DUNGEON


class BackgroundGenerator:
    def __init__(self, width, height, tile_size=DUNGEON["tile"]):
        pygame.init()
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.wall_sprite = pygame.image.load(TERRAIN["wall"])
        self.floor_sprite = pygame.image.load(TERRAIN["floor"])
        self.dungeon = [['W' for _ in range(width)] for _ in range(height)]
        self.wall_rects = []
        self.rect = self.wall_sprite.get_rect()
        self.mask = pygame.mask.from_surface(self.wall_sprite)


    def count_walls_nearby(self, x, y):
        # Counts the number of walls surrounding a given tile (x, y)
        return sum(
            self.dungeon[ny][nx] == 'W'
            for nx in range(x - 1, x + 2)
            for ny in range(y - 1, y + 2)
            if (nx, ny) != (x, y)
        )

    def generate_dungeon(self, player_tile_size=4):
        # Randomly fill the interior with walls ('W') and floors ('.')
        # Skipping the border tiles
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.dungeon[y][x] = 'W' if random.random() < 0.5 else '.'

        # Smooth out the dungeon to create corridors and open spaces
        new_dungeon = [['W' for _ in range(self.width)] for _ in range(self.height)]
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                wall_count = self.count_walls_nearby(x, y)
                new_dungeon[y][x] = 'W' if wall_count >= 7 else '.'
                if wall_count >= 7:
                    # Create a rectangle for each wall for collision detection
                    wall_rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    self.wall_rects.append(wall_rect)
        self.dungeon = new_dungeon

        # Find a clear starting point for the player within the dungeon
        for _ in range(30000):  # Limit attempts to prevent infinite loops
            player_x, player_y = random.randint(1, self.width - 2 - player_tile_size), random.randint(1, self.height - 2 - player_tile_size)
            if all(self.dungeon[player_y + dy][player_x + dx] == '.' for dx in range(player_tile_size) for dy in range(player_tile_size)):
                # Return player's starting position in pixel coordinates
                return [player_x * self.tile_size, player_y * self.tile_size]

        # If no suitable starting location is found, raise an exception
        raise Exception("Free space not found")

    def create_static_sprites(self):
        # This method creates the static sprites for the dungeon
        static_sprites = pygame.sprite.Group()

        for y, row in enumerate(self.dungeon):
            for x, cell in enumerate(row):
                pos = (x * self.tile_size, y * self.tile_size)
                if cell == "W":
                    wall_sprite = pygame.sprite.Sprite()
                    wall_sprite.image = self.wall_sprite
                    wall_sprite.rect = wall_sprite.image.get_rect(topleft=pos)
                    static_sprites.add(wall_sprite)
                elif cell == ".":
                    floor_sprite = pygame.sprite.Sprite()
                    floor_sprite.image = self.floor_sprite
                    floor_sprite.rect = floor_sprite.image.get_rect(topleft=pos)
                    static_sprites.add(floor_sprite)
        return static_sprites
