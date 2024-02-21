import sys
import pygame
from configs import logConf
from configs.appConf import Settings
from configs.assetsConf import UI
from src.ui.button import Button
from src.utils.dataHandler import DataHandler

logger = logConf.logger

class ScoreMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 800))
        pygame.display.set_caption("Scores")
        self.bg = pygame.image.load(UI["background"])
        self.font_path = UI["font"]
        self.score_data_handler = DataHandler(Settings.SCORES)
        self.scores = self.score_data_handler.read_data()
        self.back_button = Button(image=None, pos=(640, 620),
                                  text_input="BACK", font=self.get_font(40), base_color="White", hovering_color="Green")
        self.mouse_pos = pygame.mouse.get_pos()

    def get_font(self, size):
        return pygame.font.Font(self.font_path, size)

    def draw_score_table(self, scores, top_left, table_size):
        column_names = ["Player Name", "Score", "Level", "Enemies Killed"]
        row_height = 40
        column_width = table_size[0] / len(column_names)

        # Draw column headers
        for index, name in enumerate(column_names):
            header_text = self.get_font(20).render(name, True, "White")
            self.screen.blit(header_text, (top_left[0] + column_width * index, top_left[1]))

        # Draw scores
        for row_index, score in enumerate(scores):
            row_data = [score.player_name, str(score.total_points), str(score.level), str(score.enemies_killed)]
            for col_index, cell in enumerate(row_data):
                cell_text = self.get_font(20).render(cell, True, "White")
                self.screen.blit(cell_text, (top_left[0] + column_width * col_index, top_left[1] + row_height * (row_index + 1)))

    def run(self):
        while True:
            self.screen.blit(self.bg, (0, 0))
            self.mouse_pos = pygame.mouse.get_pos()

            score_text = self.get_font(45).render("Scores", True, "White")
            score_rect = score_text.get_rect(center=(640, 100))
            self.screen.blit(score_text, score_rect)

            self.draw_score_table(self.scores, (100, 150), (1080, 420))
            self.back_button.changeColor(self.mouse_pos)
            self.back_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkForInput(self.mouse_pos):
                        return

            pygame.display.update()

# Usage example:
# if __name__ == "__main__":
#     score_menu = ScoreMenu()
#     score_menu.run()
