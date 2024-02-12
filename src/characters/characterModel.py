import uuid

import pygame

from configs import logConf
from configs.entitiesConf import GENERIC_CONFIG

logger = logConf.logger


class Character(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self._id = str(uuid.uuid4())[-12:]
        self.image = pygame.Surface((50,50))  # Example placeholder image
        self.image.fill((255, 0, 0))  # Red square
        self._rect = self.image.get_rect()
        # TODO change the movement system to Vector2D
        self.rect.center = (x, y)
        self._speed = GENERIC_CONFIG["speed"]
        self._health = GENERIC_CONFIG["health"]
        self._iframes = 0  # Number of iframes after being hit (0 means not invulnerable)
        self._invincible = False  # Flag to track if the player is currently invincible
        # Cooldown for hit
        self._hit_cooldown = 0  # Initialize the cooldown timer
        self._hit_cooldown_duration = GENERIC_CONFIG["iframes"]  # Adjust this value as needed (in frames)
        self._mask = pygame.mask.from_surface(self.image)

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, value):
        self._mask = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def hit_cooldown(self):
        return self._hit_cooldown

    @hit_cooldown.setter
    def hit_cooldown(self, value):
        self._hit_cooldown = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

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
    def iframes(self):
        return self._iframes

    @iframes.setter
    def iframes(self, value):
        self._iframes = value

    @property
    def invincible(self):
        return self._invincible

    @invincible.setter
    def invincible(self, value):
        self._invincible = value

    def update(self):
        # Generic method, to be implemented by the subclasses
        if self.iframes > 0:
            self.iframes -= 1
            self.image.set_alpha(128)  # Make the player semi-transparent during iframes
        else:
            self.image.set_alpha(255)  # Reset transparency
            self.end_iframes()  # Call end_iframes when iframes are over

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

    def end_iframes(self):
        # Called when iframes are over
        self.invincible = False

    def hit(self):
        # Handle iframes only
        if not self.invincible:
            self.iframes = GENERIC_CONFIG["iframes"]
            self.invincible = True
            # Set the cooldown to prevent repeated hits
            self.hit_cooldown = self.hit_cooldown_duration

    def take_damage(self, damage):
        if not self.invincible and self.hit_cooldown == 0 and self.health > 0:
            self.health -= damage
            self.hit()
            return self.health
        else:
            return self.health

    # def cast_ray(self, start_pos, direction, wall_rects, max_distance):
    #     # Calculate the end position of the ray based on the direction and max_distance
    #     end_pos = start_pos + direction * max_distance
    #
    #     # Create a rect that represents the ray
    #     # Its size depends on the direction of the ray
    #     if direction.x != 0:  # Horizontal ray
    #         ray_rect = pygame.Rect(start_pos.x, start_pos.y, max_distance, self.rect.height)
    #     else:  # Vertical ray
    #         ray_rect = pygame.Rect(start_pos.x, start_pos.y, self.rect.width, max_distance)
    #
    #     # Adjust the ray rect position based on the direction
    #     if direction.x < 0:  # Left
    #         ray_rect.topleft = (end_pos.x, start_pos.y)
    #     elif direction.x > 0:  # Right
    #         ray_rect.topright = (end_pos.x, start_pos.y)
    #     if direction.y < 0:  # Up
    #         ray_rect.topleft = (start_pos.x, end_pos.y)
    #     elif direction.y > 0:  # Down
    #         ray_rect.bottomleft = (start_pos.x, end_pos.y)
    #
    #     # Check for collision with wall_rects
    #     for wall_rect in wall_rects:
    #         if ray_rect.colliderect(wall_rect):
    #             # If there's a collision, return the closest point of collision
    #             if direction.x < 0:  # Left
    #                 return wall_rect.topright
    #             elif direction.x > 0:  # Right
    #                 return wall_rect.topleft
    #             if direction.y < 0:  # Up
    #                 return wall_rect.bottomleft
    #             elif direction.y > 0:  # Down
    #                 return wall_rect.topleft
    #
    #     # If no collision occurred, return the end position of the ray
    #     return end_pos
    def cast_ray(self, direction, wall_rects, max_distance):
        # If there is no movement direction, don't change the position
        if direction.length() == 0:
            return pygame.math.Vector2(self.rect.center)

        # Start the ray from the center of the player
        start_pos = pygame.math.Vector2(self.rect.center)

        # Calculate the end position of the ray
        end_pos = start_pos + direction * max_distance

        # Create a virtual ray rect based on direction
        if direction.x != 0:  # Horizontal movement
            ray_rect = pygame.Rect(start_pos.x, start_pos.y, max_distance, self.rect.height)
        else:  # Vertical movement
            ray_rect = pygame.Rect(start_pos.x, start_pos.y, self.rect.width, max_distance)

        # Adjust ray_rect position based on direction
        if direction.x < 0:  # Left
            ray_rect.width += self.rect.width  # Extend the width to include the player's width
            ray_rect.topleft = (start_pos.x - ray_rect.width, start_pos.y)
        elif direction.x > 0:  # Right
            ray_rect.width += self.rect.width
        if direction.y < 0:  # Up
            ray_rect.height += self.rect.height  # Extend the height to include the player's height
            ray_rect.topleft = (start_pos.x, start_pos.y - ray_rect.height)
        elif direction.y > 0:  # Down
            ray_rect.height += self.rect.height

        # Check collision with the wall
        for wall_rect in wall_rects:
            if ray_rect.colliderect(wall_rect):
                # Adjust the end position based on the collision
                if direction.x != 0:  # Horizontal collision
                    end_pos.x = wall_rect.left if direction.x > 0 else wall_rect.right
                if direction.y != 0:  # Vertical collision
                    end_pos.y = wall_rect.top if direction.y > 0 else wall_rect.bottom
                break

        return end_pos
