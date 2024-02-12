import sys

from configs.assetsConf import PLAYER
from models.ColdCurveNevadaModel import ColdCurveNevada
from src.characters.playerModel import Player
from src.ui.mainMenu import MainMenu

# TODO implement create a randomly generated map (with walls and collision etc) each time (but somewhat big to show the camera functionality)
# TODO implement HUD
# TODO implement graphics
# TODO implement sounds
# TODO implement welcoming screen
# TODO online/multiplayer functionality
# TODO cleanup and optimizations

if __name__ == "__main__":
    # cold_curve_nevada = ColdCurveNevada(player_index=sys.argv[1], multiplayer=False, difficulty=1)
    # player_instance = Player(cold_curve_nevada.player_pos[0], cold_curve_nevada.player_pos[1],
    #                          cold_curve_nevada.sound_controller, PLAYER )
    # cold_curve_nevada.add_player(player_instance=player_instance)
    # cold_curve_nevada.main_loop()
    main_menu = MainMenu()
    main_menu.main_loop()