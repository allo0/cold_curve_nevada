import random
import time

from configs import logConf
from configs.assetsConf import SOUNDS
from configs.entitiesConf import SPAWN_PATTERNS, BOSS_SPAWN_CONDITIONS
from src.characters.enemiesModel import FastEnemy, TankEnemy, StrongEnemy, FirstBossEnemy, SecondBossEnemy
from src.characters.generEnemyModel import Enemy

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

    def __init__(self, sprite_group, enemy_group, player, sound_controller):
        self.start_time = time.time()
        self.last_spawn_time = self.start_time
        self.next_spawn_delay = random.uniform(0.5, 2)
        self._player = player
        self._spawned_boss = 0

        self.sound_controller = sound_controller
        self.spawn_config = SPAWN_PATTERNS
        self.boss_spawn_conditions = BOSS_SPAWN_CONDITIONS

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
        current_time = time.time()
        if current_time - self.last_spawn_time < self.next_spawn_delay:
            return []

        total_enemies_killed = self.player[0].enemies_killed
        new_enemies = self.generate_enemies(difficulty)
        new_enemies += self.generate_bosses(total_enemies_killed, difficulty)

        self.last_spawn_time = current_time
        self.next_spawn_delay = random.uniform(0.5, 2)

        return new_enemies

    def generate_enemies(self, difficulty):
        elapsed_time = time.time() - self.start_time
        new_enemies = []

        for field in self.spawn_config:
            if elapsed_time < field["time_limit"]:
                for enemy in field["possible_spawns"]:
                    enemy_type = enemy["type"]
                    quantity = enemy.get("quantity")
                    chance = enemy.get("chance")
                    self.create_and_add_enemies(enemy_type, quantity or chance, difficulty, new_enemies)
                break

        return new_enemies

    def create_and_add_enemies(self, enemy_type, quantity_or_chance, difficulty, enemies_list):
        if isinstance(quantity_or_chance, int):  # Fixed number of enemies
            for _ in range(quantity_or_chance):
                enemy = EnemyFactory.create_enemy(enemy_type, difficulty=difficulty)
                enemies_list.append(enemy)
        elif isinstance(quantity_or_chance, float):  # Chance-based enemy spawn
            if random.random() < quantity_or_chance:
                enemy = EnemyFactory.create_enemy(enemy_type, difficulty=difficulty)
                enemies_list.append(enemy)

    def generate_bosses(self, total_enemies_killed, difficulty):
        new_enemies = []
        for condition in self.boss_spawn_conditions:
            if total_enemies_killed >= condition["kill_threshold"] and self.spawned_boss == condition["boss_stage"]:
                enemy = EnemyFactory.create_enemy(condition["boss_type"], difficulty=difficulty)
                new_enemies.append(enemy)
                self.sound_controller.play_sound_with_fadein_fadeout(SOUNDS["boss_spawn"], fadein_duration=2000,
                                                                     total_duration=7, fadeout_duration=2000,
                                                                     final_volume=0.5)
                self.spawned_boss += 1
        return new_enemies
