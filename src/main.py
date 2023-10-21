import logging
import random

import pygame
from characters.generEnemyModel import Enemy
from characters.playerModel import Player
from configs.appConf import Settings
from configs.logConf import LogConfig, ScreenLog
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from utils.cameraModel import CameraGroup

logger = logging.getLogger("miami")
logging.basicConfig(format=LogConfig().LOG_FORMAT,
                    level=logging.DEBUG,
                    handlers=
                    [
                        logging.FileHandler("miami.log", mode='w', encoding='utf-8', ),
                        logging.StreamHandler()
                    ]
                    )


# # Create a custom event for adding a new enemy
# ADDENEMY = pygame.USEREVENT + 1
# pygame.time.set_timer(ADDENEMY, 250)
# # Variable to keep the main loop running
# running = True
# # Main loop
# while running:
#     current_time = time.time()
#
#     # for loop through the event queue
#     for event in pygame.event.get():
#       if event.type == ADDENEMY:
#             if len(enemies)>5:
#                 break
#             # Create the new enemy and add it to sprite groups
#             new_enemy = Enemy()
#             enemies.add(new_enemy)
#             all_sprites.add(new_enemy)
#             logger.info(new_enemy)

# TODO write unit tests where applicable
# TODO implement death scenario
# TODO implement player attack
# TODO implement spawns and mob variety
# TODO implement mob loot and scoring
# TODO implement scrollable background (infinitely generated background)
# TODO implement HUD
# TODO implement graphics
# TODO implement sounds
# TODO implement welcoming screen
# TODO implement difficulty levels
# TODO online/multiplayer functionality
# TODO cleanup and optimizations

def main():
    # Initialize Pygame
    pygame.init()

    # Create the game window
    screen = pygame.display.set_mode(Settings.RESOLUTION)
    pygame.display.set_caption(Settings.PROJECT_NAME)

    # Create player character
    player = Player(Settings.SCREEN_WIDTH // 2, Settings.SCREEN_HEIGHT // 2)

    # Create enemy characters
    enemies = pygame.sprite.Group()
    # TODO create a fleshed out spawing mechanism
    for _ in range(1):  # Create 5 enemy characters (you can adjust the number)
        enemy = Enemy(Settings.SCREEN_WIDTH + random.randint(1, 300) // 4,
                      Settings.SCREEN_HEIGHT + random.randint(1, 600) // 4)  # Initial positions (you can adjust)
        logger.info(f"Instanciated {enemy.id}")
        enemies.add(enemy)

    # Create sprite groups
    player_group = pygame.sprite.Group()  # Create a group for the player
    player_group.add(player)  # Add the player to the group
    enemies_group = pygame.sprite.Group()  # Create a group for enemies
    enemies_group.add(enemies)  # Add the enemies to the group

    # Create a combined group for rendering
    all_sprites = CameraGroup()
    all_sprites.add(player)
    all_sprites.add(enemies)

    screen_logs = ScreenLog()

    # Game loop
    running = True
    clock = pygame.time.Clock()
    frame_count = 0  # Initialize frame count

    while running:
        # Render
        screen.fill((0, 0, 0))  # Fill with black

        # Get the current FPS
        current_fps = int(clock.get_fps())

        # for loop through the event queue
        for event in pygame.event.get():
            # Check for KEYDOWN event
            if event.type == KEYDOWN:
                # If the Esc key is pressed, then exit the main loop
                if event.key == K_ESCAPE:
                    running = False
            # Check for QUIT event. If QUIT, then set running to false.
            elif event.type == QUIT:
                running = False

        # Update the player
        player_group.update()
        # Update the enemies
        enemies_group.update(player)

        # Check if the player's iframes are over
        if player.iframes == 0:
            player.end_iframes()

        ### Thats just a placeholder log... replace the whole code with what is actualy needed
        # Display box position every 60 frames
        frame_count += 1
        if frame_count == Settings.FPS:
            frame_count = 0

            # Update position text
            # screen_logs.position_text = f"Box Position: {player.rect.x}, {player.rect.y}"
            screen_logs.position_text = f"HP: {player.health}"

            logger.info(screen_logs.position_text)
            # Insert the current position at the beginning of the history
            screen_logs.screen_log_list.insert(0, screen_logs.position_text)

            # Keep only the last `text_history_max` positions
            if len(screen_logs.screen_log_list) > screen_logs.log_text_history_max:
                screen_logs.screen_log_list.pop()
        ########

        # Update the combined sprite group for rendering
        all_sprites.custom_draw(player)

        if Settings.ENABLE_ON_SCREEN_LOGS:
            # Set the background color of the text pane surface
            screen_logs.text_pane_surface.fill(screen_logs.text_pane_color)

            # Display the text history in the text pane
            text_y = screen_logs.text_pane_rect.y + 10
            for log in screen_logs.screen_log_list:
                text_surface = screen_logs.log_font.render(log, True, screen_logs.log_text_color)
                screen.blit(text_surface, (screen_logs.text_pane_rect.x + 15, text_y))
                text_y += 30  # Adjust the spacing as needed

                # Blit the text pane surface onto the screen
            screen.blit(screen_logs.text_pane_surface, (screen_logs.text_pane_rect.x, screen_logs.text_pane_rect.y))

            # Create a text surface for displaying FPS
            fps_surface = screen_logs.log_font.render(f"FPS: {current_fps}", True, screen_logs.log_text_color)
            # Display the FPS text on the screen
            screen.blit(fps_surface, (5, 5))  # Adjust the position as needed

        pygame.display.flip()
        clock.tick(Settings.FPS)

    pygame.quit()


if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
