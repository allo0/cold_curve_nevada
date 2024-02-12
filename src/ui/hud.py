import pygame


class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.font = pygame.font.Font(None, 30)  # Choose your font and size
        self.hp = 100  # Example starting HP
        self.max_hp = 100  # Maximum HP
        self.score = 0  # Starting score
        self.start_time = pygame.time.get_ticks()  # Game start time
        self.current_xp = 0  # Starting XP
        self.max_xp = 300  # XP needed to reset and potentially level up

        # Health bar settings
        self.hp_bar_width = 200  # Total width of the health bar
        self.hp_bar_height = 20
        # Position the health bar at the bottom left, with a 10 pixel margin
        self.hp_bar_pos = (10, self.screen_height - self.hp_bar_height - 10)

        # XP bar settings
        self.xp_bar_width = 200
        self.xp_bar_height = 10
        self.xp_bar_pos = (10, self.screen_height - self.hp_bar_height - self.xp_bar_height - 20)

        self.aoe_zone=None
        self.total_enemies_killed = 0  # Counter for total enemies killed

    def update_total_enemies_killed(self, total_enemies_killed):
        self.total_enemies_killed = total_enemies_killed

    def update_aoe_zone(self, aoe_zone):
        self.aoe_zone = aoe_zone

    def update_hp(self, hp):
        self.hp = max(0, min(hp, self.max_hp))  # Ensure HP stays within bounds

    def update_xp(self, current_exp, max_exp):
        self.current_xp = current_exp
        self.max_xp = max_exp
        # Automatically handle the level-up logic here if needed
        if self.current_xp >= self.max_xp:
            self.current_xp -= self.max_xp  # Carry over the excess XP to the next level
            # Additional level-up logic can go here

    def update_score(self, score):
        self.score = score

    def draw_health_bar(self):
        # Draw background of the health bar
        pygame.draw.rect(self.screen, (255, 0, 0),
                         (self.hp_bar_pos[0], self.hp_bar_pos[1], self.hp_bar_width, self.hp_bar_height))

        # Calculate current health ratio
        current_hp_ratio = self.hp / self.max_hp

        # Draw the current health
        pygame.draw.rect(self.screen, (0, 255, 0), (
            self.hp_bar_pos[0], self.hp_bar_pos[1], self.hp_bar_width * current_hp_ratio, self.hp_bar_height))

    def draw_xp_bar(self):
        pygame.draw.rect(self.screen, (100, 100, 255),
                         (self.xp_bar_pos[0], self.xp_bar_pos[1], self.xp_bar_width, self.xp_bar_height))
        current_xp_ratio = self.current_xp / self.max_xp
        pygame.draw.rect(self.screen, (255, 255, 0), (
            self.xp_bar_pos[0], self.xp_bar_pos[1], self.xp_bar_width * current_xp_ratio, self.xp_bar_height))

    def draw_aoe_zone_stats(self):
        # Define starting position for the AoE zone stats
        start_pos = (self.screen_width - 10, 10)
        line_height = 20  # Height of each line of text

        # Split the AoE zone stats into separate lines
        aoe_zone_stats = [
            f'AOE ZONE',
            f'Range: {self.aoe_zone.radius}',
            f'Damage: {self.aoe_zone.damage}',
            f'Attack Speed: {self.aoe_zone.attack_speed}'
        ]

        # Render and blit each line separately
        for i, stat in enumerate(aoe_zone_stats):
            stat_text = self.font.render(stat, True, (255, 255, 255))
            text_rect = stat_text.get_rect(topright=(start_pos[0], start_pos[1] + i * line_height))
            self.screen.blit(stat_text, text_rect)

    def draw(self):
        # Draw the health bar
        self.draw_health_bar()
        # Draw the exp bar
        self.draw_xp_bar()

        self.draw_aoe_zone_stats()

        # Display Score at the top left
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))  # Adjusted position

        # Display the total enemies killed at the top center
        enemies_killed_text = self.font.render(f'Enemies Killed: {self.total_enemies_killed}', True, (255, 255, 255))
        text_rect = enemies_killed_text.get_rect(center=(self.screen_width / 2, 10))
        self.screen.blit(enemies_killed_text, text_rect)

        # Display Time at the top left, below the score
        current_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert ms to s
        time_text = self.font.render(f'Time: {current_time}s', True, (255, 255, 255))
        self.screen.blit(time_text, (10, 40))  # Adjusted position
