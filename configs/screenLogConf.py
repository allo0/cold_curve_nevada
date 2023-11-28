import pygame
from configs.appConf import Settings


class ScreenLog:

    def __init__(self) -> None:
        super().__init__()
        # Font settings
        self.log_font = pygame.font.Font(None, 36)
        self.log_text_color = (255, 255, 255)

        # Log text pane settings
        self.log_text_history_max = Settings.LOG_DISPLAY_DURATION  # Maximum number of positions to display
        self.text_pane_rect = pygame.Rect(Settings.SCREEN_WIDTH - 310, 10, 300, 35 * self.log_text_history_max)
        self.text_pane_surface = pygame.Surface((self.text_pane_rect.width, self.text_pane_rect.height))
        self.text_pane_surface.set_alpha(128)  # Set alpha value for transparency
        self.text_pane_color = (50, 50, 50)  # Background color without alpha
        self.screen_log_list = []  # List to store position history
        self.position_text = ""  # Initialize position text
