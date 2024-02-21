import sys
import pygame
from configs import logConf
from configs.assetsConf import UI
from src.ui.button import Button

logger = logConf.logger

class GameEndScreen:
    def __init__(self, end_type: str, end_text: str):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 800))
        pygame.display.set_caption("Game Ended")

        self.bg = pygame.image.load(UI["background"])
        self.font_path = UI["font"]
        self.end_type = end_type
        self.end_text = end_text

        self.restart_button = Button(image=None, pos=(640, 350),
                                     text_input=self.end_type, font=self.get_font(40), base_color="White", hovering_color="Green")
        self.exit_button = Button(image=None, pos=(640, 450),
                                  text_input="EXIT", font=self.get_font(40), base_color="White", hovering_color="Green")

    def get_font(self, size):
        return pygame.font.Font(self.font_path, size)

    def run(self):
        while True:
            self.screen.blit(self.bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            # Game Ended Text
            end_text_rendered = self.get_font(45).render(self.end_text, True, "White")
            end_rect = end_text_rendered.get_rect(center=(640, 100))
            self.screen.blit(end_text_rendered, end_rect)

            # Display buttons
            for button in [self.restart_button, self.exit_button]:
                button.changeColor(mouse_pos)
                button.update(self.screen)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button.checkForInput(mouse_pos):
                        logger.info("Game restart selected.")
                        from src.ui.levels import LevelSelectionMenu
                        level_selection_screen = LevelSelectionMenu()
                        level_selection_screen.run()
                    elif self.exit_button.checkForInput(mouse_pos):
                        logger.info("Exit game selected.")
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

