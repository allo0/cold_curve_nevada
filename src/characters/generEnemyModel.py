from random import choice

from configs import logConf
from configs.entitiesConf import ENEMY_CONFIG, MISC
from src.characters.characterModel import Character

logger = logConf.logger


class Enemy(Character):
    def __init__(self, difficulty):
        spawn_coordinates = choice(MISC["spawns"])
        self.difficulty_multipliers = MISC["difficulty_multipliers"][difficulty]

        super().__init__(spawn_coordinates[0], spawn_coordinates[1])

        self.image.fill((255, 0, 255))

        self._speed = ENEMY_CONFIG["speed"] * self.difficulty_multipliers['speed']
        self._health = ENEMY_CONFIG["health"] * self.difficulty_multipliers['health']
        self._damage = ENEMY_CONFIG["damage"] * self.difficulty_multipliers['damage']
        self._exp = ENEMY_CONFIG["exp"] * self.difficulty_multipliers['exp']
        self._points = ENEMY_CONFIG["points"] * self.difficulty_multipliers['points']

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        self._exp = value

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value):
        self._points = value

    def update(self, players):
        super().update()

        for player in players:
            # Move the enemy towards the player
            dx = player.rect.x - self.rect.x
            dy = player.rect.y - self.rect.y
            dist = (dx ** 2 + dy ** 2) ** 0.5  # Calculate distance to the player
            if dist != 0:
                dx = dx / dist
                dy = dy / dist
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
            # Check if enemy collides with the player
            if self.rect.colliderect(player.rect):
                self.attack(player)

    def attack(self, player):
        # Calculate and apply damage to the player
        logger.info(f"Player {player.id} current HP: {player.health}")

        player.take_damage(self.damage)  # Adjust the damage value as needed

    def hit(self):
        # just used to override the default is-hit mechanism and the
        # invincibility after being hit
        pass
