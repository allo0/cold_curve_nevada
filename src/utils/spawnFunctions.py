import random
import time

from cold_curve_nevada.src.characters.generEnemyModel import Enemy
from configs import logConf
from src.characters.enemiesModel import FastEnemy, TankEnemy, StrongEnemy, FirstBossEnemy, SecondBossEnemy

logger = logConf.logger


class EnemyFactory:
    @staticmethod
    def create_enemy(enemy_type, difficulty):
        if enemy_type == "generic":
            return Enemy(difficulty)
        elif enemy_type == "fast":
            return FastEnemy(difficulty)
        elif enemy_type == "tank":
            return TankEnemy(difficulty)
        elif enemy_type == "strong":
            return StrongEnemy(difficulty)
        elif enemy_type == "first_boss":
            return FirstBossEnemy(difficulty)
        elif enemy_type == "second_boss":
            return SecondBossEnemy(difficulty)
        # ... handle other enemy types
        else:
            raise ValueError("Unknown enemy type")


class Spawner(Enemy):

    def __init__(self, sprite_group, enemy_group, player):
        self.start_time = time.time()
        self.last_spawn_time = self.start_time
        self.next_spawn_delay = random.uniform(0.5, 2)
        self._player = player
        self._spawned_boss = 0

    @property
    def spawned_boss(self):
        return self._spawned_boss

    @spawned_boss.setter
    def spawned_boss(self, value):
        self._spawned_boss = value

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value

    def spawn_enemies(self, difficulty):
        total_enemies_killed = self.player[0].enemies_killed

        current_time = time.time()
        if current_time - self.last_spawn_time >= self.next_spawn_delay:

            new_enemies = []
            elapsed_time = time.time() - self.start_time
            if elapsed_time < 30:  # First 30 secs
                for _ in range(2):
                    enemy = EnemyFactory.create_enemy("generic", difficulty=difficulty)
                    new_enemies.append(enemy)
            if 30 < elapsed_time < 90:  # 30s <-> 1.5m
                for _ in range(3):
                    enemy = EnemyFactory.create_enemy("generic", difficulty=difficulty)
                    new_enemies.append(enemy)
                if random.random() < 0.3:  # 30% chance for fast
                    enemy = EnemyFactory.create_enemy("fast", difficulty=difficulty)
                    new_enemies.append(enemy)
                if random.random() < 0.05:  # 5% chance for tank
                    enemy = EnemyFactory.create_enemy("tank", difficulty=difficulty)
                    new_enemies.append(enemy)
            if 90 < elapsed_time < 120:  # 1.5m <-> 2m   Hard round
                for _ in range(2):
                    enemy = EnemyFactory.create_enemy("strong", difficulty=difficulty)
                    new_enemies.append(enemy)
                if random.random() < 0.3:  # 30% chance for tank
                    enemy = EnemyFactory.create_enemy("tank", difficulty=difficulty)
                    new_enemies.append(enemy)
            if 120 < elapsed_time < 180:  # 2m <-> 3m   whatever round
                for _ in range(3):
                    enemy = EnemyFactory.create_enemy("strong", difficulty=difficulty)
                    new_enemies.append(enemy)
                if random.random() < 0.5:  # 50% chance for fast
                    enemy = EnemyFactory.create_enemy("fast", difficulty=difficulty)
                    new_enemies.append(enemy)
                if random.random() < 0.3:  # 30% chance for tank
                    enemy = EnemyFactory.create_enemy("tank", difficulty=difficulty)
                    new_enemies.append(enemy)
            if total_enemies_killed >= 50 and self.spawned_boss == 0:  # 50 kill boss spawn
                enemy = EnemyFactory.create_enemy("second_boss", difficulty=difficulty)
                new_enemies.append(enemy)
                self.spawned_boss += 1
            if total_enemies_killed >= 500 and self.spawned_boss == 1:  # 500 kill boss spawn
                enemy = EnemyFactory.create_enemy("second_boss", difficulty=difficulty)
                new_enemies.append(enemy)
                self.spawned_boss += 1

            # Reset the last spawn time and calculate the next spawn delay
            self.last_spawn_time = current_time
            self.next_spawn_delay = random.uniform(0.5, 2)

            return new_enemies

        else:
            return []
