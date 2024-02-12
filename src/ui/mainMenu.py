import sys

import pygame

from src.ui import levels
from src.ui.button import Button
from configs.assetsConf import UI


class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Menu")
        self.bg = pygame.image.load(UI["background"])
        self.font_path = UI["font"]
        self.play_button = Button(image=pygame.image.load(UI["play"]), pos=(640, 250),
                                  text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4",
                                  hovering_color="White")
        self.online_button = Button(image=pygame.image.load(UI["options"]), pos=(640, 400),
                                    text_input="ONLINE", font=self.get_font(75), base_color="#d7fcd4",
                                    hovering_color="White")
        self.quit_button = Button(image=pygame.image.load(UI["quit"]), pos=(640, 550),
                                  text_input="EXIT", font=self.get_font(75), base_color="#d7fcd4",
                                  hovering_color="White")
        self.menu_mouse_pos = pygame.mouse.get_pos()

    def get_font(self, size):
        return pygame.font.Font(self.font_path, size)

    def draw_menu(self):
        menu_text = self.get_font(70).render("Cold Curve Nevada", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))
        self.menu_mouse_pos = pygame.mouse.get_pos()
        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(menu_text, menu_rect)
        # Additional menu drawing logic goes here (e.g., buttons)
        for button in [self.play_button, self.online_button, self.quit_button]:
            button.changeColor(self.menu_mouse_pos)
            button.update(self.screen)

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.checkForInput(self.menu_mouse_pos):
                        levels.level_selection()  # Καλεί τη συνάρτηση level_selection() όταν πατηθεί το κουμπί "PLAY"
                    if self.online_button.checkForInput(self.menu_mouse_pos):
                        print("Options button clicked")  # Αντίστοιχη λειτουργικότητα για το κουμπί "OPTIONS"
                    if self.quit_button.checkForInput(self.menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            self.draw_menu()
            pygame.display.update()


if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.main_loop()
