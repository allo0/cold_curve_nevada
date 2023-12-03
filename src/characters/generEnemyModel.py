from random import choice

from configs.entitiesConf import SIMPLE_ENEMY_CONFIG, MISC
from src.characters.characterModel import Character


class Enemy(Character):
    def __init__(self, difficulty):
        spawn_coordinates = choice(MISC["spawns"])
        self.dificulty_multipliers = MISC["difficulty_multipliers"][difficulty]

        super().__init__(spawn_coordinates[0], spawn_coordinates[1])

        self.image.fill((255, 0, 255))

        self.speed = SIMPLE_ENEMY_CONFIG["speed"] * self.dificulty_multipliers['speed']
        self.health = SIMPLE_ENEMY_CONFIG["health"] * self.dificulty_multipliers['health']
        self.damage = SIMPLE_ENEMY_CONFIG["damage"] * self.dificulty_multipliers['damage']
        self.exp = SIMPLE_ENEMY_CONFIG["exp"] * self.dificulty_multipliers['exp']
        self.points = SIMPLE_ENEMY_CONFIG["points"] * self.dificulty_multipliers['points']


    def update(self, players):
        for player in players:
            # Move the enemy towards the player (you can customize the behavior)
            dx = player.rect.x - self.rect.x
            dy = player.rect.y - self.rect.y
            dist = (dx ** 2 + dy ** 2) ** 0.5  # Calculate distance to the player
            if dist != 0:
                dx = dx / dist
                dy = dy / dist
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed

            # Optional: You can add collision detection logic here
            # For example,
            if self.rect.colliderect(player.rect):
                self.attack(player)

    def attack(self, player):
        # Calculate and apply damage to the player
        player.take_damage(self.damage)  # Adjust the damage value as needed
