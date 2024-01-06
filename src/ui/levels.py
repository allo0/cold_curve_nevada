# level_selection.py

import pygame
import sys
from button import Button
from src.characters.playerModel import Player
from src.utils.ColdCurveNevadaModel import ColdCurveNevada

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Level Selection")

BG = pygame.image.load("assets/Background.png")


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def main_menu():
    # προσπαθώ να καλέσω το main
    from ui.mainMenu import main_menu

    main_menu()


def level_selection():
    username = ""
    difficulty = 1

    level_slider = pygame.Rect(200, 400, 880, 10)
    slider_button = pygame.Rect(200 + (difficulty - 1) * 176, 390, 20, 30)

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

        if level_slider.collidepoint(LEVEL_MOUSE_POS):
            if pygame.mouse.get_pressed()[0]:  # πρεπει να πατησει ο χρηστης κλικ (υποθετικα)
                slider_button.x = max(level_slider.left, min(LEVEL_MOUSE_POS[0], level_slider.right - 20))
                difficulty = round((slider_button.x - level_slider.left) / (level_slider.width - 20) * 4) + 1

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
                    print(f"Username: {username}, Difficulty: {difficulty}")
                    cold_curve_nevada = ColdCurveNevada(player_index= 0, multiplayer=False, difficulty=difficulty)

                    player_instance = Player(100, 100)
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
                    print(f"Username: {username}, Difficulty: {difficulty}")
                    cold_curve_nevada = ColdCurveNevada(player_index= 0 , multiplayer=False, difficulty=1)
                    player_instance = Player(100, 100)
                    cold_curve_nevada.add_player(player_instance=player_instance)
                    cold_curve_nevada.main_loop()
                    return

                elif PLAY_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    print(f"Username: {username}, Difficulty: {difficulty}")
                    cold_curve_nevada = ColdCurveNevada(player_index= 0 , multiplayer=False, difficulty=1)
                    player_instance = Player(100, 100)
                    cold_curve_nevada.add_player(player_instance=player_instance)
                    cold_curve_nevada.main_loop()
                    return

                elif BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    main_menu()  # Επιστροφή στο mainMenu

        pygame.display.update()


if __name__ == "__main__":
    level_selection()
