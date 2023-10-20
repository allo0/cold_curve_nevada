from configs.entitiesConf import SIMPLE_ENEMY_CONFIG
from src.characters.characterModel import Character


class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.image.fill((255, 0, 255))

        self.speed = SIMPLE_ENEMY_CONFIG["speed"]
        self.health = SIMPLE_ENEMY_CONFIG["health"]

    def update(self, player):
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
        player.take_damage(SIMPLE_ENEMY_CONFIG["damage"])  # Adjust the damage value as needed
