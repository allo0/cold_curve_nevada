import sys

import pygame

from configs import logConf, assetsConf
from src.characters.playerModel import Player
from src.models.ColdCurveNevadaModel import ColdCurveNevada
from src.ui.button import Button

logger = logConf.logger


class LevelSelectionMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 800))
        pygame.display.set_caption("Level Selection")
        self.bg = pygame.image.load(assetsConf.UI["background"])
        self.font_path = assetsConf.UI["font"]
        self.username = ""
        self.difficulty = 1
        self.level_slider = pygame.Rect(200, 400, 880, 10)
        self.slider_positions = [self.level_slider.left + i * (self.level_slider.width / 4) for i in
                                 range(5)]  # 5 difficulty levels
        self.slider_button = pygame.Rect(self.slider_positions[self.difficulty - 1], 390, 20, 30)
        self.play_button = Button(image=None, pos=(640, 550), text_input="PLAY", font=self.get_font(40),
                                  base_color="White", hovering_color="Green")
        self.back_button = Button(image=None, pos=(640, 620), text_input="BACK", font=self.get_font(40),
                                  base_color="White", hovering_color="Green")

    def get_font(self, size):
        return pygame.font.Font(self.font_path, size)

    def run(self):
        while True:
            self.screen.blit(self.bg, (0, 0))
            level_mouse_pos = pygame.mouse.get_pos()

            self.draw_level_selection(level_mouse_pos)
            self.handle_events(level_mouse_pos)

            pygame.display.update()

    def draw_level_selection(self, mouse_pos):
        # Drawing the UI components
        level_text = self.get_font(45).render("Choose Difficulty", True, "White")
        level_rect = level_text.get_rect(center=(640, 100))
        self.screen.blit(level_text, level_rect)

        name_text = self.get_font(30).render("Enter Your Name:", True, "White")
        name_rect = name_text.get_rect(center=(640, 200))
        self.screen.blit(name_text, name_rect)

        input_rect = pygame.Rect(540, 250, 400, 50)
        input_rect.centerx = self.screen.get_rect().centerx
        pygame.draw.rect(self.screen, "White", input_rect, 2)

        name_input = self.get_font(30).render(self.username, True, "White")
        self.screen.blit(name_input, (input_rect.x + 5, input_rect.y + 5))

        # Difficulty selection
        difficulty_text = self.get_font(30).render("Choose Difficulty:", True, "White")
        difficulty_rect = difficulty_text.get_rect(center=(640, 350))
        self.screen.blit(difficulty_text, difficulty_rect)

        pygame.draw.rect(self.screen, "White", self.level_slider, 2)
        pygame.draw.rect(self.screen, "Green", self.slider_button)

        # Display difficulty numbers
        for i, pos in enumerate(self.slider_positions, start=1):
            difficulty_text = self.get_font(20).render(str(i), True, "White")
            self.screen.blit(difficulty_text, (pos - difficulty_text.get_width() / 2, self.level_slider.top - 30))

        if self.username != "":
            self.play_button.changeColor(mouse_pos)
            self.play_button.update(self.screen)

        self.back_button.changeColor(mouse_pos)
        self.back_button.update(self.screen)

    def handle_events(self, mouse_pos):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.username != "":
                    self.start_game()
                elif event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                else:
                    self.username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button.checkForInput(mouse_pos) and self.username != "":
                    self.start_game()
                elif self.back_button.checkForInput(mouse_pos):
                    from src.ui.mainMenu import MainMenu

                    main_menu = MainMenu()
                    main_menu.main_loop()

                # Update difficulty based on slider interaction
                if self.level_slider.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    self.update_difficulty(mouse_pos)

    def update_difficulty(self, mouse_pos):
        # Snap slider to the nearest difficulty level based on mouse position
        self.slider_button.x = max(self.level_slider.left,
                                   min(mouse_pos[0], self.level_slider.right - self.slider_button.width))
        self.difficulty = min(range(1, 6), key=lambda i: abs(
            self.slider_button.x - self.slider_positions[i - 1]))  # Find nearest difficulty level
        self.slider_button.x = self.slider_positions[self.difficulty - 1]  # Snap to precise position

    def start_game(self):
        logger.info(f"Game started with player {self.username} and difficulty {self.difficulty}")
        # Initialize and start the game level with the selected difficulty and username
        cold_curve_nevada = ColdCurveNevada(player_index=sys.argv[1], multiplayer=False, difficulty=self.difficulty)
        player_instance = Player(cold_curve_nevada.player_pos[0], cold_curve_nevada.player_pos[1], self.username,
                                 cold_curve_nevada.sound_controller, assetsConf.PLAYER)
        cold_curve_nevada.add_player(player_instance=player_instance)
        cold_curve_nevada.main_loop()


if __name__ == "__main__":
    level_selection_menu = LevelSelectionMenu()
    level_selection_menu.run()
