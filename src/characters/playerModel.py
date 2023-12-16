import random

import pygame

from cold_curve_nevada.configs import logConf
from cold_curve_nevada.configs.Events import (
    PLAYERDEATH, FINAL_BOSS_KILLED,

)
from cold_curve_nevada.configs.entitiesConf import PLAYER_CONFIG
from cold_curve_nevada.src.characters.characterModel import Character
from cold_curve_nevada.src.models.attacksModel import AoE_Zone
from cold_curve_nevada.src.models.networkModel import Network
from cold_curve_nevada.src.utils.utilFunctions import Utils

logger = logConf.logger


class Player(Character):

    def __init__(self, x, y):
        super().__init__(x, y)
        logger.info(f"Player {self.id} initialized")

        self.image.fill((255, 255, 0))

        self._speed = PLAYER_CONFIG["speed"]
        self._health = PLAYER_CONFIG["health"]

        self._hit_cooldown_duration = PLAYER_CONFIG["iframes"]

        self._multiplayer = None
        self._network = None

        # Inner class for semi-transparent area

        # Create an instance of the AoE_Zone class
        self._aoe_zone = AoE_Zone(self.rect)
        # self._line_of_doom = RotatingLine(self.rect)

        self._level = PLAYER_CONFIG["level"]
        self._current_exp = 0
        self._enemies_killed = 0
        self._total_points = 0

    @property
    def total_points(self):
        return self._total_points

    @total_points.setter
    def total_points(self, value):
        self._total_points = value

    @property
    def hit_cooldown_duration(self):
        return self._hit_cooldown_duration

    @hit_cooldown_duration.setter
    def hit_cooldown_duration(self, value):
        self._hit_cooldown_duration = value

    @property
    def multiplayer(self):
        return self._multiplayer

    @multiplayer.setter
    def multiplayer(self, value):
        self._multiplayer = value

    @property
    def aoe_zone(self):
        return self._aoe_zone

    @aoe_zone.setter
    def aoe_zone(self, value):
        self._aoe_zone = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def line_of_doom(self):
        return self._line_of_doom

    @line_of_doom.setter
    def line_of_doom(self, value):
        self._line_of_doom = value

    @property
    def enemies_killed(self):
        return self._enemies_killed

    @enemies_killed.setter
    def enemies_killed(self, value):
        self._enemies_killed = value

    @property
    def line_of_doom(self):
        return self._line_of_doom

    @line_of_doom.setter
    def line_of_doom(self, value):
        self._line_of_doom = value

    @property
    def current_exp(self):
        return self._current_exp

    @current_exp.setter
    def current_exp(self, value):
        self._current_exp = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

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
    def hit_cooldown_duration(self):
        return self._hit_cooldown_duration

    @hit_cooldown_duration.setter
    def hit_cooldown_duration(self, value):
        self._hit_cooldown_duration = value

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, value):
        self._network = value

    @property
    def multiplayer(self):
        return self._multiplayer

    @multiplayer.setter
    def multiplayer(self, value):
        self._multiplayer = value

    @property
    def aoe_zone(self):
        return self._aoe_zone

    @aoe_zone.setter
    def aoe_zone(self, value):
        self._aoe_zone = value

    def set_network(self, player_instance, player_index):
        self.network = Network(player=self, init_network=self.multiplayer, player_index=player_index)
        return self.network

    def init_network(self):
        if self.multiplayer and self.network:
            self.set_initial_position()  # Set the initial position on the server

    def set_initial_position(self):
        if self.network:
            self.network.send({"id": self.id, "x": self.rect.x, "y": self.rect.y, "health": self.health})

    def update(self, enemies):
        super().update()

        if self.health <= 0:
            player_death_event = pygame.event.Event(PLAYERDEATH, custom_text='YA DEAD')
            pygame.event.post(player_death_event)

        # Implement character movement and actions here
        keys = pygame.key.get_pressed()

        if not self.multiplayer:
            # Single-player mode controls
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
            if keys[pygame.K_s]:
                self.rect.y += self.speed

            # else:
            #     # Multiplayer mode controls
            #     if self.network:
            #         server_data = self.network.getP()
            #         if server_data:
            #             self.rect.x = server_data.get("x", self.rect.x)
            #             self.rect.y = server_data.get("y", self.rect.y)

        # Kill enemies
        self.check_if_killed(enemies=enemies)

        # # Update the transparent area
        self.aoe_zone.update(self.rect)
        # self._line_of_doom.update(self.rect)

        # Level Up
        self.leveling_management(level=self.level)

        ####### This is deprecated since implemented the camera #######
        # # Keep player on the game_screen

        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.right > Settings.SCREEN_WIDTH:
        #     self.rect.right = Settings.SCREEN_WIDTH
        # if self.rect.top <= 0:
        #     self.rect.top = 0
        # if self.rect.bottom >= Settings.SCREEN_HEIGHT:
        #     self.rect.bottom = Settings.SCREEN_HEIGHT

        # Add more logic for shooting, health management, etc.

    def attack(self, enemy):
        logger.info(f"Enemy {enemy.id} current HP: {enemy.health}")

        return enemy.take_damage(self.aoe_zone.damage)

    def heal_player(self, health):
        new_health = self.health + health

        # If new hp exceeds maximum set it to max hp
        if new_health > PLAYER_CONFIG["health"]:
            self.health = PLAYER_CONFIG["health"]
        else:
            self.health = new_health

    def get_player_data(self):
        return {
            "id": self.id,
            "x": self.rect.x,
            "y": self.rect.y,
            "health": self.health,
            "kills": self.enemies_killed,
            # Add any other relevant data you want to send
        }

    def update_from_data(self, data):
        if data is not None:
            self.id = data["id"]
            self.rect.x = data["x"]
            self.rect.y = data["y"]
            self.health = data["health"]
            self.enemies_killed = data["enemies_killed"]

    def leveling_management(self, level):
        exp_need_for_level_up = Utils.calculate_experience_custom(level=level)
        if exp_need_for_level_up <= self.current_exp:
            self.level += 1

            # heal player
            self.heal_player(self.health * PLAYER_CONFIG["level_up_heal"])
            upgrades = ['aoe_radius', 'aoe_attack_speed', 'aoe_damage']
            weights = [1.3, 1, 1]

            upgrade = random.choices(upgrades, weights, k=1)[0]

            if upgrade == 'aoe_radius':
                self.aoe_zone.radius += 20
            elif upgrade == 'aoe_attack_speed':
                self.aoe_zone.attack_speed += 1
            elif upgrade == 'aoe_damage':
                self.aoe_zone.damage += 10

            logger.debug(f"radius {self.aoe_zone.radius} damage {self.aoe_zone.damage} as {self.aoe_zone.attack_speed}")
            # carry over any exp left to the next level
            self.current_exp = self.current_exp - exp_need_for_level_up
            logger.info(f"Lvl up: {self.level}"
                        f" & current exp: {self.current_exp}/{Utils.calculate_experience_custom(level=self.level)}")

    def check_if_killed(self, enemies):
        for enemy in enemies:
            if self.aoe_zone.rect.colliderect(enemy.rect):
                if self.aoe_zone.can_attack(Utils.get_curr_time()):
                    enemy_health = self.attack(enemy)
                    self.aoe_zone.last_attack_time = Utils.get_curr_time()
                    if enemy_health <= 0:
                        if enemy.id == "second_boss":
                            final_boss_killed = pygame.event.Event(FINAL_BOSS_KILLED,
                                                                   custom_text='Killed the final boss')
                            pygame.event.post(final_boss_killed)

                        enemy.kill()
                        self.current_exp += enemy.exp
                        self.enemies_killed += 1
                        self.total_points += enemy.points
                        del enemy
                        logger.info(
                            f"Player {self.id} enemies killed: {self.enemies_killed} and total points: {self.total_points}")
