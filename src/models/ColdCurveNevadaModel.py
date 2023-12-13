import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from cold_curve_nevada.configs import logConf
from cold_curve_nevada.configs.Events import (
    PLAYERDEATH,
)
from cold_curve_nevada.configs.appConf import Settings
from cold_curve_nevada.configs.screenLogConf import ScreenLog
from cold_curve_nevada.src.models.cameraModel import CameraGroup
from cold_curve_nevada.src.utils.spawnFunctions import Spawner


class ColdCurveNevada():

    def __init__(self, difficulty: 1, player_index: 0, multiplayer: False) -> None:
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
        self.multiplayer = multiplayer

        # Create a Network instance for communication
        self.network = None

        # Create a list to dynamically store connected players
        self.players = []
        self.player_index = player_index

        # Game difficulty
        self.difficulty = difficulty

        # Create sprite groups
        self.player_group = pygame.sprite.Group()  # Create a group for the player
        self.enemies_group = pygame.sprite.Group()  # Create a group for enemies

        # Create a combined group for rendering
        self.all_sprites = CameraGroup()

        self.enemies = pygame.sprite.Group()


        self.spawner = Spawner(sprite_group=self.all_sprites, enemy_group=self.enemies_group, player=self.players)

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
            elif event.type == PLAYERDEATH:
                # Here will be a death screen or something
                self.logger.info(event.custom_text)
                self.running = False
            #     NOT USED YET (if ever)
            # elif event.type == ENEMYDEATH:
            #     # Here will be a death screen or something
            #     self.logger.info(event.custom_text)

    def update(self):

        self.player_group.update(self.enemies)
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

            self.update()
            self.handle_events()

            # Spawn and add new enemies to the main sprite group
            new_enemies = self.spawner.spawn_enemies(difficulty=self.difficulty)
            for enemy in new_enemies:
                self.enemies.add(enemy)
            self.enemies_group.add(self.enemies)  # Add the enemies to the group
            self.all_sprites.add(self.enemies)

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
        player_instance.mulitplayer = self.multiplayer
        self.network = player_instance.set_network(player_instance=player_instance, player_index=self.player_index)
        # self.players[int(self.player_index)].update_from_data(player_instance.get_player_data())
        # player_instance.init_network()  # Initialize network connection
        # self.network.send(player_data)
        self.player_group.add(player_instance)  # Add the player to the group
        self.all_sprites.add(player_instance.aoe_zone)
        # self.all_sprites.add(player_instance.line_of_doom)
        self.all_sprites.add(player_instance)