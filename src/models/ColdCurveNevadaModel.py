import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from configs import logConf
from configs.Events import (
    PLAYERDEATH, FINAL_BOSS_KILLED, )
from configs.appConf import Settings
from configs.assetsConf import SOUNDS, SOUND_LEVEL
from configs.entitiesConf import DUNGEON
from configs.screenLogConf import ScreenLog
from src.models.backgroundModel import BackgroundGenerator
from src.models.cameraModel import CameraGroup
from src.models.soundModel import SoundController
from src.ui.hud import HUD
from src.utils.spawnFunctions import Spawner


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

        # Initialize the RandomDungeon and generate the dungeon layout
        self.dungeon = BackgroundGenerator(DUNGEON['width'], DUNGEON['height'])
        self.player_pos = self.dungeon.generate_dungeon()

        self.static_sprites = None

        # Initialize the SoundController
        self.sound_controller = SoundController()

        # Set if it is multiplayer or not
        self.multiplayer = multiplayer

        # Create a Network instance for communication
        self.network = None

        # Create a list to dynamically store connected players
        self.players = []
        self.player_index = player_index

        self.total_enemies_killed = 0

        # Game difficulty
        self.difficulty = difficulty

        # Create sprite groups
        self.player_group = pygame.sprite.Group()  # Create a group for the player
        self.enemies_group = pygame.sprite.Group()  # Create a group for enemies

        # Create a combined group for rendering
        self.all_sprites = CameraGroup()

        self.enemies = pygame.sprite.Group()

        self.spawner = Spawner(sprite_group=self.all_sprites, enemy_group=self.enemies_group, player=self.players,
                               sound_controller=self.sound_controller)

        self.screen_logs = ScreenLog()
        self.frame_count = 0  # Initialize frame count
        self.running = True
        self.dt = 0
        self.hud = HUD(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            elif event.type == QUIT:
                self.running = False
            elif event.type == PLAYERDEATH:
                # Here will be a death screen or something
                self.logger.debug(event.custom_text)
                self.sound_controller.play_sound(SOUNDS["death"], SOUND_LEVEL["death"])
                self.running = False
            elif event.type == FINAL_BOSS_KILLED:
                self.logger.debug(event.custom_text)
                self.sound_controller.play_sound(SOUNDS["victory"], SOUND_LEVEL["victory"])

    def update(self):

        self.player_group.update(enemies=self.enemies, wall_rects=self.dungeon.wall_rects, dt=self.dt, hud=self.hud)
        self.enemies_group.update(players=self.players,
                                  obstacles=self.dungeon.wall_rects)  # Update enemies based on all players

    def render(self):
        self.screen.fill((0, 0, 0))  # Fill with black
        # Render the static dungeon (not affected by the camera)
        for sprite in self.static_sprites:
            self.screen.blit(sprite.image, sprite.rect)

        for player in self.players:
            self.all_sprites.custom_draw(player)
            self.frame_count += 1
            if self.frame_count == Settings.FPS:
                self.frame_count = 0

        self.hud.draw()
        pygame.display.flip()

    def main_loop(self):

        self.dt = self.clock.tick(60) / 1000
        self.static_sprites = self.dungeon.create_static_sprites()

        # Start the background music
        self.sound_controller.start_playlist(SOUND_LEVEL["ambient"])

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

            # Get total kills for all players

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
