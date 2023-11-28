import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from configs import logConf
from configs.appConf import Settings
from configs.screenLogConf import ScreenLog
from src.characters.generEnemyModel import Enemy
from src.utils.cameraModel import CameraGroup


class ColdCurveNevada():

    def __init__(self, player_index) -> None:
        super().__init__()
        pygame.init()  # Initialize Pygame

        # Create the game window
        self.screen = pygame.display.set_mode(Settings.RESOLUTION)
        pygame.display.set_caption(Settings.PROJECT_NAME)
        self.clock = pygame.time.Clock()

        if Settings.ENABLE_LOGS:
            logConf.configure_logging()

        # init logger
        self.logger = logConf.logger

        # Create an instance of BackgroundGenerator
        # self.background = BackgroundGenerator()

        # Set if it is multiplayer or not
        self.multiplayer = True  # TODO migrate it to appconfig

        # Create a Network instance for communication
        self.network = None

        # Create a list to dynamically store connected players
        self.players = []
        self.player_index = player_index

        # Create sprite groups
        self.player_group = pygame.sprite.Group()  # Create a group for the player
        self.enemies_group = pygame.sprite.Group()  # Create a group for enemies

        # Create a combined group for rendering
        self.all_sprites = CameraGroup()

        self.enemies = pygame.sprite.Group()
        # for _ in range(5):  # Create 5 enemy characters (you can adjust the number)
        #     enemy = Enemy()
        #     self.logger.info(f"Instantiated {enemy.id}")
        #     self.enemies.add(enemy)

        # # Modify player instances for multiplayer
        # for player in self.players:
        #     player.set_multiplayer(self.multiplayer)
        #     player.set_network(self.network)  # You might want to adjust this based on your actual network setup
        #     player.init_network(player_index=player_index)  # Initialize network connection
        #     self.player_group.add(player)  # Add the player to the group
        #     self.all_sprites.add(player)

        self.enemies_group.add(self.enemies)  # Add the enemies to the group
        self.all_sprites.add(self.enemies)

        self.screen_logs = ScreenLog()
        self.frame_count = 0  # Initialize frame count
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == QUIT:
                self.running = False

    def update(self):
        self.player_group.update()
        self.enemies_group.update(self.players)  # Update enemies based on all players

    def render(self):
        self.screen.fill((0, 0, 0))  # Fill with black
        self.all_sprites.custom_draw(self.players)

        for player in self.players:
            self.frame_count += 1
            if self.frame_count == Settings.FPS:
                self.frame_count = 0

        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update()

            if self.multiplayer:
                # Send and receive player data through the network
                for idx, player in enumerate(self.players):
                    player_data = player.get_player_data()
                    self.network.send(player_data)

                    # Update other players' positions based on received data
                    other_player_data = self.network.send("")  # Sending an empty message just to receive data
                    if other_player_data is not None and idx != self.network.get_player_index():
                        player.update_from_data(other_player_data)

            self.render()
            self.clock.tick(Settings.FPS)

        # Cleanup on disconnect
        self.network.close()
        pygame.quit()

    def add_player(self, player_instance):
        player_data = player_instance.get_player_data()
        # Now that the player is added, create and set up the Network instance
        # self.network = Network(init_network=self.multiplayer,
        #                        player_index=self.player_index)  # Adjust player_index accordingly

        # Add a player instance to the list
        self.players.append(player_instance)
        player_instance.set_multiplayer(self.multiplayer)
        self.network = player_instance.set_network(player_index=self.player_index)  # You might want to adjust this based on your actual network setup
        player_instance.init_network()  # Initialize network connection
        # self.network.send(player_data)

        self.player_group.add(player_instance)  # Add the player to the group
        self.all_sprites.add(player_instance)
