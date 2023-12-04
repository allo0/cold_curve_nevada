import pygame

from cold_curve_nevada.configs import logConf
from cold_curve_nevada.configs.Events import (
    PLAYERDEATH,

)
from cold_curve_nevada.configs.entitiesConf import PLAYER_CONFIG
from cold_curve_nevada.src.characters.characterModel import Character
from cold_curve_nevada.src.utils.networkModel import Network

logger = logConf.logger


class Player(Character):

    def __init__(self, x, y):
        super().__init__(x, y)
        logger.info(f"Player {self.id} initialized")

        self.image.fill((255, 255, 0))

        self.__speed = PLAYER_CONFIG["speed"]
        self.__health = PLAYER_CONFIG["health"]
        self.__damage = PLAYER_CONFIG["damage"]

        self.__hit_cooldown_duration = PLAYER_CONFIG["iframes"]

        self.__multiplayer = None
        self.__network = None

        # Inner class for semi-transparent area
        class AoE_Zone(pygame.sprite.Sprite):
            def __init__(self, player_rect):
                super().__init__()
                self.image = pygame.Surface((PLAYER_CONFIG["aoe_radius"] * 2, PLAYER_CONFIG["aoe_radius"] * 2),
                                            pygame.SRCALPHA)
                pygame.draw.circle(self.image, (255, 255, 255, 32),
                                   (PLAYER_CONFIG["aoe_radius"], PLAYER_CONFIG["aoe_radius"]),
                                   PLAYER_CONFIG["aoe_radius"])
                self.rect = self.image.get_rect(center=player_rect.center)

            def update(self, player_rect):
                self.rect.center = player_rect.center

        # Create an instance of the AoE_Zone class
        self.__aoe_zone = AoE_Zone(self.rect)

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, value):
        self.__speed = value

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        self.__health = value

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, value):
        self.__damage = value

    @property
    def hit_cooldown_duration(self):
        return self.__hit_cooldown_duration

    @hit_cooldown_duration.setter
    def hit_cooldown_duration(self, value):
        self.__hit_cooldown_duration = value

    @property
    def network(self):
        return self.__network

    @network.setter
    def network(self, value):
        self.__network = value

    @property
    def multiplayer(self):
        return self.__multiplayer

    @multiplayer.setter
    def multiplayer(self, value):
        self.__multiplayer = value

    @property
    def aoe_zone(self):
        return self.__aoe_zone

    @aoe_zone.setter
    def aoe_zone(self, value):
        self.__aoe_zone = value

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

        for enemy in enemies:
            if self.aoe_zone.rect.colliderect(enemy.rect):
                enemy_health = self.attack(enemy)
                if enemy_health <= 0:
                    enemy.kill()
                    del enemy
        # Update the transparent area
        self.aoe_zone.update(self.rect)

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
        return enemy.take_damage(self.damage)

    def get_player_data(self):
        return {
            "id": self.id,
            "x": self.rect.x,
            "y": self.rect.y,
            "health": self.health,
            # Add any other relevant data you want to send
        }

    def update_from_data(self, data):
        if data is not None:
            self.id = data["id"]
            self.rect.x = data["x"]
            self.rect.y = data["y"]
            self.health = data["health"]
            # Update any other relevant data you received
