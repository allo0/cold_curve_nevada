import pygame.draw

from src.characters.generEnemyModel import Enemy


class FastEnemy(Enemy):
    def __init__(self, difficulty):
        super().__init__(difficulty=difficulty)
        self.image.fill((125, 125, 125))
        self._speed *= 2
        self._health *= 0.8
        self._exp *= 0.5
        self._points *= 0.8

class TankEnemy(Enemy):
    def __init__(self, difficulty):
        super().__init__(difficulty=difficulty)
        self.image.fill((210, 50, 50))
        self._health *= 2
        self._exp *= 1.1
        self._points *= 1


class StrongEnemy(Enemy):
    def __init__(self, difficulty):
        super().__init__(difficulty=difficulty)
        self.image.fill((45, 210, 165))
        self._health *= 1.4
        self._damage *= 1.5
        self._exp *= 1.1
        self._points *= 1.1


class FirstBossEnemy(Enemy):

    def __init__(self, difficulty):
        super().__init__(difficulty=difficulty)
        self._id = "first_boss"
        self.image = pygame.Surface((69, 69))  # Example placeholder image
        self.image.fill((69, 69, 69))
        self._health *= 5
        self._damage *= 1.9
        self._speed *= 0.9
        self._exp *= 2
        self._points *= 2


class SecondBossEnemy(Enemy):

    def __init__(self, difficulty):
        super().__init__(difficulty=difficulty)
        self._id = "second_boss"
        self.image = pygame.Surface((85, 85))  # Example placeholder image
        self.image.fill((100, 210, 45))
        self._health *= 13
        self._damage *= 3
        self._speed *= 3
        self._points *= 3
