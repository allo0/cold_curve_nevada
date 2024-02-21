import sys

import pygame

from configs import logConf
from configs.assetsConf import UI, PLAYER
from src.characters.playerModel import Player
from src.models.ColdCurveNevadaModel import ColdCurveNevada
from src.ui.button import Button

logger = logConf.logger

pygame.init()

SCREEN = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Level Selection")

BG = pygame.image.load(UI["background"])


def get_font(size):
    return pygame.font.Font(UI["font"], size)


def go_back_to_main_menu():
    # προσπαθώ να καλέσω το main
    from src.ui.mainMenu import main_menu

    main_menu()


def level_selection():
    username = ""
    difficulty = 1

    # level_slider = pygame.Rect(200, 400, 880, 10)
    # slider_button = pygame.Rect(200 + (difficulty - 1) * 176, 390, 20, 30)
    level_slider = pygame.Rect(200, 400, 880, 10)
    slider_positions = [level_slider.left + i * (level_slider.width / 4) for i in range(5)]  # 5 difficulty levels
    slider_button = pygame.Rect(slider_positions[difficulty - 1], 390, 20, 30)

    while True:
        SCREEN.blit(BG, (0, 0))
        LEVEL_MOUSE_POS = pygame.mouse.get_pos()

        LEVEL_TEXT = get_font(45).render("Choose Difficulty", True, "White")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)

        NAME_TEXT = get_font(30).render("Enter Your Name:", True, "White")
        NAME_RECT = NAME_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(NAME_TEXT, NAME_RECT)

        input_rect = pygame.Rect(540, 250, 400, 50)
        input_rect.centerx = SCREEN.get_rect().centerx
        pygame.draw.rect(SCREEN, "White", input_rect, 2)

        name_input = get_font(30).render(username, True, "White")
        SCREEN.blit(name_input, (input_rect.x + 5, input_rect.y + 5))

        DIFFICULTY_TEXT = get_font(30).render("Choose Difficulty:", True, "White")
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(640, 350))
        SCREEN.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)

        pygame.draw.rect(SCREEN, "White", level_slider, 2)
        pygame.draw.rect(SCREEN, "Green", slider_button)

        # Display difficulty numbers
        for i, pos in enumerate(slider_positions, start=1):
            difficulty_text = get_font(20).render(str(i), True, "White")
            SCREEN.blit(difficulty_text,
                        (pos - difficulty_text.get_width() / 2, level_slider.top - 30))

        if level_slider.collidepoint(LEVEL_MOUSE_POS) and pygame.mouse.get_pressed()[0]:
            # Snap slider to the nearest difficulty level based on mouse position
            slider_button.x = max(level_slider.left, min(LEVEL_MOUSE_POS[0], level_slider.right - slider_button.width))
            # Update difficulty based on slider position
            difficulty = min(range(1, 6), key=lambda i: abs(
                slider_button.x - slider_positions[i - 1]))  # Find nearest difficulty level
            slider_button.x = slider_positions[difficulty - 1]  # Snap to the precise position for the difficulty

        PLAY_BUTTON = Button(image=None, pos=(640, 550),
                             text_input="PLAY", font=get_font(40), base_color="White", hovering_color="Green")

        BACK_BUTTON = Button(image=None, pos=(640, 620),
                             text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")

        if username != "":
            PLAY_BUTTON.changeColor(LEVEL_MOUSE_POS)
            PLAY_BUTTON.update(SCREEN)

        BACK_BUTTON.changeColor(LEVEL_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username != "":
                    logger.info(f"Game started with player {username} and difficulty {difficulty}")

                    cold_curve_nevada = ColdCurveNevada(player_index=sys.argv[1], multiplayer=False,
                                                        difficulty=difficulty)
                    player_instance = Player(cold_curve_nevada.player_pos[0], cold_curve_nevada.player_pos[1],
                                             username, cold_curve_nevada.sound_controller, PLAYER)
                    cold_curve_nevada.add_player(player_instance=player_instance)
                    cold_curve_nevada.main_loop()
                    return

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    pass
                elif 640 <= LEVEL_MOUSE_POS[0] <= 840 and 550 <= LEVEL_MOUSE_POS[1] <= 582 and username != "":
                    logger.info(f"Game started with player {username} and difficulty {difficulty}")

                    cold_curve_nevada = ColdCurveNevada(player_index=sys.argv[1], multiplayer=False,
                                                        difficulty=difficulty)
                    player_instance = Player(cold_curve_nevada.player_pos[0], cold_curve_nevada.player_pos[1],
                                             username, cold_curve_nevada.sound_controller, PLAYER)
                    cold_curve_nevada.add_player(player_instance=player_instance)
                    cold_curve_nevada.main_loop()
                    return

                elif PLAY_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    logger.info(f"Game started with player {username} and difficulty {difficulty}")

                    cold_curve_nevada = ColdCurveNevada(player_index=sys.argv[1], multiplayer=False,
                                                        difficulty=difficulty)
                    player_instance = Player(cold_curve_nevada.player_pos[0], cold_curve_nevada.player_pos[1],
                                             username, cold_curve_nevada.sound_controller, PLAYER)
                    cold_curve_nevada.add_player(player_instance=player_instance)
                    cold_curve_nevada.main_loop()
                    return

                elif BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    return  # Επιστροφή στο mainMenu

        pygame.display.update()


if __name__ == "__main__":
    level_selection()
