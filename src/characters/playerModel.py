import random

import pygame
from pydantic import BaseModel

from cold_curve_nevada.configs import logConf
from cold_curve_nevada.configs.Events import (
    PLAYERDEATH, FINAL_BOSS_KILLED,

)
from cold_curve_nevada.configs.entitiesConf import PLAYER_CONFIG
from cold_curve_nevada.src.characters.characterModel import Character
from cold_curve_nevada.src.models.attacksModel import AoE_Zone
from cold_curve_nevada.src.models.networkModel import Network
from cold_curve_nevada.src.utils.utilFunctions import Utils
from configs.appConf import Settings
from configs.assetsConf import SOUNDS, SOUND_LEVEL
from src.utils.dataHandler import DataHandler

logger = logConf.logger


class Player(Character):

    def __init__(self, x, y, name, sound_controller, images):
        super().__init__(x, y)
        self.name = name
        logger.info(f"Player {self.id} with name {self.name} initialized")
        self.images = images
        self.index = 0
        self.direction = 'still'
        self.image = pygame.image.load(images[f"{self.direction}_{self.index + 1}"]).convert_alpha()
        self.animation_time = 0.1  # Time each frame is displayed
        self.current_time = 0

        self._speed = PLAYER_CONFIG["speed"]
        self._health = PLAYER_CONFIG["health"]

        self._hit_cooldown_duration = PLAYER_CONFIG["iframes"]

        self._multiplayer = None
        self._network = None

        # Create an instance of the AoE_Zone class
        self._aoe_zone = AoE_Zone(self.rect)
        # self._line_of_doom = RotatingLine(self.rect)

        self._level = PLAYER_CONFIG["level"]
        self._current_exp = 0
        self._enemies_killed = 0
        self._total_points = 0
        self.score_data_handler = DataHandler(Settings.SCORES)

        self.sound_controller = sound_controller

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

    def update(self, enemies, wall_rects, dt, hud):
        super().update()
        hud.update_hp(self.health)
        hud.update_score(self.total_points)
        hud.update_xp(self.current_exp, Utils.calculate_experience_custom(level=self.level))
        hud.update_total_enemies_killed(self.enemies_killed)
        hud.update_aoe_zone(self.aoe_zone)
        hud.update_level(self.level)

        if self.health <= 0:
            player_death_event = pygame.event.Event(PLAYERDEATH, custom_text='YA DEAD')
            pygame.event.post(player_death_event)

        # Implement character movement and actions here
        keys = pygame.key.get_pressed()
        key_pressed = False
        if not self.multiplayer:
            # Single-player mode controls
            if keys[pygame.K_a]:
                self.move_player(self, wall_rects, 'left')
                self.direction = 'left'
                key_pressed = True
            if keys[pygame.K_d]:
                self.move_player(self, wall_rects, 'right')
                self.direction = 'right'
                key_pressed = True
            if keys[pygame.K_w]:
                self.move_player(self, wall_rects, 'back')
                self.direction = 'back'
                key_pressed = True
            if keys[pygame.K_s]:
                self.move_player(self, wall_rects, 'front')
                self.direction = 'front'
                key_pressed = True

        if not key_pressed:
            self.direction = "still"

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % 3  # Assuming 3 frames per direction
            self.image = pygame.image.load(self.images[f"{self.direction}_{self.index + 1}"]).convert_alpha()

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

            self.sound_controller.play_sound(SOUNDS["level_up"], SOUND_LEVEL["level_up"])

            # heal player
            self.heal_player(self.health * PLAYER_CONFIG["level_up_heal"])
            upgrades = ['aoe_radius', 'aoe_attack_speed', 'aoe_damage']
            weights = [1.1, 1.1, 1]

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
                        if enemy.id == "first_boss":
                            final_boss_killed = pygame.event.Event(FINAL_BOSS_KILLED,
                                                                   custom_text='Killed the final boss')
                            self.score_data_handler.write_data(
                                PlayerScore(player_name=self.name,
                                            enemies_killed=self.enemies_killed,
                                            total_points=self.total_points,
                                            level=self.level))

                            test = self.score_data_handler.read_data()
                            logger.debug(f"{test}")
                            pygame.event.post(final_boss_killed)

                        enemy.kill()
                        self.current_exp += enemy.exp
                        self.enemies_killed += 1
                        self.total_points += enemy.points
                        del enemy
                        logger.info(
                            f"Player {self.id} enemies killed: {self.enemies_killed} and total points: {self.total_points}")

    def move_player(self, player, obstacles, direction):
        """Move the player if no collision is detected in the intended direction."""
        original_position = player.rect.copy()  # Copy the original position

        # Update player's position based on direction
        if direction == 'right':
            player.rect.x += player.speed
        elif direction == 'left':
            player.rect.x -= player.speed
        elif direction == 'back':
            player.rect.y -= player.speed
        elif direction == 'front':
            player.rect.y += player.speed

        # Check for collisions with any obstacles
        for obstacle in obstacles:
            if player.rect.colliderect(obstacle):
                player.rect = original_position  # Reset to original position if collision detected
                break  # Exit the loop early if a collision is found


class PlayerScore(BaseModel):
    player_name: str
    enemies_killed: int
    total_points: float
    level: int
