import pygame.draw

from src.characters.generEnemyModel import Enemy


class FastEnemy(Enemy):
    def __init__(self, difficulty, image):
        super().__init__(difficulty=difficulty, image=image)
        self.image = image
        self._speed *= 2
        self._health *= 0.8
        self._exp *= 0.5
        self._points *= 0.8


class TankEnemy(Enemy):
    def __init__(self, difficulty, image):
        super().__init__(difficulty=difficulty, image=image)
        self.image = image
        self.image=pygame.transform.scale(self.image, (40,40))
        self._health *= 2
        self._exp *= 1.1
        self._points *= 1


class StrongEnemy(Enemy):
    def __init__(self, difficulty, image):
        super().__init__(difficulty=difficulty, image=image)
        self.image = image
        self._health *= 1.4
        self._damage *= 1.5
        self._exp *= 1.1
        self._points *= 1.1


class FirstBossEnemy(Enemy):

    def __init__(self, difficulty, image):
        super().__init__(difficulty=difficulty, image=image)
        self._id = "first_boss"
        self.image = image
        self.image = pygame.transform.scale(self.image, (64, 64))
        self._health *= 5
        self._damage *= 1.9
        self._speed *= 0.9
        self._exp *= 2
        self._points *= 2


class SecondBossEnemy(Enemy):

    def __init__(self, difficulty, image):
        super().__init__(difficulty=difficulty, image=image)
        self._id = "second_boss"
        self.image = image
        self.image = pygame.transform.scale(self.image, (64, 64))
        self._health *= 13
        self._damage *= 3
        self._speed *= 3
        self._points *= 3
