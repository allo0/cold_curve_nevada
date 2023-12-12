import random
import time

from cold_curve_nevada.src.characters.generEnemyModel import Enemy


class Spawner(Enemy):

    def __init__(self, sprite_group, enemy_group, player):
        self.start_time = time.time()
        self.last_spawn_time = self.start_time
        self.next_spawn_delay = random.uniform(0.5, 2)

    def spawn_enemies(self, difficulty):
        current_time = time.time()
        if current_time - self.last_spawn_time >= self.next_spawn_delay:

            new_enemies = []
            elapsed_time = time.time() - self.start_time
            if elapsed_time < 300:  # First 2 minutes
                for _ in range(3):
                    enemy = Enemy(difficulty)
                    new_enemies.append(enemy)
            # Reset the last spawn time and calculate the next spawn delay
            self.last_spawn_time = current_time
            self.next_spawn_delay = random.uniform(0.5, 2)

            return new_enemies
        else:
            return []
