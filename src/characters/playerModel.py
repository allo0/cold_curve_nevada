import logging

import pygame

from cold_curve_nevada.configs import logConf
from cold_curve_nevada.configs.Events import (PLAYERDEATH)
from cold_curve_nevada.configs.entitiesConf import PLAYER_CONFIG
from cold_curve_nevada.src.characters.characterModel import Character
from cold_curve_nevada.src.utils.networkModel import Network

logger = logConf.logger


# You can create different character classes for the player and enemies and add specific behaviors.
class Player(Character):
    iframes = 60

    def __init__(self, x, y):
        super().__init__(x, y)
        # Access the global logger object from main.py
        self.logger = logging.getLogger("miami")
        self.logger.info(f"Player {self.id} initialized")

        self.image.fill((255, 255, 0))

        self.speed = PLAYER_CONFIG["speed"]
        self.health = PLAYER_CONFIG["health"]
        self.iframes = 0  # Number of iframes after being hit (0 means not invulnerable)
        self.invincible = False  # Flag to track if the player is currently invincible
        # Cooldown for hit
        self.hit_cooldown = 0  # Initialize the cooldown timer
        self.hit_cooldown_duration = PLAYER_CONFIG["iframes"]  # Adjust this value as needed (in frames)
        # New attributes for multiplayer
        self.multiplayer = None
        self.network = None

    def set_network(self, player_instance, player_index):
        self.network = Network(player=self, init_network=self.multiplayer, player_index=player_index)
        return self.network

    def get_network(self):
        return self.network

    def set_multiplayer(self, multiplayer):
        self.multiplayer = multiplayer

    def init_network(self):
        if self.multiplayer and self.network:
            self.set_initial_position()  # Set the initial position on the server

    def set_initial_position(self):
        if self.network:
            self.network.send({"id": self.id, "x": self.rect.x, "y": self.rect.y, "health": self.health})

    def update(self):
        super().update()
        # TODO maybe migrate the iframes and hit-cooldown functionality to the parent class
        if self.iframes > 0:
            self.iframes -= 1
            self.image.set_alpha(128)  # Make the player semi-transparent during iframes
        else:
            self.image.set_alpha(255)  # Reset transparency
            self.end_iframes()  # Call end_iframes when iframes are over

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

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

    def take_damage(self, damage):
        # Deduct health when the player takes damage
        if not self.invincible and self.hit_cooldown == 0 and self.health > 0:
            self.health -= damage
            self.logger.debug(f"Current HP: {self.health}")
            self.hit()
        elif self.health <= 0:
            player_death_event = pygame.event.Event(PLAYERDEATH, custom_text='YA DEAD')
            pygame.event.post(player_death_event)

    def hit(self):
        # Handle iframes only
        if not self.invincible:
            self.iframes = PLAYER_CONFIG["iframes"]
            self.invincible = True
            # Set the cooldown to prevent repeated hits
            self.hit_cooldown = self.hit_cooldown_duration

    def end_iframes(self):
        # Called when iframes are over
        self.invincible = False
        self.was_hit = False  # Reset the flag for the next collision

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
