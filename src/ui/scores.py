import sys

import pygame

from configs import logConf
from configs.appConf import Settings
from configs.assetsConf import UI, PLAYER
from src.characters.playerModel import Player
from src.models.ColdCurveNevadaModel import ColdCurveNevada
from src.ui.button import Button
from src.utils.dataHandler import DataHandler

logger = logConf.logger

pygame.init()

SCREEN = pygame.display.set_mode((1280, 800))
pygame.display.set_caption("Level Selection")

BG = pygame.image.load(UI["background"])


def get_font(size):
    return pygame.font.Font(UI["font"], size)


def draw_score_table(scores, screen, top_left, table_size):
    column_names = ["Player Name", "Score", "Level", "Enemies Killed"]
    row_height = 40
    column_width = table_size[0] / len(column_names)

    # Draw column headers
    for index, name in enumerate(column_names):
        header_text = get_font(20).render(name, True, "White")
        screen.blit(header_text, (top_left[0] + column_width * index, top_left[1]))

    # Draw scores
    for row_index, score in enumerate(scores):
        row_data = [score.player_name, str(score.total_points), str(score.level), str(score.enemies_killed)]
        for col_index, cell in enumerate(row_data):
            cell_text = get_font(20).render(cell, True, "White")
            screen.blit(cell_text, (top_left[0] + column_width * col_index, top_left[1] + row_height * (row_index + 1)))


def score_selection():
    score_data_handler = DataHandler(Settings.SCORES)
    scores = score_data_handler.read_data()

    while True:
        SCREEN.blit(BG, (0, 0))
        LEVEL_MOUSE_POS = pygame.mouse.get_pos()

        LEVEL_TEXT = get_font(45).render("Scores", True, "White")
        LEVEL_RECT = LEVEL_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(LEVEL_TEXT, LEVEL_RECT)
        # Assuming scores are loaded into a list of PlayerScore objects
        draw_score_table(scores, SCREEN, (100, 150), (1080, 420))
        BACK_BUTTON = Button(image=None, pos=(640, 620),
                             text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")

        BACK_BUTTON.changeColor(LEVEL_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(LEVEL_MOUSE_POS):
                    return

        pygame.display.update()

