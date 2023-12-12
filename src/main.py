import sys

from cold_curve_nevada.src.characters.playerModel import Player
from models.ColdCurveNevadaModel import ColdCurveNevada

# TODO write unit tests where applicable
# TODO implement spawns and mob variety
# TODO add somehow a sort of scoring, and storage in a database ( I guess )
# TODO implement mob loot and scoring
# TODO implement create a randomly generated map (with walls and collision etc) each time (but somewhat big to show the camera functionality)
# TODO implement HUD
# TODO implement graphics
# TODO implement sounds
# TODO implement welcoming screen
# TODO online/multiplayer functionality
# TODO cleanup and optimizations

if __name__ == "__main__":
    cold_curve_nevada = ColdCurveNevada(player_index=sys.argv[1], multiplayer=False, difficulty=1)
    player_instance = Player(100, 100)
    cold_curve_nevada.add_player(player_instance=player_instance)
    cold_curve_nevada.main_loop()
